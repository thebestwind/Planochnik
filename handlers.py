from datetime import datetime
import telebot
from telebot import types
from db import db_table_val, get_connection
from utils import get_drills, workouts_db_update
import time
from config import BOT_TOKEN
import pathlib
import sys

bot = telebot.TeleBot(BOT_TOKEN)
script_path = pathlib.Path(sys.argv[0]).parent


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    us_username = message.from_user.username
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    db_table_val(username=us_username, user_name=us_name, user_surname=us_sname)
    bot.reply_to(message, "Время подкачаться! \nВведи количество упражнений. От 1 до 10")


# Обработчик команды /who
@bot.message_handler(commands=['who'])
def who(message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select t_id FROM people")
    done_drill_list = cursor.fetchall()
    bot.reply_to(message, f"{done_drill_list}")
    for i in done_drill_list:
        bot.reply_to(message, i)
    conn.close()


# Функция для получения изображений
def get_pics(values2, message):
    conn = get_connection()
    cursor = conn.cursor()
    error = False
    for num in values2:
        cursor.execute("SELECT drillID FROM drills where drillName == ?", (num,))
        catch = cursor.fetchone()
        try:
            with open(script_path / 'drills' / f'{catch[0]}.gif', 'rb') as photo:
                    bot.send_animation(message.chat.id, photo)
                    time.sleep(1)
        except telebot.apihelper.ApiException as e:
            print(f"Ошибка при отправке изображения: {e}")
            error = True
            continue
    if error == True:
        bot.reply_to(message, 'Повртори попытку через 5 минут. Телеграму не понравилось, что ты получил много сообщений')
    conn.close()


# Обработчик сообщений с числами
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    start = datetime.now()
    username = message.from_user.username
    try:
        global values2
        number = int(message.text)
        if number <= 0 or number > 10: #если число не в диапазоне, то пропуск обработки
            bot.reply_to(message, "Введи от 1 до 10")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT count(people) FROM workouts where people == ?", (username,))
        num_drills_done = cursor.fetchall()
        num_drills_done = int(num_drills_done[0][0])
        # если выполненых упражнений больше 10, удаляем старые из бд
        if num_drills_done + number >= 10:
            cursor.execute("delete from workouts where people = ?", [username])
            conn.commit()
        values = get_drills(conn, number, username)
        values2 = [str(item[0]) for item in values[:number]]

        # Берем только столько значений, сколько указал пользователь
        values_str = '\n''\n'.join([str(item[0]) for item in values[:number]])
        # кнопка для картинок
        pics = types.InlineKeyboardMarkup()
        picsButton = types.InlineKeyboardButton(text="Показать наглядно", callback_data="get_pics")
        pics.add(picsButton)

        bot.reply_to(message, f"Вот твои упражнения:\n\n{values_str}", reply_markup=pics)
        workouts_db_update(values, number, username, conn) #записываем выданные упр в бд workots
        conn.close()
    except ValueError:
        bot.reply_to(message, 'Введи целое число.')


# Обработчик для callback кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_pics":
        get_pics(values2, call.message)

