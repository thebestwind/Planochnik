from globals import bot
from db import create_tables, insert_default_drills,conn
import handlers
from config import *
from prep_bluer_video import process_missing_files

if __name__ == "__main__":
    create_tables()
    insert_default_drills(conn)
    for dur in time_of_drill:
        process_missing_files(original_video_dir, f"drill{dur}_clips_dir", dur)
    # process_missing_files(original_video_dir, prep_video_dir, 5)
    # process_missing_files(original_video_dir, drill25_clips_dir, 25)
    # process_missing_files(original_video_dir, drill35_clips_dir, 35)
    # process_missing_files(original_video_dir, drill45_clips_dir, 45)
    # process_missing_files(original_video_dir, drill55_clips_dir, 55)
    bot.polling(none_stop=True)

