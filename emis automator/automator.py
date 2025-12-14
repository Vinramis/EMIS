import time
import json
import os
from playwright.sync_api import sync_playwright
import pandas as pd

# test message

# --- Конфигурация ---

ONE_ID_LOGIN_URL = "https://emis.edu.uz/login"
ONE_ID_BUTTON_SELECTOR = "#root > div > div > div > main > div > div > a"
LOGIN_FIELD_PLACEHOLDER = "Loginni kiriting"
PASSWORD_FIELD_PLACEHOLDER = "Parolni kiriting"
LOGIN_BUTTON_TEXT = "Kirish"
SUCCESS_URL = "https://emis.edu.uz"  # URL appearing after successful login
NEW_TOPIC_URL = "https://emis.edu.uz/teacher/topics/add"

# Загрузка конфигурации из файла JSON
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Учетные данные (из файла config.json)
login = config["credentials"]["login"]
password = config["credentials"]["password"]

# Настройки автоматизации (из файла config.json)
LINE_COUNT = config["automation_settings"]["LINE_COUNT"]
TOPICS_FILE_PATH = config["automation_settings"]["TOPICS_FILE_PATH"]
START_CELL = config["automation_settings"]["START_CELL"]
START_FROM_LINE = config["automation_settings"]["START_FROM_LINE"]
MODE = config["automation_settings"]["MODE"]
TOPICS_FOLDER = config["automation_settings"]["TOPICS_FOLDER"]
HOMEWORK_FOLDER = config["automation_settings"]["HOMEWORK_FOLDER"]




# Селекторы для элементов на странице
topics = "#topics_"
TOPIC_NAME = "_name"
TOPIC_FILE = "_topic_file"
HOMEWORK_FILE = "_homework_file"
ADD_LINE_BUTTON = ".Full"

# --- Конец Конфигурации ---


# --- Извлечение информации ---

def extract_files(folder_path: str, case_insensitivity: bool, infix: list[str] | str):
    """
    Находит файлы в указанной папке по инфиксам в имени файла, возвращает список имен файлов.
    """
    try:
        all_files = os.listdir(folder_path) # list.remove(x): x not in list исправить
        matched_files = []
        if isinstance(infix, str):
            infix = [infix]
        if case_insensitivity:
            # all_files = [file.lower() for file in all_files]
            infix = [inf.lower() for inf in infix]
        # print("not here")
        for inf in infix:
            for file in all_files:
                if case_insensitivity:
                    if inf in file.lower():
                        matched_files.append(file)
                        all_files.remove(file)  # Чтобы не обрабатывать файл несколько раз
                else:
                    if inf in file:
                        matched_files.append(file)
                        all_files.remove(file)  # Чтобы не обрабатывать файл несколько раз
    except Exception as e:
        print(f"[ОШИБКА] Произошла ошибка при извлечении файлов: {e}")
        exit(0)
    print("extract_files отработал правильно.")

    return matched_files

def find_file_by_prefix(directory: str, prefix: str):
    """
    Находит первый файл в указанной директории, имя которого начинается с заданного префикса.
    Возвращает полный путь к файлу или None, если файл не найден.
    """
    try:
        for filename in os.listdir(directory):
            # Сравнение без учета регистра и с удалением пробелов для надежности
            if filename.lower().startswith(prefix.lower().strip()):
                return os.path.join(directory, filename)
    except FileNotFoundError:
        print(f"[ОШИБКА] Директория '{directory}' не существует.")
        return None
    except Exception as e:
        print(f"[ОШИБКА] Произошла ошибка при поиске в директории '{directory}': {e}")
        return None
    
    return None

# def find_file_by_leading_count(directory: str, count: int):
#     """
#     Находит первый файл в указанной директории, имя которого начинается с заданного числа.
#     Возвращает имя файла или None, если файл не найден.
#     """
#     count_str = str(count)
#     wrong_symbol_counter = 0
#     wrong_symbol_counter_ceeling = 5

#     try:
#         for filename in os.listdir(directory):
#             length_of_count = len(count_str)
#             length_of_filename = len(filename)
#             # Сравнение без учета регистра и с удалением пробелов для надежности
#             while (i=0, i=+, wrong_symbol_counter < wrong_symbol_counter_ceeling and i < length_of_filename):
#                 if filename.lower().startswith(count_str):
#                     return filename
#     except FileNotFoundError:
#         print(f"[ОШИБКА] Директория '{directory}' не существует.")
#         return None
#     except Exception as e:
#         print(f"[ОШИБКА] Произошла ошибка при поиске в директории '{directory}': {e}")
#         return None

