from moviepy.audio.AudioClip import concatenate_audioclips, CompositeAudioClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.resize import resize
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip
import os
from create_video import create_blurred_clip
from db import get_drill_name
from config import *


def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    print("chek dirrr", directory)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

# Находим файлы из original_dir, которых нет в prep_dir
def get_missing_files(original_dir, prep_dir):
    # ensure_directory_exists(prep_dir)
    # Список файлов в обеих директориях
    original_files = set(os.listdir(original_dir))
    prep_files = set(os.listdir(prep_dir))
    missing_files = original_files - prep_files
    # Исключаем системные файлы и файлы без видеоформатов
    video_extensions = {'.mp4', '.avi', '.mov'}  # Добавьте нужные форматы
    missing_files = [f for f in missing_files if os.path.splitext(f)[1].lower() in video_extensions]
    return list(missing_files)

# Обрабатывает недостающие файлы
def process_missing_files(original_dir, prep_dir, duration):
    if not os.path.exists(prep_dir):
        os.makedirs(prep_dir)

    missing_files = get_missing_files(original_dir, prep_dir)

    if not missing_files:
        print("Все файлы обработаны.")
        return

    print(f"Найдено {len(missing_files)} недостающих файлов. Начинаем обработку...")
    for file_name in missing_files:
        original_path = os.path.join(original_dir, file_name)
        prep_path = os.path.join(prep_dir, file_name)
        file_name_without_extension = os.path.splitext(os.path.basename(original_path))[0]

        try:
            create_clip_with_text(
                original_path, prep_path, file_name_without_extension, target_height=720, duration=duration
            )
            print(f"Файл обработан и сохранён: {prep_path}")
        except Exception as e:
            print(f"Ошибка при обработке {file_name}: {e}")

# создание предподготоленных клипов для видео
def create_clip_with_text(
        input_video_path, output_video_path, num_of_drill, target_height=720, duration=5
):
    video_clip = None
    looped_clip = None
    blurred_clip = None
    composite_clip = None

    try:
        # Загружаем исходное видео
        video_clip = VideoFileClip(input_video_path)

        # Устанавливаем длительность
        if video_clip.duration < duration:
            repeat_count = int(duration / video_clip.duration) + 1
            looped_clip = concatenate_videoclips([video_clip] * repeat_count).subclip(0, duration)
        else:
            looped_clip = video_clip.subclip(0, duration)

        # Изменяем размер основного видео
        resized_video_clip = looped_clip.fx(resize, height=target_height)

        # Получаем текст упражнения
        name_of_drill = get_drill_name(num_of_drill)
        countdown_clips = []

        # проверка типа ролика. Создаем текстовый клип, блюрим, таймер
        if duration < 15:
            text_clip = TextClip(str(name_of_drill), fontsize=45, font="Arial", color="white").set_position("center").set_duration(
                looped_clip.duration)
            resized_video_clip = create_blurred_clip(resized_video_clip, target_height, duration)

            # Создаём таймер обратного отсчёта
            for t in range(int(duration), 0, -1):
                countdown_text = TextClip(
                    f"Подготовка\n  Осталось: {t} сек",
                    fontsize=50,
                    font="Arial",
                    color="white"
                ).set_position(("right", "top")).set_duration(1)
                countdown_clips.append(countdown_text)
        else:
            text_clip = TextClip(str(name_of_drill), fontsize=40, font="Arial", color="black").set_position(
                "bottom").set_duration(looped_clip.duration)

            # Создаём таймер обратного отсчёта
            for t in range(int(duration), 0, -1):
                countdown_text = TextClip(
                    f"Работа \n Осталось: {t} сек",
                    fontsize=50,
                    font="Arial",
                    color="black"
                ).set_position(("right", "top")).set_duration(1)
                countdown_clips.append(countdown_text)

        # Объединяем все таймеры в один клип
        countdown_clip = concatenate_videoclips(countdown_clips)

        # Объединяем размытую версию с текстом и основным видео
        composite_clip = CompositeVideoClip([resized_video_clip.set_position("center"), text_clip, countdown_clip])


        # Загрузка аудиофайла
        end_audio = AudioFileClip(end_audio_path)

        # Ограничиваем длительность аудиофайла, чтобы она не превышала длительность видео
        end_audio = end_audio.subclip(0, min(looped_clip.duration, end_audio.duration))

        # Если у видео отсутствует аудио, создаём тишину с той же длительностью
        # if video_clip.audio is None:
        #     silence_audio = AudioClip(lambda t: 0, duration=looped_clip.duration).set_duration(looped_clip.duration)
        # else:
        #     silence_audio = video_clip.audio.set_duration(looped_clip.duration)

        silence_audio = AudioClip(lambda t: 0, duration=looped_clip.duration).set_duration(looped_clip.duration)

        # Установка нового аудиотрека в конец
        final_audio = CompositeAudioClip(
            [silence_audio, end_audio.set_start(looped_clip.duration - end_audio.duration+0.5)])

        # Установка аудиотрека для клипа
        composite_clip = composite_clip.set_audio(final_audio)

        # Сохраняем результат
        composite_clip.write_videofile(output_video_path, fps=24, audio_codec="aac")

    finally:
        # Закрываем клипы для освобождения памяти
        if video_clip:
            video_clip.close()
        if looped_clip:
            looped_clip.close()
        if blurred_clip:
            blurred_clip.close()
        if composite_clip:
            composite_clip.close()
        if end_audio:
            end_audio.close()

# проверка использования
if __name__ == "__main__":
    input_path = "example.mp4"
    output_path = "blurred_with_text.mp4"
    create_clip_with_text(
        input_video_path="drills/2.mp4",
        output_video_path="drill25_clips_dir/prep_2.mp4",
        num_of_drill=3,
        target_height=720,
        duration= 5
    )