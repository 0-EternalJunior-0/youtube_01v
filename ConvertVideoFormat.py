from moviepy.editor import VideoFileClip


def convert_video_format(input_file, output_file, target_resolution=(1920, 1080), target_format='mp4'):
    try:
        # Відкрийте відеофайл
        video_clip = VideoFileClip(input_file)

        # Змініть розмір відео
        resized_clip = video_clip.resize(newsize=(target_resolution[0], target_resolution[1]))

        # Конвертуємо в інший формат
        resized_clip.write_videofile(output_file, codec='libx264', fps=video_clip.fps, audio=False)

        print(f"Конвертація відео завершена: {output_file}")

    except Exception as e:
        print(f"Помилка під час конвертації відео: {e}")

if __name__ == "__main__":
    # Замініть це на ваші шляхи та імена файлів
    input_video_path = "2036944935.mp4"
    output_video_path = "output_video.mp4"

    # Вказати розмір вихідного відео (за замовчуванням 1920x1080)
    target_resolution = (1920, 1080)

    # Конвертація відео до потрібного формату та розміру
    convert_video_format(input_video_path, output_video_path, target_resolution)
