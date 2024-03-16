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


def upload_large_file_to_drive(drive, local_file_path, parent_id='root', chunk_size=30 * 1024 * 1024 * 1024):
    # Get file name and size
    file_name = os.path.basename(local_file_path)
    file_size = os.path.getsize(local_file_path)

    # Calculate number of chunks
    num_chunks = file_size // chunk_size + (1 if file_size % chunk_size != 0 else 0)

    # Create a folder on Drive to store the chunks
    folder_metadata = {
        'title': file_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_id}]
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    # Upload chunks
    with open(local_file_path, 'rb') as file:
        for i in range(num_chunks):
            start_byte = i * chunk_size
            end_byte = min((i + 1) * chunk_size, file_size)
            chunk_data = file.read(chunk_size)

            # Create chunk file
            chunk_file_name = f'{file_name}.part{i + 1}'
            chunk_file_path = os.path.join('/tmp', chunk_file_name)
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk_data)

            # Upload chunk file
            chunk_metadata = {
                'title': chunk_file_name,
                'parents': [{'id': folder['id']}]
            }
            chunk = drive.CreateFile(chunk_metadata)
            chunk.SetContentFile(chunk_file_path)
            chunk.Upload()

            # Remove temporary chunk file
            os.remove(chunk_file_path)

    print(f'File "{file_name}" uploaded successfully.')
def upload_to_drive(drive, local_dir_path, zip_dir):
    CHUNK_SIZE = 100 * 1024 * 1024  # 100 MB chunk size
    if zip_dir == 1:
        if os.listdir(local_dir_path):
            zip_file_name = "Zip_Rar.zip"
            with ZipFile(zip_file_name, 'w') as zip_file:
                for foldername, subfolders, filenames in os.walk(local_dir_path):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, local_dir_path)
                        zip_file.write(file_path, arcname)

            upload_large_file_to_drive(drive, zip_file_name)

            try:
                os.remove(zip_file_name)
                print(f"Архів '{zip_file_name}' видалено")
            except Exception as e:
                print(f"Помилка видалення архіву '{zip_file_name}': {e}")
        else:
            print(f"Папка '{local_dir_path}' порожня. Нічого не завантажено.")
    elif zip_dir == 2:
        parent_id = 'root'
        folder_name = os.path.basename(local_dir_path)
        folder_drive = drive.CreateFile(
            {'title': folder_name, 'parents': [{'id': parent_id}], 'mimeType': 'application/vnd.google-apps.folder'})
        folder_drive.Upload()
        folder_id = folder_drive['id']

        for item in os.listdir(local_dir_path):
            item_path = os.path.join(local_dir_path, item)
            if os.path.isfile(item_path):
                file_drive = drive.CreateFile({'title': item, 'parents': [{'id': folder_id}]})
                file_drive.SetContentFile(item_path)
                try:
                    file_drive.Upload()
                    print(f"Файл '{item}' успішно завантажено")
                except Exception as e:
                    print(f"Помилка завантаження файлу '{item}': {e}")
            elif os.path.isdir(item_path):
                upload_to_drive(drive, item_path, 2)
    elif zip_dir == 3:
        if os.path.isfile(local_dir_path):  # Перевірка, чи шлях вказує на файл
            file_drive = drive.CreateFile()
            file_drive.SetContentFile(local_dir_path)  # Встановлення файлу для завантаження
            try:
                file_drive.Upload()
                print(f"Файл '{local_dir_path}' успішно завантажено на Google Drive")
            except Exception as e:
                print(f"Помилка завантаження файлу '{local_dir_path}': {e}")
        else:
            print(f"Шлях '{local_dir_path}' не вказує на файл")
def list_drive_files(drive):
    total_size = 0
    file_list = drive.ListFile().GetList()
    if not file_list:
        print("Немає файлів на Google Диску.")
    else:
        print("Файли на Google Диску:")
        for file_drive in file_list:
            if 'folder' in file_drive['mimeType']:
                print(file_drive['title'])
            else:
                print(file_drive['title'])
                try:
                    file_size = int(file_drive['fileSize'])
                    total_size += file_size
                except KeyError:
                    print(f"Не вдалося отримати розмір для файлу: {file_drive['title']}")

    # Переведення розміру у мегабайти
    total_size_mb = total_size / (1024 * 1024)
    print(f"Загальний розмір файлів на диску: {total_size_mb:.2f} МБ")


def delete_all_drive_files(drive):
    file_list = drive.ListFile().GetList()
    if not file_list:
        print("На Диску Google не знайдено файлів.")
    else:
        print("Видалення всіх файлів на Google Drive:")
        for file_drive in file_list:
            file_drive.Delete()
            print(f"File '{file_drive['title']}' deleted.")

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def download_file_from_drive(file_drive, local_dir_path_downloaded):
    try:
        # Replace invalid characters in the file name
        safe_file_title = file_drive['title'].replace("/", "_").replace("\\", "_")
        # Download the file
        file_drive.GetContentFile(os.path.join(local_dir_path_downloaded, safe_file_title))
        print(f"File '{safe_file_title}' downloaded.")
    except Exception as e:
        print(f"Error downloading file '{file_drive['title']}': {e}")


def download_folder_from_drive(drive, folder_drive, local_dir_path_downloaded):
    try:
        # Replace invalid characters in the folder name
        safe_folder_title = folder_drive['title'].replace("/", "_").replace("\\", "_")
        # Create a local folder for the downloaded contents
        local_folder_path = os.path.join(local_dir_path_downloaded, safe_folder_title)
        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)

        # List all files and folders inside the folder
        folder_content = drive.ListFile({'q': f"'{folder_drive['id']}' in parents and trashed=false"}).GetList()

        # Recursively download files and folders inside the current folder
        for item_drive in folder_content:
            if item_drive['mimeType'] == 'application/vnd.google-apps.folder':
                download_folder_from_drive(drive, item_drive, local_folder_path)
            else:
                download_file_from_drive(item_drive, local_folder_path)

        print(f"Folder '{safe_folder_title}' downloaded.")
    except Exception as e:
        print(f"Error downloading folder '{folder_drive['title']}': {e}")

def download_all_from_drive(drive, local_dir_path_downloaded):
    try:
        if not os.path.exists(local_dir_path_downloaded):
            os.makedirs(local_dir_path_downloaded)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    if not file_list:
        print("No files found on Google Drive.")
    else:
        print("Downloading all files and folders from Google Drive:")
        for item_drive in file_list:
            if item_drive['mimeType'] == 'application/vnd.google-apps.folder':
                download_folder_from_drive(drive, item_drive, local_dir_path_downloaded)
            else:
                download_file_from_drive(item_drive, local_dir_path_downloaded)

if __name__ == "__main__":
    credentials_path = "key/aerobic-star-416510-e6f939d408db.json"  # Змініть на шлях до свого JSON-ключа
    local_dir_path = "../youtube_01v/content"  # Змініть на шлях до вашого локального файлу скачування
    local_dir_path_downloaded = r"../youtube/downloaded"  # Змініть на шлях до вашого локального файлу загрузка
    drive = authenticate_drive(credentials_path)
    while True:
        print('1- Загрузка на диск')
        print('2- Скачати все з диск')
        print('3- Список диска')
        print('4- Очистка диска')
        print('5- ехід')
        num = input()
        if num == '1':
            zip_dir = input("Завантажити як архів натисніть 1 \nЗавантажити як директорію натисніть - 2\nЗавантажити як 1 файл натисніть - 3\n")
            # Загрузка файлу на Google Drive
            if zip_dir == '1' or zip_dir == '2' or zip_dir == '3':
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


