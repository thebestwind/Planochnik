import sqlite3
import pathlib
import sys
from config import DB_NAME
import json

script_path = pathlib.Path(sys.argv[0]).parent  # Абсолютный путь до каталога, где лежит скрипт
conn = sqlite3.connect(script_path /  DB_NAME)

def load_exercises_from_json(filename="exercises.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [(item["drillName"], item["type"]) for item in data]

#создание и наполнение таблиц
def get_connection():
    return sqlite3.connect(script_path / DB_NAME)
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS drills (drillID INTEGER PRIMARY KEY AUTOINCREMENT, drillName varchar(50), type varchar(50))')
    cursor.execute('CREATE TABLE IF NOT EXISTS workouts (drillName varchar(50), people varchar(50), date DATE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS people (peopleID INTEGER PRIMARY KEY AUTOINCREMENT, t_id varchar(50), surname varchar(50), name varchar(50))')
    conn.commit()
    conn.close()

def insert_default_drills(conn): #наполнение таблиц упражнениями
    own_connection = False
    if conn is None:
        conn = get_connection()
        own_connection = True
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS (SELECT 1 FROM drills);")
    catch = cursor.fetchone()
    if catch[0] == 0:
        exercises = load_exercises_from_json()
        cursor.executemany(
            'INSERT INTO drills (drillName, type) VALUES (?, ?)',
            exercises
        )
    conn.commit()
    if own_connection:
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
    if own_connection:
            conn.close()