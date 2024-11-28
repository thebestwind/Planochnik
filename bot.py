from globals import bot
from db import create_tables, insert_default_drills,conn
import handlers
from config import *
from prep_bluer_video import process_missing_files

if __name__ == "__main__":
    create_tables()
    insert_default_drills(conn)
    for dur in [5]:
        process_missing_files(original_video_dir, f"drill{dur}_clips_dir", dur)
    bot.polling(none_stop=True)

