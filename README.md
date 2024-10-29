Telegram Bot Planochnik

Этот Telegram-бот подбирает для пользователя случайные упражнения для тренировки кора, с учетом категорий групп мышц. 
Бот использует базу данных SQLite для хранения выполненных упражнений для каждого пользователя, чтобы они не повторялись, не вызвая привыкания к нагрузке.

Версии

	•	1.0.1 - Первый релиз
	•	1.0.2 - Исправлено подключение к БД
	•	1.0.3 - Исправлены баги записи упражнений и обновлены названия колонок в БД
	•	1.1.0 - Основна структура БД
	•	2.0.0 - Добавлены GIF-анимации для упражнений

Основные функции

	•	Предоставление случайных упражнений для тренировок, с учетом выполненных ранее.
	•	Отслеживание истории выполненных упражнений для каждого пользователя.
	•	Возможность удаления истории тренировок.
	•	Показ GIF-анимаций для выполнения упражнений.

Команды бота

	•	/start - Регистрация пользователя в базе данных и начало взаимодействия с ботом.
	•	/help - Информация о функциональности бота и использование команды.
	•	/delete - Удаление истории упражнений текущего пользователя.
 
Структура базы данных
База данных состоит из трех таблиц:

	•	drills - Содержит информацию об упражнениях.
	•	workouts - Записывает историю выполненных упражнений для каждого пользователя.
	•	people - Содержит данные о пользователях.

Как использовать

	1.	Начните с команды /start для регистрации.
	2.	Введите количество упражнений, которое хотите выполнить (1–10).
	3.	Используйте кнопку «Показать наглядно» для получения GIF-анимации.
	4.	Чтобы удалить историю тренировок, воспользуйтесь командой /delete.

Примечания

	•	Бот отслеживает до 10 упражнений на пользователя; по достижении лимита старые записи автоматически удаляются.
	•	Если возникает ошибка при отправке GIF-анимаций, повторите попытку через несколько минут, чтобы избежать ограничения Telegram на частоту сообщений.