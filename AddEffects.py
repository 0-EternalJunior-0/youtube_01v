import os
import sys

from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageSequenceClip
import numpy as np

os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:/InstALL/ffmpeg-6.1.1-essentials_build/bin/ffmpeg.exe"
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
import imageio_ffmpeg as ffmpeg


def make_white_transparent(video_clip):
    # Отримайте кадри відео у форматі numpy array
    frames = [np.array(frame) for frame in video_clip.iter_frames()]

    desired_color = [0, 255, 18]
    # Створіть альфа-канал, де колір фону стає прозорим
    alpha_channel = np.all(np.array(frames)[:, :, :, :3] == desired_color, axis=-1) * 255
    alpha_channel = alpha_channel.astype(np.uint8)

    # Додайте альфа-канал до кадрів
    frames_with_alpha = np.concatenate([np.array(frames), alpha_channel[:, :, :, np.newaxis]], axis=-1)

    # Створіть новий відеокліп із створеними кадрами
    video_clip_with_alpha = ImageSequenceClip(list(frames_with_alpha), fps=video_clip.fps)
    return video_clip_with_alpha


def insert_overlay(video_path, logo, output_path, logo_time_start=0):
    # Завантажте основне відео
    main_video = VideoFileClip(video_path)

    # Завантажте відео заставку
    overlay = VideoFileClip(logo, audio=False)
    # Задайте розмір та положення логотипу відносно основного відео
    overlay_position = (0.5 * (main_video.size[0] - overlay.size[0]), 0.5 * (main_video.size[1] - overlay.size[1]))
    overlay_duration = overlay.duration
    logo_time_end = logo_time_start + overlay_duration
    overlay = make_white_transparent(overlay)

    # Вставте відео заставку в середину основного відео
    final_clip = CompositeVideoClip([main_video, overlay.set_position(overlay_position).set_duration(logo_time_end)])
    # Збережіть вихідне відео
    final_clip.write_videofile(output_path, codec='libx264', fps=main_video.fps, audio=False)



# Приклад використання:
logo = "content/Asset/channel_logo.mp4"
main_video_path = "content/YoutubeVideo_1/video_0.mp4"
output_video_path = "ваш_вихідний_файл.mp4"

insert_overlay(main_video_path, logo, output_video_path)
