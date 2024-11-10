import pytest
import sqlite3
from db import db_table_val, insert_default_drills
from unittest.mock import patch

def test_create_user(open_temp_people_db): #проверка функции добавления нового пользователя в таблицу db_table_val
    with patch('db.get_connection', return_value=open_temp_people_db):
        db_table_val("test_id", "TestName", "TestSurname", conn=open_temp_people_db)
        cursor = open_temp_people_db.cursor()
        cursor.execute("SELECT * FROM people WHERE t_id = ?", ("test_id",))
        user = cursor.fetchone()
        assert user is not None
        assert user[1] == "test_id"
        assert user[2] == "TestName"
        assert user[3] == "TestSurname"

def test_insert_default_drills(temp_drills_db): #проверка, упражнения добавляются в новую таблицу
    with patch('db.get_connection', return_value=temp_drills_db):
        insert_default_drills(temp_drills_db)
        cursor = temp_drills_db.cursor()
        cursor.execute("SELECT count(*) FROM drills")
        count = cursor.fetchone()[0]
        assert count > 0


def test_insert_default_drills_no_duplicates(temp_drills_db): #проверка, что упражнения НЕ добавляются в старую таблицу
    # Первый вызов функции — добавляем записи
    insert_default_drills(temp_drills_db)
    cursor = temp_drills_db.cursor()
    cursor.execute("SELECT COUNT(*) FROM drills")
    count_after_first = cursor.fetchone()[0]

    # Второй вызов функции — не должно добавляться записей
    insert_default_drills(temp_drills_db)
    cursor.execute("SELECT COUNT(*) FROM drills")
    count_after_second = cursor.fetchone()[0]
    assert count_after_first == count_after_second


def test_insert_default_drills_data_integrity(temp_db): #проверка, что таблица наполнилась верными данными
    insert_default_drills(temp_db)
    cursor = temp_db.cursor()
    cursor.execute("SELECT drillName, type FROM drills")
    rows = cursor.fetchall()
    expected_data = [
        ("Russian twist", "остальные"),
        ("Superman plank", "суперсмены"),
        ("Side plank", "боковые")
    ]
    for data in expected_data:
        assert data in rows, f"Запись {data} должна быть в таблице drills"