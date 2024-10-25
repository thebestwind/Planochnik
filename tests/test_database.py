import pytest
import sqlite3
from db import db_table_val

@pytest.fixture
def temp_db():
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

def test_create_user(temp_db):
    db_table_val("test_id", "TestName", "TestSurname", temp_db)

    # Проверяем, что пользователь был добавлен
    cursor = temp_db.cursor()
    cursor.execute("SELECT * FROM people WHERE t_id = ?", ("test_id",))
    user = cursor.fetchone()
    assert user is not None
    assert user[1] == "test_id"
    assert user[2] == "TestName"
    assert user[3] == "TestSurname"