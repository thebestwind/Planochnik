import random
from datetime import datetime

#выбор списка упражнений из бд по типу, и исключение из выборки, которые уже сделал

def get_drills(conn, number, username):
    cursor = conn.cursor()
    types = ['планки', 'боковые', 'суперсмены', 'остальные']
    values = []
    while len(values) < number:
        for type in types:
            cursor.execute("SELECT drillName FROM drills WHERE type = ?", (type,))
            random_item = cursor.fetchall()
            drill_list = []

            cursor.execute("SELECT drillName FROM workouts WHERE people = ?", (username,))
            done_drill_list = cursor.fetchall()

            for drill in random_item:
                if drill not in done_drill_list:
                    drill_list.append(drill)

            # Проверяем, что drill_list не пуст
            if drill_list:
                val1 = random.choice(drill_list)
                values.append(val1)
            else:
                print(f"Нет доступных упражнений для категории {type}")

    return values

 #обновление бд сделанных упражнений
def workouts_db_update(values, number, username, conn):
    cursor = conn.cursor()
    # заполнение бд сделанных упражнений
    for item in values[:number]:
        item = str(*item)
        cursor.execute('INSERT INTO workouts (drillName, people, date) VALUES (?, ?, ?)',(item, username, datetime.now()))
        conn.commit()
    conn.close()