def next_col(col):
    """Инкрементирует буквенное обозначение столбца Excel (A -> B, Z -> AA)."""
    result = list(col)
    i = len(result) - 1
    while i >= 0:
        if result[i] != 'Z':
            result[i] = chr(ord(result[i]) + 1)
            return ''.join(result)
        else:
            result[i] = 'A'
            i -= 1
    return 'A' + ''.join(result)

def get_cell_value(data: pd.DataFrame, cell_ref: str):
    """Получает значение ячейки из DataFrame по ссылке (например, 'A1')."""
    col = ''.join(filter(str.isalpha, cell_ref)).upper()
    # Excel-строки 1-индексированы, pandas .iat 0-индексирован.
    row = int(''.join(filter(str.isdigit, cell_ref))) - 1

    col_index = 0
    for c in col:
        col_index = col_index * 26 + (ord(c) - ord('A') + 1)
    col_index -= 1

    if 0 <= row < len(data) and 0 <= col_index < len(data.columns):
        return data.iat[row, col_index]
    return None

def generate_sequence(data: pd.DataFrame, start_cell: str, mode: str) -> list:
    """Генерирует последовательность непустых ячеек из DataFrame."""
    sequence = []
    empty_cell_counter = 0
    MAX_EMPTY_CELLS_IN_A_ROW = 5

    current_col = ''.join(filter(str.isalpha, start_cell)).upper()
    current_row = int(''.join(filter(str.isdigit, start_cell)))

    while empty_cell_counter < MAX_EMPTY_CELLS_IN_A_ROW:
        cell_ref = f"{current_col}{current_row}"
        cell_value = get_cell_value(data, cell_ref)

        # Проверяем, пуста ли ячейка
        is_empty = pd.isna(cell_value) or len(str(cell_value).strip()) < 2

        if is_empty:
            empty_cell_counter += 1
        else:
            empty_cell_counter = 0  # Сброс счетчика, если ячейка не пустая
            sequence.append(cell_ref)

        # Переход к следующей ячейке в любом случае
        if mode == "col":
            current_row += 1
        elif mode == "row":
            current_col = next_col(current_col)

    return sequence

# --- Конец Извлечения информации ---


