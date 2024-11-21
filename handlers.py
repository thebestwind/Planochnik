from telebot import types
from create_video import get_pics
from db import db_table_val, get_connection
from utils import get_drills, workouts_db_update
import pathlib
import sys
from globals import user_actions,bot


script_path = pathlib.Path(sys.argv[0]).parent


# Обработчик команды /start, записываем пользователя в бд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    us_username = message.from_user.username
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    db_table_val(username=us_username, user_name=us_name, user_surname=us_sname, conn=None)
    # Создаем меню с кнопкой "Начать тренировку"
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Начать тренировку", callback_data="start_training")
    markup.add(start_button)
    bot.reply_to(message, "Готов к тренировке?", reply_markup=markup)


# Обработчик нажатия на кнопку "Начать тренировку"
@bot.callback_query_handler(func=lambda call: call.data == "start_training")
def start_training(call):
    # Переход к выбору количества упражнений
    bot.send_message(call.message.chat.id, "Нужно выбрать количество упражнений, которое сделаешь за один круг:")
    exercise_markup = types.InlineKeyboardMarkup(row_width=5)
    exercise_buttons = [types.InlineKeyboardButton(text=str(i), callback_data=f"exercise_count_{i}") for i in range(2, 12, 2)]
    exercise_markup.add(*exercise_buttons)
    bot.send_message(call.message.chat.id, "Сколько упражнений хочешь выполнить?", reply_markup=exercise_markup)


# Обработчик выбора количества упражнений
@bot.callback_query_handler(func=lambda call: call.data.startswith("exercise_count_"))
def choose_exercise_count(call):
    # Извлекаем количество упражнений
    user_id = call.message.chat.id
    number_of_drills = int(call.data.split("_")[2])

    # Используем user_actions для записи состояния
    user_actions.set_state(user_id, "number_of_drills", number_of_drills)

    # Переход к выбору времени тренировки
    bot.send_message(user_id, "Теперь выбери время на одно упражнение:")
    time_markup = types.InlineKeyboardMarkup(row_width=5)
    time_buttons = [types.InlineKeyboardButton(text=f"{time} сек", callback_data=f"time_{number_of_drills}_{time}")
                    for time in [25, 35, 45, 55]]
    time_markup.add(*time_buttons)
    bot.send_message(user_id, "Сколько секунд для каждого упражнения?", reply_markup=time_markup)

# Выбор количества кругов
@bot.callback_query_handler(func=lambda call: call.data.startswith("time_"))
def set_training_time(call):
    # Получаем количество упражнений и время выполнения
    user_id = call.message.chat.id
    _, _, time_of_one_drill = call.data.split("_")
    user_actions.set_state(user_id, "time_of_one_drill", int(time_of_one_drill))
    # Переход к выбору количества кругов
    rounds_markup = types.InlineKeyboardMarkup(row_width=5)
    rounds_buttons = [types.InlineKeyboardButton(text=str(rounds), callback_data=f"rounds_{rounds}")
                      for rounds in [1, 2, 3, 4, 5]]
    rounds_markup.add(*rounds_buttons)
    bot.send_message(user_id, "Теперь выбери количество кругов", reply_markup=rounds_markup)

# Генерация и выдача уникальных упражнений, обновление бд workouts
@bot.callback_query_handler(func=lambda call: call.data.startswith("rounds_"))
def set_training_rounds(call):
    # Получаем количество кругов
    number_of_rounds = int(call.data.split("_")[1])
    username = call.message.chat.username
    user_id = call.message.chat.id
    user_actions.set_state(user_id, "number_of_rounds", int(number_of_rounds))

    if user_actions.user_exists(user_id):
        number_of_drills = user_actions.get_state(user_id, "number_of_drills")
        time_of_one_drill = user_actions.get_state(user_id, "time_of_one_drill")

        # Подключение к базе данных
        conn = get_connection()
        cursor = conn.cursor()
        # Удаление старых данных, если тренировок больше 10
        cursor.execute("SELECT count(people) FROM workouts WHERE people = ?", (username,))
        num_drills_done = int(cursor.fetchone()[0])
        if num_drills_done + number_of_drills >= 10:
            cursor.execute("DELETE FROM workouts WHERE people = ?", [username])
            conn.commit()

        # Вызов функции, получение упражнений из бд
        values = get_drills(conn, number_of_drills, username)
        values2 = [str(item[0]) for item in values[:number_of_drills]]
        drills_str = '\n'.join(values2)
        # Сохраняем список упражнений
        user_actions.set_state(user_id, "drills_list", values2)
        # Обновляем базу данных
        workouts_db_update(values, number_of_drills, username, conn)
        conn.close()

        # Выдача списка упражнений пользователю, с кнопкой генерации видео
        pics_markup = types.InlineKeyboardMarkup()
        pics_button = types.InlineKeyboardButton(text="Показать наглядно", callback_data="get_pics")
        pics_markup.add(pics_button)
        total_time_workout = ((time_of_one_drill+5) * number_of_rounds * number_of_drills)
        total_time_workout_minutes = int(total_time_workout // 60)
        total_time_workout_seconds = int(total_time_workout % 60)

        # Отправляем сообщение с упражнениями
        bot.send_message(call.message.chat.id, f"Вот упражнения:\n\n{drills_str}\n\n"
                                               f"Время на упражнение: {time_of_one_drill} секунд\n"
                                               f"Количество кругов: {number_of_rounds}\n"
                                               f"Общее время тренировки: {total_time_workout_minutes}:{total_time_workout_seconds:02}", reply_markup=pics_markup)
    else: # Если пользователь пропустил предыдущие шаги.
        bot.send_message(call.message.chat.id, "Не удалось найти данные для тренировки. Начни заново. Введи любой символ")


# Обработчик для кнопки «Показать наглядно»
@bot.callback_query_handler(func=lambda call: call.data == "get_pics")
def get_pics_callback(call):
    user_id = call.message.chat.id
    if user_actions.get_state(user_id, "drills_list"):
        bot.send_message(call.message.chat.id, "Делаю видео, придётся подождать")
        get_pics(user_actions.get_state(user_id, "drills_list"), call.message, bot, user_id)  # Передаем только список упражнений
        # Удаляем список упражнений для пользователя после отправки видео
        user_actions.clear_state(user_id)
    else:
        bot.send_message(call.message.chat.id, "Не удалось найти список упражнений. Пожалуйста, начните тренировку заново.")


# Обработчик для отправки кнопки «Начать тренировку» на любое сообщение
@bot.message_handler(func=lambda message: True)
def always_show_start_button(message):
    # Создаем Inline клавиатуру с кнопкой «Начать тренировку»
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Начать тренировку", callback_data="start_training")
    markup.add(start_button)
    bot.reply_to(message, "Чтобы начать тренировку, нажмите кнопку ниже:", reply_markup=markup)


# Обработчик команды /who
@bot.message_handler(commands=['who'])
def who(message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT t_id FROM people")
    done_drill_list = cursor.fetchall()
    bot.reply_to(message, f"{done_drill_list}")
    for i in done_drill_list:
        bot.reply_to(message, i)
    conn.close()
