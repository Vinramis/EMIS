import os
import time


def extract_files(folder_path: str, case_insensitivity: bool, infix: list[str] | str):
    """
    Finds files in the specified folder by infixes in the filename, returns a list of filenames.
    """
    try:
        all_files = os.listdir(folder_path)
        matched_files = []
        if isinstance(infix, str):
            infix = [infix]

        files_to_check = list(all_files)
        processed_files = set()

        for inf in infix:
            search_inf = inf.lower() if case_insensitivity else inf

            for file in files_to_check:
                if file in processed_files:
                    continue

                search_file = file.lower() if case_insensitivity else file

                if search_inf in search_file:
                    matched_files.append(file)
                    processed_files.add(file)

    except Exception as e:
        print(f"[ОШИБКА] Ошибка при извлечении файлов: {e}")
        exit(0)

    return matched_files


def find_file_by_prefix(directory: str, prefix: str):
    """
    Finds the first file in the directory starting with the given prefix.
    """
    try:
        for filename in os.listdir(directory):
            if filename.lower().startswith(prefix.lower().strip()):
                return os.path.join(directory, filename)
    except FileNotFoundError:
        print(f"[ОШИБКА] Директория '{directory}' не существует.")
        return None
    except Exception as e:
        print(f"[ОШИБКА] Ошибка при поиске в директории '{directory}': {e}")
        return None
    return None


def numbers_in_string(string: str) -> list[int]:
    numbers_found = []
    number_buffer = ""
    for char in string:
        if char.isdigit():
            number_buffer += char
        else:
            if number_buffer:
                numbers_found.append(int(number_buffer))
                number_buffer = ""
    return numbers_found


def find_file_by_count(directory: str, count: int) -> str | None:
    """
    Finds the file in the directory with the given count.
    """
    directory = normalize_path(directory)
    try:
        for filename in os.listdir(directory):
            if numbers_in_string(filename)[0] == count:
                return os.path.join(directory, filename)
    except FileNotFoundError:
        print(f"[ОШИБКА] Директория '{directory}' не существует.")
        return None
    except Exception as e:
        print(f"[ОШИБКА] Ошибка при поиске в директории '{directory}': {e}")
        return None
    return None


def organize_files(topics_folder: str, homework_folder: str) -> tuple[str, str]:
    """
    Organizes files into TOPICS and HOMEWORK subfolders if they are currently in the same folder.
    Returns the new paths for TOPICS_FOLDER and HOMEWORK_FOLDER.
    """
    if os.path.abspath(topics_folder) == os.path.abspath(homework_folder):
        print("Разделение файлов тем и домашних заданий...")
        topic_keywords = ["кл", "лек", "урок"]
        homework_keywords = ["дз", "дом"]

        all_folder = topics_folder

        topic_files = extract_files(all_folder, True, topic_keywords)
        homework_files = extract_files(all_folder, True, homework_keywords)

        all_files_in_dir = os.listdir(all_folder)
        assigned_files = set(topic_files + homework_files)
        unassigned = [
            f
            for f in all_files_in_dir
            if f not in assigned_files and os.path.isfile(os.path.join(all_folder, f))
        ]

        if unassigned:
            print(
                f"[ИНФО] Остались нераспределенные файлы в папке '{all_folder}': {unassigned}"
            )
            print("(?) Просто разделите оставшиеся файлы вручную")
            print(
                "(?) Или добавьте ключевые слова в имена оставшихся файлов и перезапустите скрипт."
            )
            print("\n(?) --- Ключевые слова ---")
            print(f"(?) Для классных работа: {topic_keywords}")
            print(f"(?) Для домашних заданий: {homework_keywords}\n")
            time.sleep(2)

        new_topics_folder = os.path.join(os.path.dirname(all_folder), "КЛ")
        new_homework_folder = os.path.join(os.path.dirname(all_folder), "ДЗ")

        os.makedirs(new_topics_folder, exist_ok=True)
        os.makedirs(new_homework_folder, exist_ok=True)

        for file in topic_files:
            try:
                os.rename(
                    os.path.join(all_folder, file),
                    os.path.join(new_topics_folder, file),
                )
            except FileNotFoundError:
                pass

        for file in homework_files:
            try:
                os.rename(
                    os.path.join(all_folder, file),
                    os.path.join(new_homework_folder, file),
                )
            except FileNotFoundError:
                pass

        if not os.listdir(all_folder):
            try:
                os.rmdir(all_folder)
                print(
                    f"[ИНФО] Файлы успешно разделены на папки '{new_topics_folder}' и '{new_homework_folder}'."
                )
            except OSError:
                pass

        return new_topics_folder, new_homework_folder

    return topics_folder, homework_folder


