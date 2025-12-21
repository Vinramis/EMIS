import time
import sys

try:
    from playwright.sync_api import sync_playwright
    from config_manager import ConfigManager
    import file_utils
    import excel_utils
except Exception as e:
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
        time.sleep(0.2)

        print("Переход на страницу входа...")
        page.goto(cfg.ONE_ID_LOGIN_URL)
        time.sleep(0.2)

        # Вход
        print("Выполняется вход...")
        try:
            page.locator(cfg.ONE_ID_BUTTON_SELECTOR).click()
            time.sleep(0.1)
            page.get_by_placeholder(cfg.LOGIN_FIELD_PLACEHOLDER).fill(cfg.LOGIN)
            page.get_by_placeholder(cfg.PASSWORD_FIELD_PLACEHOLDER).fill(cfg.PASSWORD)
            time.sleep(0.1)
            page.get_by_text(cfg.LOGIN_BUTTON_TEXT).first.click()
            page.wait_for_url(cfg.SUCCESS_URL)
            print("Вход выполнен успешно!")
        except Exception as e:
            print(f"[ОШИБКА] Вход не удался: {e}")
            return

        # 4. Подготовка данных
        print("Подготовка данных из Excel...")
        file_utils.rename_single_excel()
        topic_names = excel_utils.read_topics_from_excel(cfg.TOPICS_FILE_PATH, cfg.START_CELL, cfg.MODE)
        time.sleep(0.5)
        print(f"Извлечено {len(topic_names)} записей из Excel.")
        time.sleep(0.5)

        # 5. Цикл автоматизации
        print("Запуск автоматизации...")
        page.goto(cfg.NEW_TOPIC_URL)

        actual_length = cfg.END_ON_LINE - cfg.START_FROM_LINE
        counter = -1

        for current_topic_number in range(cfg.START_FROM_LINE, cfg.END_ON_LINE + 1):
            counter += 1
            print(f"\n--- Обработка строки {counter + 1} из {actual_length} ---") # Counter + 1 because first element will be 1 AND we need to count which actual line we are on

            topic_name = topic_names[current_topic_number - 1] # current_topic_number and not counter, because topic_names contains all topics, not only which we need to fill

            # Поиск файлов
            topic_file_path = file_utils.find_file_by_count(cfg.TOPICS_FOLDER, current_topic_number)
            homework_file_path = file_utils.find_file_by_count(cfg.HOMEWORK_FOLDER, current_topic_number)

            if not topic_file_path:
                print(f"[ОШИБКА] Файл классной работы отсутствует в папке '{cfg.TOPICS_FOLDER}'")
            if not homework_file_path:
                print(f"[ОШИБКА] Файл домашнего задания отсутствует в папке '{cfg.HOMEWORK_FOLDER}'")

            try:
                print("Нажатие 'Добавить строку'...")
                page.locator(cfg.ADD_LINE_BUTTON).click()
                time.sleep(0.1)

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
                print(f"[КРИТИЧЕСКАЯ ОШИБКА] на строке {counter + 1} (Элемент {current_topic_number}): {e}")
                print("Сохранение скриншота ошибки.")
                page.screenshot(path="error_screenshot.png")
                break

        print("\n--- Автоматизация завершена! ---")
        print("\n\n(?) Теперь вы можете взаимодействовать с браузером. Не закрывайте это окно!\n\n")

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

        time.sleep(1)

if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print("\n\nВы остановили программу. Можно закрыть это окно.\n\n")
        time.sleep(999)
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] Необработанное исключение: {e}")
        time.sleep(1)
