import os


def find_file_with_prefix(folder_path, prefix):
    # Отримайте список файлів у вказаній папці
    files = os.listdir(folder_path)

    # Пройдіться по файлам і знайдіть перший файл з вказаним префіксом
    for file in files:
        if file.startswith(prefix):
            # Поверніть повний шлях до файлу
            return os.path.join(folder_path, file)

    # Якщо файл із вказаним префіксом не знайдено, поверніть None
    return None


def find_files_with_prefix_list(folder_path, prefix):
    # Отримайте список файлів у вказаній папці
    files = os.listdir(folder_path)

    # Зберіть усі файли з вказаним префіксом
    matching_files = [file for file in files if file.startswith(prefix)]

    # Поверніть список повних шляхів до файлів
    return [os.path.join(folder_path, file) for file in matching_files]