def get_files(
    directory: str
) -> list[str]:
    """
    Returns the list of files in the directory.
    """
    directory = normalize_path(directory)
    found_items = os.listdir(directory)
    return [file for file in found_items if os.path.isfile(os.path.join(directory, file))]


def rename_single_excel(path, new_name="КТП.xlsx"):
    """
    Renames the single .xlsx file in the current directory to the specified name.
    """
    path = normalize_path(path)

    # 1. Get list of all files in the current directory
    files = os.listdir(path)

    # 2. Filter for .xlsx files (ignoring temporary ~$ files created by Excel)
    excel_files = [f for f in files if f.endswith(".xlsx") and not f.startswith("~$")]

    # 3. Check if exactly one file exists
    if len(excel_files) == 1:
        old_name = excel_files[0]

        # Avoid renaming if it's already named correctly
        if old_name == new_name:
            return
        try:
            os.rename(old_name, new_name)
            print("[ИНФО] Файл КТП найден!")
        except Exception as e:
            print(f"[ОШИБКА] Что-то пошло не так при поиске файла КТП: {e}")
    elif len(excel_files) == 0:
        print("[ОШИБКА] Файл КТП не найден")
    else:
        print(
            "[ОШИБКА] Найдено несколько файлов КТП. Пожалуйста, оставьте только один файл"
        )


def get_numerical_interval(directory: str) -> tuple[int, int]:
    """
    Returns the numerical interval of numerated files in the directory.
    """
    current_file_folder = os.path.dirname(
        __file__
    )  # C:\Users\rmura\OneDrive\Рабочий стол\EMIS is shit\emis automator\components
    if directory.startswith(".."):
        directory = directory[3:]  # ..\\КЛ
        current_file_folder_parent = os.path.dirname(
            current_file_folder
        )  # C:\Users\rmura\OneDrive\Рабочий стол\EMIS is shit
        directory = os.path.join(
            current_file_folder_parent, directory
        )  # C:\Users\rmura\OneDrive\Рабочий стол\EMIS is shit\КЛ
    else:
        directory = os.path.join(current_file_folder, directory)

    # 1. Get list of all files in the given directory
    files = os.listdir(directory)

    # 2. Filter for files that start with a number
    numerated_files = [f for f in files if numbers_in_string(f) != []]

    # 3. Get the numerical interval of the files
    numbers = [numbers_in_string(f)[0] for f in numerated_files]

    # 4. Return the numerical interval of the files
    return min(numbers), max(numbers)


def normalize_path(path) -> str:
    """
    Normalizes the path to the absolute path, depending on the caller file location.
    Handles paths starting with "..".
    """
    path = str(path)
    desirable_file_folder = os.path.dirname(__file__)  # C:\Users\rmura\OneDrive\Рабочий стол\EMIS is shit\emis automator\components
    if path.startswith(".."):
        path = path[3:]  # ..\\КЛ
        desirable_file_folder = os.path.dirname(desirable_file_folder)  # C:\Users\rmura\OneDrive\Рабочий стол\EMIS is shit=
    elif path.startswith(".") or path.startswith("\\"):
        path = path[2:]  # \КЛ
    path = os.path.join(desirable_file_folder, path)
    return path


def pure_name(path) -> str:
    """
    Returns the pure name of the file.
    """
    path = normalize_path(path)
    return os.path.basename(path)
