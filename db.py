import sqlite3
import pathlib
import sys
from config import DB_NAME

script_path = pathlib.Path(sys.argv[0]).parent  # Абсолютный путь до каталога, где лежит скрипт
conn = sqlite3.connect(script_path /  DB_NAME)

#создание и наполнение таблиц
def get_connection():
    return sqlite3.connect(script_path / DB_NAME)
#создание таблиц для записей бота
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS drills (drillID INTEGER PRIMARY KEY AUTOINCREMENT, drillName varchar(50), type varchar(50))')
    cursor.execute('CREATE TABLE IF NOT EXISTS workouts (drillName varchar(50), people varchar(50), date DATE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS people (peopleID INTEGER PRIMARY KEY AUTOINCREMENT, t_id varchar(50), surname varchar(50), name varchar(50))')
    conn.commit()
    conn.close()
#наполнение таблиц упражнениями
def insert_default_drills():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS (SELECT 1 FROM drills);")
    catch = cursor.fetchone()
    if catch[0] == 0:
        cursor.executemany(
            'INSERT INTO drills (drillName, type) VALUES (?, ?)',
            [
                ('Russian twist', 'остальные'),('Dead bug', 'остальные'),('Dead bug + отягощение в каждой руке', 'остальные'),('Dead bug arm hold (в руках отягощение держать в статике, ноги работают в обычном режиме)', 'остальные'),('Dead bug + band (в руках резина держать в статике или в динамике, ноги работают в обычном режиме)', 'остальные'),('Dead bug + legs hold band ( руки в обычном режиме, ноги согнуты под 90 градусов в колене и тзб и в натяжение держать резину)', 'остальные'),('Hip thrust', 'остальные'),('Hip thrust leg change ', 'остальные'),('Hollow body', 'остальные'),('Bird dog', 'планки'),('Shoulder touch plank', 'планки'),('Arm raise plank', 'планки'),('Plank saw', 'планки'),('Bear walk', 'планки'),('Lateral bear walk', 'планки'),('Crab walk', 'планки'),('Spiderman walk', 'планки'),('Plank jack', 'планки'),('Plank in and out (ип планка на прямых руках, постановка рук на ширине плеч, руками выполняем движение наружу, потом внутрь)', 'планки'),('Mountain Climber plank', 'планки'),('Hip raise plank', 'планки'),('Leg raise plank', 'планки'),('Hip drop plank', 'планки'),('Spiderman plank', 'планки'),('Push up plank', 'планки'),('Plank (обычная на предплечьях)', 'планки'),('Plank (на прямых руках)', 'планки'),('Standing walkout plank', 'планки'), ('Side plank', 'боковые'),('Side plank rotation', 'боковые'),('Side plank rotation + отягощение', 'боковые'),('Side plank star', 'боковые'),('Side plank kick', 'боковые'),('Side plank crunch', 'боковые'),('Side plank roll', 'боковые'),('side plank leg raise', 'боковые'),('Side plank leg raise band (маленькая резинка на голеностоп)', 'боковые'),('Side plank knee tuck + band', 'боковые'),('Side plank knee tuck+ band ( то же самое только в статике держать согнутую в колене ногу с натяжением резины)', 'боковые'),('Copenhagen plank', 'боковые'), ('Superman plank', 'суперсмены'),('Superman roll', 'суперсмены'),('Superman VTW', 'суперсмены'),('Superman VA', 'суперсмены'),('Superman hold', 'суперсмены'),('Superman lat pull-down resistance band', 'суперсмены')
            ]
        )
    conn.commit()
    conn.close()
#запись пользователя в бд при обращении, если его еще нет
def db_table_val(username: str, user_name: str, user_surname: str, conn: bool):
    own_connection = False
    if conn is None:
        conn = get_connection()
        own_connection = True
    cursor = conn.cursor()
    cursor.execute("SELECT t_id FROM people WHERE t_id == ?", (username,))
    catch = cursor.fetchone()
    if catch is None:
        cursor.execute('INSERT INTO people (t_id, name, surname) VALUES (?, ?, ?)', (username, user_name, user_surname))
        conn.commit()
        # Закрываем соединение, если оно было создано внутри этой функции
    if own_connection:
            conn.close()