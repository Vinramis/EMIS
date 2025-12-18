
import time
import sys

try:
    from playwright.sync_api import sync_playwright
    from config_manager import ConfigManager
    import file_utils
    import excel_utils
except ImportError as e:
    print(f"[КРИТИЧЕСКАЯ ОШИБКА] Не удалось импортировать модули: {e}")
    print("(?) Кажется, вы запустили программу неправильно. Попробуйте заново.")
    sys.exit(1)

def run_automation():
    # 1. Загрузка конфигурации
    cfg = ConfigManager()

    # 2. Организация файлов
    cfg.TOPICS_FOLDER, cfg.HOMEWORK_FOLDER = file_utils.organize_files(cfg.TOPICS_FOLDER, cfg.HOMEWORK_FOLDER)

    # 3. Автоматизация браузера
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        page = browser.new_page()

        print(f"Переход на страницу входа...")
        page.goto(cfg.ONE_ID_LOGIN_URL)

        # Вход
        print("Выполняется вход...")
        try:
            page.locator(cfg.ONE_ID_BUTTON_SELECTOR).click()
            page.get_by_placeholder(cfg.LOGIN_FIELD_PLACEHOLDER).fill(cfg.LOGIN)
            page.get_by_placeholder(cfg.PASSWORD_FIELD_PLACEHOLDER).fill(cfg.PASSWORD)
            # Click the first matching login button
            page.get_by_text(cfg.LOGIN_BUTTON_TEXT).first.click()
            
            page.wait_for_url(cfg.SUCCESS_URL)
            print("Вход выполнен успешно!")
        except Exception as e:
            print(f"[ОШИБКА] Вход не удался: {e}")
            return

        # 4. Подготовка данных
        print("Подготовка данных из Excel...")
        topic_names = excel_utils.read_topics_from_excel(
            cfg.TOPICS_FILE_PATH, 
            cfg.START_CELL, 
            cfg.MODE
        )
        print(f"Извлечено {len(topic_names)} записей из Excel.")

        # 5. Цикл автоматизации
        print("Запуск автоматизации... \n(?) Нажмите Ctrl+C в терминале, чтобы остановить.")
        page.goto(cfg.NEW_TOPIC_URL)

        if cfg.LINE_COUNT < cfg.START_FROM_LINE:
            print(f"[КРИТИЧЕСКАЯ ОШИБКА] Количество строк ({cfg.LINE_COUNT}) меньше чем начальное значение ({cfg.START_FROM_LINE}).")
            return

        actual_length = min(cfg.LINE_COUNT, len(topic_names))
        
        counter = -1
        
        for topic_number in range(cfg.START_FROM_LINE, actual_length + 1):
            counter += 1
            print(f"\n--- Обработка строки {topic_number} из {actual_length} ---")

            topic_name = topic_names[topic_number - 1]

            # Поиск файлов
            topic_file_path = file_utils.find_file_by_count(cfg.TOPICS_FOLDER, topic_number)
            homework_file_path = file_utils.find_file_by_count(cfg.HOMEWORK_FOLDER, topic_number)

            if not topic_file_path: 
                print(f"[ОШИБКА] Файл темы отсутствует в папке '{cfg.TOPICS_FOLDER}'")
            if not homework_file_path: 
                print(f"[ОШИБКА] Файл домашнего задания отсутствует в папке '{cfg.HOMEWORK_FOLDER}'")

            try:
                print("Нажатие 'Добавить строку'...")
                page.locator(cfg.ADD_LINE_BUTTON).click()
                time.sleep(0.01)

                if not topic_name:
                    print("[КРИТИЧЕСКАЯ ОШИБКА] Имя темы не определено.")
                    sys.exit(1)

                print(f"Заполнение названия темы: '{topic_name}'")
                page.locator(f"{cfg.TOPICS_PREFIX}{1000+counter}{cfg.TOPIC_NAME_SUFFIX}").fill(topic_name)

                if topic_file_path:
                    print(f"Загрузка файла темы: {topic_file_path}")
                    page.locator(f"{cfg.TOPICS_PREFIX}{1000+counter}{cfg.TOPIC_FILE_SUFFIX}").set_input_files(topic_file_path)

                if homework_file_path:
                    print(f"Загрузка файла домашнего задания: {homework_file_path}")
                    page.locator(f"{cfg.TOPICS_PREFIX}{1000+counter}{cfg.HOMEWORK_FILE_SUFFIX}").set_input_files(homework_file_path)

            except Exception as e:
                print(f"[КРИТИЧЕСКАЯ ОШИБКА] на строке {counter + 1} (Элемент {topic_number}): {e}")
                print("Сохранение скриншота ошибки.")
                page.screenshot(path="error_screenshot.png")
                break

        print("\n--- Автоматизация завершена! ---")
        print("\n\n\n(?) Теперь вы можете взаимодействовать с браузером. Скрипт завершится после закрытия браузера.\n\n\n")

        # Ожидание закрытия браузера пользователем
        while True:
            try:
                if page.is_closed():
                    break
                page.wait_for_event("close", timeout=1000)
            except Exception:
                if page.is_closed():
                    break
                continue
        
        print("Браузер закрыт. Завершение скрипта.\n")
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print("\nОстановлено пользователем.")
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] Необработанное исключение: {e}")
        time.sleep(10)
