import pytest
import sqlite3
from utils import get_drills, workouts_db_update
import math

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
        ("Exercise2", "боковые"),
        ("Exercise3", "суперсмены"),
        ("Exercise4", "остальные")
    ])

    conn.commit()
    yield conn
    conn.close()

@pytest.mark.parametrize("req, resp", [(1,4),
                                       (4,4),
                                       (5,8),
                                       (8,8),
                                       (0,0)])

def test_get_drills(temp_db, req, resp):
    exercises = get_drills(temp_db, req, "test_user")
    if req > 1:
        assert exercises[0][0] in ['Exercise1', 'Exercise2', 'Exercise3', 'Exercise4']
    assert len(exercises) == math.ceil(resp / 4) * 4 #упражнения выдаются кратно кол-ву категорий, с округлением к большему.


@pytest.mark.parametrize("values, number, username", [
    ([("Exercise1",), ("Exercise2",), ("Exercise3",), ("Exercise4",)], 4, "test_user"),
    ([("Exercise1",), ("Exercise2",), ("Exercise3",), ("Exercise4",)], 3, "test_user"),
    ([("Exercise1",), ("Exercise2",), ("Exercise3",), ("Exercise4",)], 1, "test_user")
])
def test_workouts_db_update(temp_db, number, username, values):
    #values = [("Exercise1",), ("Exercise2",), ("Exercise3",)]
    workouts_db_update(values, number, username, temp_db)
    cursor = temp_db.cursor()
    cursor.execute("SELECT drillName, people, date FROM workouts")
    results = cursor.fetchall()
    assert len(results) == number
    for result in results:
        assert result[0] in [val[0] for val in values[:number]]  # Проверка, что упражнение добавлено
        assert result[1] == username  # Проверка имени пользователя
