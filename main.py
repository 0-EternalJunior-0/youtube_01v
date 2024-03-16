import os
import random
import sys

from Pexels import search_for_stock_videos
from DownloadVideo import download_audio_from_youtube, download_video
from output_data import num_videos_to_edit, url_audi_YouTube_topic, width_height, _directory
from Api_key import *
from data import find_file_with_prefix, find_files_with_prefix_list
from moviepy.editor import VideoFileClip, AudioFileClip
from Video import merge_videos, trim_video, overlay_audio

def main():
    pr = str(random.randint(0, 6000))

    for info, i in zip(url_audi_YouTube_topic, range(len(url_audi_YouTube_topic))):

        url = info['url']
        topic = info['_topic']
        directory = f"{_directory}/YoutubeVideo_{i}_{pr}"
        os.makedirs(directory, exist_ok=True)

        name = download_audio_from_youtube(url, output_path=directory)

        # Пошук відео на Pexels
        data_stock_videos = search_for_stock_videos(query=topic, api_key=api_key_pexels, it=2000, time_minimum=30, width_height=width_height)

        # Отримання розміру з максимального розміру відображення
        max_size = max(data_stock_videos.keys(), key=lambda x: len(data_stock_videos[x]))
        videos = data_stock_videos[max_size]

        print(f"{max_size} Доступне до скачування  = {len(videos)}")

        # Випадкове перемішування та обмеження кількості відео для скачування
        random.shuffle(videos)
        _num_videos_to_edit = min(num_videos_to_edit, len(videos))
        videos = videos[:_num_videos_to_edit]

        # Завантаження та збереження відео
        for i, video_info in enumerate(videos):
            url = video_info['url']
            file_name = f"video_{i}.mp4"
            download_video(url, directory, file_name)

        path_audi = find_file_with_prefix(directory, 'audio_')
        print(path_audi)
        audio_clip = AudioFileClip(path_audi)
        time_audio = audio_clip.duration

        list_video = find_files_with_prefix_list(directory,'video_')
        random.shuffle(list_video)

        list_video = list_video * 5000
        time_vido_all = 0
        video_all = VideoFileClip(list_video[0])
        time_vido_all = video_all.duration
        for _video_path in list_video[1:-1]:
            _video = VideoFileClip(_video_path)
            if (time_vido_all + _video.duration) > time_audio:
                new_time = abs((time_vido_all + _video.duration) - time_audio)
                _video = trim_video(_video, new_time)
                video_all = merge_videos(video_all, _video, audio=False)
                time_vido_all += _video.duration
                _video = None
                break
            else:
                video_all = merge_videos(video_all, _video, audio=False)
                time_vido_all += _video.duration
                _video = None
        print(f'Групування виконане відо триває = \t{time_vido_all}\n Аудіо файл становить = \t{time_audio}\n')
        list_video = None
        try:
            # Отримуємо мінімальну тривалість між відео та аудіо
            video_all = video_all.subclip(0, min(time_audio, video_all.duration))
            audio_clip = audio_clip.subclip(0, min(time_audio, video_all.duration))

            # Додаємо аудіо до відео
            video_all = video_all.set_audio(None)
            video_all = video_all.set_audio(audio_clip)

            # Звільняємо ресурси, пов'язані з аудіо

        except Exception as e:
            print(f"Error during audio and video processing: {e}")
        # Додаємо аудіо до відео
        video_all = video_all.set_audio(None)
        video_all = video_all.set_audio(audio_clip)
        # Звільняємо ресурси, пов'язані з аудіо
        audio_clip = None

        # Встановлюємо кількість кадрів на секунду (FPS)
        video_all = video_all.set_fps(30)

        # Зберігаємо відео зі зменшеними обчислювальними витратами та певними параметрами
        video_all.write_videofile(os.path.join(directory, f"YoutubeVideo_end_{topic}____{name}.mp4"), codec='libx264', audio_codec='aac')
        # Звільняємо ресурси, пов'язані з відео
        video_all = None
        del video_all , audio_clip , _video , time_audio , time_vido_all


if __name__ == '__main__':
    main()