def run_automation(TOPICS_FOLDER=TOPICS_FOLDER, HOMEWORK_FOLDER=HOMEWORK_FOLDER):
    # --- Разделение файлов, при необходимости ---
    # print(TOPICS_FOLDER, HOMEWORK_FOLDER)
    if (TOPICS_FOLDER == HOMEWORK_FOLDER):
        print("Разделение файлов тем и домашних заданий...")
        topic_keywords = ["кл", "лек", "урок"]
        homework_keywords = ["дз", "дом"]

        all_files = os.listdir(TOPICS_FOLDER)
        topic_files = extract_files(TOPICS_FOLDER, True, topic_keywords)
        all_files = [f for f in all_files if f not in topic_files]
        homework_files = extract_files(TOPICS_FOLDER, True, homework_keywords)
        all_files = [f for f in all_files if f not in homework_files]
        if len(all_files) > 0:
            print(f"Остались нераспределенные файлы в папке '{TOPICS_FOLDER}': {all_files}")
            print("(?) Просто добавьте ключевые слова в имена оставшихся файлов и перезапустите скрипт.")
            print(f"\n(?) --- Ключевые слова ---")
            print(f"(?) Для классных работа: {topic_keywords}")
            print(f"(?) Для домашних заданий: {homework_keywords}\n")
            
            print("(?) Если вы хотите продолжить так, подождите 5 секунд. Иначе - закойроте окно\n")
            time.sleep(5)

        ALL_FOLDER = TOPICS_FOLDER
        TOPICS_FOLDER = os.path.join(os.path.dirname(ALL_FOLDER), "КЛ")
        HOMEWORK_FOLDER = os.path.join(os.path.dirname(ALL_FOLDER), "ДЗ")
        os.makedirs(TOPICS_FOLDER, exist_ok=True)
        os.makedirs(HOMEWORK_FOLDER, exist_ok=True)
        # Move files to respective folders
        for file in topic_files:
            os.rename(os.path.join(ALL_FOLDER, file), os.path.join(TOPICS_FOLDER, file))
        for file in homework_files:
            os.rename(os.path.join(ALL_FOLDER, file), os.path.join(HOMEWORK_FOLDER, file))
        if (os.listdir(ALL_FOLDER) == []):
            os.rmdir(ALL_FOLDER)  # Remove the original folder if empty
            print(f"Файлы успешно разделены на папки '{TOPICS_FOLDER}' и '{HOMEWORK_FOLDER}'.")
        # else:
        #     print(f"[КРИТИЧЕСКАЯ ОШИБКА] Не удалось полностью разделить файлы. Проверьте папку '{ALL_FOLDER}'.")
        #     print("(?) Просто распределите оставшиеся файлы вручную и перезапустите скрипт.")
        #     exit(0)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Установите True для запуска в фоновом режиме.
        page = browser.new_page()

        print(f"Переход на страницу входа...")
        page.goto(ONE_ID_LOGIN_URL)

        # --- Вход в систему ---
        print("Выполняется вход...")
        page.locator(ONE_ID_BUTTON_SELECTOR).click()

        page.get_by_placeholder(LOGIN_FIELD_PLACEHOLDER).fill(login)
        page.get_by_placeholder(PASSWORD_FIELD_PLACEHOLDER).fill(password)
        page.get_by_text(LOGIN_BUTTON_TEXT).first.click()

        page.wait_for_url(SUCCESS_URL)

        print("Вход выполнен успешно!")


        # --- Подготовка данных ---
        print("Подготовка данных из Excel...")
        df = pd.read_excel(TOPICS_FILE_PATH, header=None)
        start_cell = START_CELL
        mode = MODE
        cell_sequence = generate_sequence(df, start_cell, mode)
        values = [str(get_cell_value(df, cell_ref)).strip() for cell_ref in cell_sequence]
        print(f"Извлечено {len(values)} записей из Excel.")
        
        # print(HOMEWORK_FOLDER, TOPICS_FOLDER)


        # --- Автоматизация ---
        print("Запуск автоматизации... \n(?) Нажмите Ctrl+C в терминале, чтобы остановить.")
        page.goto(NEW_TOPIC_URL)
        
        if LINE_COUNT < START_FROM_LINE:
            print(f"[КРИТИЧЕСКАЯ ОШИБКА] Количество строк ({LINE_COUNT}) меньше чем начальное значение ({START_FROM_LINE}).")
            return

        actual_length = min(LINE_COUNT, len(values))
        counter = -1
        
        for i in range(START_FROM_LINE - 1, actual_length):
            counter += 1
            print(f"\n--- Обработка строки {i + 1} из {actual_length} ---")

            topic_name = values[i]
            check_for = str(i+1)

            # Динамический поиск файлов темы и домашнего задания
            # print(f"Поиск файла темы, начинающегося с: '{check_for}' в папке '{TOPICS_FOLDER}'")
            topic_file_path = find_file_by_prefix(TOPICS_FOLDER, check_for)
            homework_file_path = find_file_by_prefix(HOMEWORK_FOLDER, check_for)

            if not topic_file_path: print(f"   - Файл темы отсутствует в папке '{TOPICS_FOLDER}'")
            if not homework_file_path: print(f"   - Файл домашнего задания отсутствует в папке '{HOMEWORK_FOLDER}'")

            try:
                # time.sleep(3)
                print("Нажатие 'Добавить строку'...")
                page.locator(ADD_LINE_BUTTON).click()
                time.sleep(0.01)

                if topic_name is None:
                    print("[КРИТИЧЕСКАЯ ОШИБКА] Имя темы не определено. Что-то пошло не так.")
                    exit(1)

                print(f"Заполнение названия темы: '{topic_name}'")
                page.locator(f"{topics}{1000+counter}{TOPIC_NAME}").fill(topic_name)

                if topic_file_path is not None:
                    print(f"Загрузка файла темы: {topic_file_path}")
                    page.locator(f"{topics}{1000+counter}{TOPIC_FILE}").set_input_files(topic_file_path)

                if homework_file_path is not None:
                    print(f"Загрузка файла домашнего задания: {homework_file_path}")
                    page.locator(f"{topics}{1000+counter}{HOMEWORK_FILE}").set_input_files(homework_file_path)

            except Exception as e:
                print(f"[КРИТИЧЕСКАЯ ОШИБКА] на строке {counter + 1}: {e}")
                print("Сохранение скриншота ошибки.")
                page.screenshot(path="error_screenshot.png")
                break

        print("\n--- Автоматизация завершена! ---")
        time.sleep(3)
        print("\n\n\n(?) Теперь вы можете взаимодействовать с браузером. Скрипт завершится после закрытия браузера.\n\n\n")

        # Приостанавливает выполнение скрипта до тех пор, пока пользователь не закроет страницу.
        while True:
            try:
                page.wait_for_event("close", 999999)
            except Exception:
                continue
            print("Браузер закрыт. Завершение скрипта.")
            time.sleep(3)
            exit(0)

        # time.sleep(999999)



if __name__ == "__main__":
    try:
        run_automation()
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] Необработанное исключение: {e}")
        time.sleep(999999)
