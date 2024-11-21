import os
from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.resize import resize
from db import get_connection, script_path
from globals import user_actions
from concurrent.futures import ProcessPoolExecutor


def create_blurred_clip(video_clip, target_height, duration):
    # Увеличиваем размер видео для создания размытого эффекта
    enlarged_clip = video_clip.fx(resize, height=target_height * 1)
    # Устанавливаем прозрачность и длительность
    blurred_background = enlarged_clip.set_opacity(0.1).set_duration(duration)
    return blurred_background

def create_video_from_mp4(mp4_paths, number_of_drills=2, time_of_one_drill=25, number_of_rounds=1, pause_duration=5, output_path="output_video.mp4",
                          target_height=480):
    clips = []
    pre_final_clip = []
    total_duration = 0

    # Обрабатываем каждый MP4 из списка
    for idx, mp4_path in enumerate(mp4_paths, start=1):
        # Загружаем MP4 видео
        video_clip = VideoFileClip(str(mp4_path))
        # Изменяем размер видео
        video_clip = video_clip.fx(resize, height=target_height)

        # Корректная обработка длительности MP4
        if video_clip.duration < time_of_one_drill:
            repeat_count = int(time_of_one_drill / video_clip.duration) + 1
            looped_clip = concatenate_videoclips([video_clip] * repeat_count).subclip(0, time_of_one_drill)
        else:
            looped_clip = video_clip.subclip(0, time_of_one_drill)

        # Создаем заблюренный клип для паузы
        blurred_clip = create_blurred_clip(looped_clip, target_height, pause_duration)

        # Добавляем упражнение и заблюренный клип в список
        pre_final_clip.extend([blurred_clip, looped_clip])

        # Повторяем упражнение для каждого круга
    full_clip = pre_final_clip * number_of_rounds
    # Объединяем все клипы в одно видео
    final_clip = concatenate_videoclips(full_clip, method="compose")
    final_clip.final_clip.preview(output_path, fps=10)

    # Освобождаем память, закрывая все клипы
    for clip in pre_final_clip:
        clip.close()

    return output_path


# Функция для отправки видео вместо MP4
def get_pics(values2, message, bot, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    mp4_paths = []
    error = False

    # Собираем пути к MP4-файлам
    for num in values2:
        cursor.execute("SELECT drillID FROM drills WHERE drillName = ?", (num,))
        catch = cursor.fetchone()
        if catch:
            mp4_path = str(script_path / 'drills' / f'{catch[0]}.mp4')
            if os.path.exists(mp4_path):
                mp4_paths.append(mp4_path)
            else:
                error = True
        else:
            error = True

    conn.close()
    if error:
        bot.reply_to(message, "Ошибка при создании видео. Проверьте наличие файлов MP4.")
        return

    # Создаем видео из MP4-файлов
    # video_path = create_video_from_mp4(mp4_paths)
    print(user_actions.get_training_parameters(user_id))
    video_path = create_video_from_mp4(mp4_paths, *user_actions.get_training_parameters(user_id))

    with open(video_path, "rb") as video:
        bot.send_video(message.chat.id, video)
    # Удаляем временный видеофайл после отправки
    os.remove(video_path)