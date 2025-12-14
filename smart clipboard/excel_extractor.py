import time
# import threading
import keyboard
import pyperclip
import os
import json
import sys
import pandas as pd

# --- Глобальная переменная для остановки ---
RUNNING = True

# --- Константы ---
HOTKEY_PASTE_NEXT = 'ctrl+v'
HOTKEY_STOP = 'alt+c'
MAX_EMPTY_CELLS_IN_A_ROW = 5


def load_config():
    """Загружает конфигурацию из файла, переданного в аргументах командной строки."""
    if len(sys.argv) < 2:
        print("\n[КРИТИЧЕСКАЯ ОШИБКА] Не указан файл конфигурации.")
        print("Пожалуйста, запускайте скрипт через 'СТАРТ.cmd'.")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"\n[КРИТИЧЕСКАЯ ОШИБКА] Файл конфигурации '{config_file}' не найден.")
        print("Пожалуйста, сначала запустите 'СТАРТ.cmd' для настройки.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"\n[КРИТИЧЕСКАЯ ОШИБКА] Ошибка при чтении '{config_file}' - удалите его и попробуйте снова.")
        sys.exit(1)


# Вспомогательная функция для инкрементации столбцов
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
            empty_cell_counter = 0  # Сброс счетчика, если ячейка не пуста
            sequence.append(cell_ref)

        # Переход к следующей ячейке в любом случае
        if mode == "col":
            current_row += 1
        elif mode == "row":
            current_col = next_col(current_col)
            
    return sequence


# --- Функция остановки ---
def stop_script():
    """Останавливает выполнение скрипта."""
    global RUNNING
    print("\n[СТОП] Нажата Alt+C. Интеллектуальный буфер обмена останавливается...")
    RUNNING = False
    keyboard.unhook_all()


class ClipboardManager:
    """Управляет состоянием буфера обмена и последовательностью."""
    def __init__(self, values_to_copy):
        self.values = values_to_copy
        self.index = -1

    def update_clipboard(self):
        """Копирует следующее значение в буфер обмена и симулирует вставку."""
        global RUNNING
        if not RUNNING:
            return

        self.index += 1

        if self.index < len(self.values):
            value_to_copy = self.values[self.index]
            pyperclip.copy(value_to_copy)
            print(f"Скопировано: {value_to_copy}")

            time.sleep(0.05)  # Небольшая задержка для стабильности
            keyboard.press_and_release(HOTKEY_PASTE_NEXT)
        else:
            print("\nПоследовательность завершена. Интеллектуальный буфер обмена останавливается...")
            stop_script()


def main():
    """Основная функция выполнения скрипта."""
    global RUNNING, MODE
    
    config = load_config()
    EXCEL_FILE = config['excel_file']
    START_CELL = config['start_cell']
    MODE = config.get('mode', "col")
    SHEET_NAME = config.get('sheet_name', 0)

    try:
        print(f"[ИНФО] Попытка загрузить файл Excel: {EXCEL_FILE}")
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, header=None)
    except FileNotFoundError:
        print(f"\n[КРИТИЧЕСКАЯ ОШИБКА] Файл Excel '{EXCEL_FILE}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[КРИТИЧЕСКАЯ ОШИБКА] Произошла ошибка при загрузке файла Excel: {e}")
        sys.exit(1)

    sequence_refs = generate_sequence(df, START_CELL, MODE)
    
    if not sequence_refs:
        print("\n[ИНФО] Начальная ячейка или последовательность пуста. Нечего копировать.")
        sys.exit(0)

    values_to_copy = [str(get_cell_value(df, ref)) for ref in sequence_refs]
    manager = ClipboardManager(values_to_copy)

    # Запуск прослушивания горячих клавиш
    keyboard.add_hotkey(HOTKEY_PASTE_NEXT, manager.update_clipboard, suppress=True)
    keyboard.add_hotkey(HOTKEY_STOP, stop_script, suppress=True)

    mode_str = 'По Столбцу' if MODE == 'col' else 'По Строке'
    print(f"\nИнтеллектуальный буфер обмена запущен (Файл: {os.path.basename(EXCEL_FILE)}, Ячейка: {START_CELL}, Режим: {mode_str}).")
    print(f"  - Горячая клавиша (Копировать и вставить далее): '{HOTKEY_PASTE_NEXT.upper()}'")
    print(f"  - Горячая клавиша (Остановить скрипт): '{HOTKEY_STOP.upper()}'")
    print(f"Длина последовательности: {len(values_to_copy)} ячеек")

    try:
        while RUNNING:
            time.sleep(0.5)
        print("Скрипт успешно завершен.")
    except KeyboardInterrupt:
        print("\nСкрипт прерван пользователем.")
    finally:
        keyboard.unhook_all()

if __name__ == "__main__":
    main()