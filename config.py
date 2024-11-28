import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = "planochnikDB3.sql"
time_of_drill = [5, 25, 35, 45, 55]
original_video_dir = "drills"

prep_video_dir = "prep_clips"
drill25_clips_dir = "drill25_clips_dir"
drill35_clips_dir = "drill35_clips_dir"
drill45_clips_dir = "drill45_clips_dir"
drill55_clips_dir = "drill55_clips_dir"

