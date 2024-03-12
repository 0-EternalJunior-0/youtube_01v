import errno
import os
import sys

from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from zipfile import ZipFile
def authenticate_drive(credentials_path):
    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path,  # Шлях до вашого JSON-ключа
        ['https://www.googleapis.com/auth/drive']
    )
    gauth.Authorize()
    drive = GoogleDrive(gauth)
    return drive


def upload_to_drive(drive, local_dir_path, zip_dir):
    if zip_dir == 1:
        # Створіть архів, тільки якщо папка не порожня
        if os.listdir(local_dir_path):
            zip_file_name = "Zip_Rar.zip"
            with ZipFile(zip_file_name, 'w') as zip_file:
                for foldername, subfolders, filenames in os.walk(local_dir_path):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, local_dir_path)
                        zip_file.write(file_path, arcname)

            file_drive = drive.CreateFile({'title': os.path.basename(file_path)})
            file_drive.Upload()
            print(f"Файл '{zip_file_name}' Успішно завантажаний")

            # Видалення архіву після завантаження
            os.remove(zip_file_name)
            print(f"Архів '{zip_file_name}' видалено")
        else:
            print(f"Папка '{local_dir_path}' порожня. Нічого не завантажено.")
    else:
        # Загрузка всіх файлів без архівації
        for foldername, subfolders, filenames in os.walk(local_dir_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # Визначте відносний шлях від local_dir_path для визначення шляху на Google Drive
                relative_path = os.path.relpath(file_path, local_dir_path)
                # Створіть файл на Google Drive
                file_drive = drive.CreateFile({'title': relative_path, 'parents': [{'id': 'root'}]})
                # Завантажте вміст файлу
                file_drive.Upload()
                print(f"Файл '{relative_path}' Успішно завантажений на Google Drive")

def list_drive_files(drive):
    file_list = drive.ListFile().GetList()
    if not file_list:
        print("Немає файлів на гугол диску.")
    else:
        print("Файли на Google Drive:")
        for file_drive in file_list:
            print(file_drive['title'])


def delete_all_drive_files(drive):
    file_list = drive.ListFile().GetList()
    if not file_list:
        print("На Диску Google не знайдено файлів.")
    else:
        print("Видалення всіх файлів на Google Drive:")
        for file_drive in file_list:
            file_drive.Delete()
            print(f"File '{file_drive['title']}' deleted.")

def download_all_from_drive(drive, local_dir_path_downloaded):
    try:
        os.makedirs(local_dir_path_downloaded)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    if not file_list:
        print("На Диску Google не знайдено файлів для скачування.")
    else:
        print("Скачування усіх файлів з Google Drive:")
        for file_drive in file_list:
            try:
                # Заміна недопустимих символів в імені файлу
                safe_file_title = file_drive['title'].replace("\\", "_")

                # Завантаження інших файлів
                file_drive.GetContentFile(os.path.join(local_dir_path_downloaded, safe_file_title))
                print(f"File '{safe_file_title}' downloaded.")
            except Exception as e:
                print(f"Помилка під час обробки файлу '{file_drive['title']}': {e}")

if __name__ == "__main__":
    credentials_path = "key/aerobic-star-416510-e6f939d408db.json"  # Змініть на шлях до свого JSON-ключа
    local_dir_path = "content/"  # Змініть на шлях до вашого локального файлу скачування
    local_dir_path_downloaded = "downloaded/"  # Змініть на шлях до вашого локального файлу загрузка
    drive = authenticate_drive(credentials_path)
    while True:
        print('1- Загрузка на диск')
        print('2- Скачати все з диск')
        print('3- Список диска')
        print('4- Очистка диска')
        print('5- ехід')
        num = input()
        if num == '1':
            zip_dir = input("Завантажити як архів натисніть 1 \nЗавантажити як директорію натисніть - 2\n")
            # Загрузка файлу на Google Drive
            if zip_dir == '1' or zip_dir == '2':
                upload_to_drive(drive, local_dir_path, int(zip_dir))
        elif num == '2':
            # Завантаження всіх файлів з Google Drive
            download_all_from_drive(drive, local_dir_path_downloaded)
        elif num == '3':
            # Виведення списку файлів на Google Drive
            list_drive_files(drive)
        elif num == '4':
            # Видалення усіх файлів на Google Drive
            delete_all_drive_files(drive)
        elif num == '5':
            sys.exit()


