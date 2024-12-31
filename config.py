import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
end_audio_path = "end_audio.mp3"
DB_NAME = "planochnikDB3.sql"

time_of_drill = [5, 25, 35, 45, 55]
original_video_dir = "drills"


prep_video_dir = "prep_clips"
drill25_clips_dir = f"drill{time_of_drill[1]}_clips_dir"
drill35_clips_dir = f"drill{time_of_drill[2]}_clips_dir"
drill45_clips_dir = f"drill{time_of_drill[3]}_clips_dir"
drill55_clips_dir = f"drill{time_of_drill[4]}_clips_dir"

