# tests/conftest.py
import sqlite3
import sys
import os

import pytest

# Добавляем корневую папку проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="function", autouse=True)
def temp_drills_and_workout_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Создаем таблицу drills для тестов
    cursor.execute('''CREATE TABLE drills (
                        drillID INTEGER PRIMARY KEY,
                        drillName TEXT,
                        type TEXT
                    )''')

    # Создаем таблицу workouts для тестов
    cursor.execute('''CREATE TABLE workouts (
                        drillName TEXT,
                        people TEXT,
                        date TEXT
                    )''')

    # Добавляем тестовые данные
    cursor.executemany("INSERT INTO drills (drillName, type) VALUES (?, ?)", [
        ("Exercise1", "планки"),
        ("Exercise2", "боковые"),
        ("Exercise3", "суперсмены"),
        ("Exercise4", "остальные")
    ])

    conn.commit()
    yield conn
    conn.close()

@pytest.fixture(scope="function", autouse=True)
def open_temp_people_db():
    # Создаем временную БД
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    # Создаем таблицу people для тестов
    cursor.execute('''CREATE TABLE people (
                        peopleID INTEGER PRIMARY KEY AUTOINCREMENT,
                        t_id TEXT,
                        name TEXT,
                        surname TEXT
                    )''')
    conn.commit()
    yield conn
    conn.close()

@pytest.fixture(scope="function", autouse=True)
def temp_drills_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Создаем таблицу drills для тестов
    cursor.execute('''CREATE TABLE drills (
                        drillID INTEGER PRIMARY KEY,
                        drillName TEXT,
                        type TEXT
                    )''')
    conn.commit()
    yield conn
    conn.close()