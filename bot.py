from db import create_tables, insert_default_drills
from handlers import bot

if __name__ == "__main__":
    create_tables()
    insert_default_drills()
    bot.polling(none_stop=True)
