from db import create_tables, insert_default_drills
from handlers import bot
from db import conn
if __name__ == "__main__":
    create_tables()
    insert_default_drills(conn)
    bot.polling(none_stop=True)


