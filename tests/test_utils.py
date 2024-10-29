import pytest
import sqlite3
from utils import get_drills

@pytest.fixture
def temp_db():
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
        ("Exercise2", "планки"),
        ("Exercise3", "остальные"),
    ])

    conn.commit()
    yield conn
    conn.close()


def test_get_drills(temp_db):
    exercises = get_drills(temp_db, 1, "test_user")
    assert len(exercises) == 1
    assert exercises[0][0] in ["Exercise1", "Exercise2", "Exercise3"]