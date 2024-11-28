from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.resize import resize
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from create_video import create_blurred_clip
from db import get_drill_name
from config import *


def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    print("chek dirrr", directory)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
# def normalize_resolution(clip): #Принудительно округляет размеры видео до ближайших четных значений.
#     width, height = clip.size
#     normalized_width = (width // 2) * 2
#     normalized_height = (height // 2) * 2
#     print(f"Оригинальные размеры: {width}x{height}, нормализованные размеры: {normalized_width}x{normalized_height}")
#     return clip.resize(width=normalized_width, height=normalized_height)

# Находим файлы из original_dir, которых нет в prep_dir
def get_missing_files(original_dir, prep_dir):
    # ensure_directory_exists(prep_dir)
    # Список файлов в обеих директориях
    original_files = set(os.listdir(original_dir))
    prep_files = set(os.listdir(prep_dir))
    missing_files = original_files - prep_files
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


def create_clip_with_text(
        input_video_path, output_video_path, num_of_drill, target_height=720, duration=5
):
    video_clip = None
    looped_clip = None
    blurred_clip = None
    composite_clip = None

    try:
        # # Проверяем и создаем директорию, если она не существует
        # ensure_directory_exists(output_video_path)
        # Загружаем исходное видео
        video_clip = VideoFileClip(input_video_path)
        # video_clip = normalize_resolution(video_clip)

        # Устанавливаем длительность
        if video_clip.duration < duration:
            repeat_count = int(duration / video_clip.duration) + 1
            looped_clip = concatenate_videoclips([video_clip] * repeat_count).subclip(0, duration)
        else:
            looped_clip = video_clip.subclip(0, duration)

        # Размываем видео


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

        # Сохраняем результат
        composite_clip.write_videofile(output_video_path, fps=24)

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



# проверка использования
if __name__ == "__main__":
    input_path = "example.mp4"
    output_path = "blurred_with_text.mp4"
    create_clip_with_text(
        input_video_path="drills/2.mp4",
        output_video_path="drill25_clips_dir/prep_2.mp4",
        num_of_drill=3,
        target_height=720,
        duration= 25
    )