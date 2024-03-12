from pytube import YouTube
import requests
import os
import re
import string

from unicodedata import normalize


def sanitize_filename(filename):
    # Вилучення всіх символів, крім букв, цифр, пробілів та деяких інших допустимих символів
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_filename = ''.join(c if c in valid_chars else '_' for c in filename)

    # Вилучення подвійних пробілів
    sanitized_filename = re.sub(' +', ' ', sanitized_filename)
    # Нормалізація Unicode
    sanitized_filename = normalize('NFKD', sanitized_filename).encode('ascii', 'ignore').decode('utf-8')

    return sanitized_filename
def download_audio_from_youtube(video_url, output_path='content'):
    try:
        yt = YouTube(video_url)

        # Вибираємо найвищу якість аудіо
        audio_stream = yt.streams.filter(only_audio=True).first()

        print(f"Завантаження аудіо з відео: {yt.title}")

        # Санітізація імені файла
        sanitized_filename = sanitize_filename(yt.title)
        audio_file_name = f"audio_{sanitized_filename}.mp3"
        audio_file_path = os.path.join(output_path, audio_file_name)

        # Завантаження аудіо
        audio_stream.download(output_path, filename=audio_file_name)

        print(f"Аудіо завантажено: {audio_file_path}")
        return sanitized_filename
    except Exception as e:
        print(f"Помилка під час завантаження аудіо: {e}")
        return None



def download_video(url, output_path, file_name):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Зберігаємо відео з заданим іменем файлу без аудіо
        full_path = os.path.join(output_path, file_name)
        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Відео було завантажено: {full_path}")

    except Exception as e:
        print(f"Помилка під час завантаження відео: {e}")


