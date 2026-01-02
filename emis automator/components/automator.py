import time
import sys
import pathlib

try:
    import openpyxl
    from playwright.sync_api import sync_playwright
    from config_manager import JsonTwin
    import file_utils
    import excel_utils
except Exception as e:
    print(f"[КРИТИЧЕСКАЯ ОШИБКА] Не удалось импортировать модули: {e}")
    print("(?) Кажется, вы запустили программу неправильно. Попробуйте заново.")
    pause = input("Нажмите Enter...")
    sys.exit(1)

def run_automation(silent: bool = False):
    # 1. Загрузка конфигурации
    cfg: JsonTwin = JsonTwin("config.json")
    autorisation: JsonTwin = cfg.get("credentials")
    settings: JsonTwin = cfg.get("settings")

    selectors = JsonTwin("web.json").get("constants")


    # 2. Определение наибольшего интервала
    classwork_interval: tuple[int, int] = file_utils.get_numerical_interval(settings.get("classwork_folder"))
    homework_interval: tuple[int, int] = file_utils.get_numerical_interval(settings.get("homework_folder"))
    settings["start_from_line"] = min(classwork_interval[0], homework_interval[0])
    settings["end_on_line"] = max(classwork_interval[1], homework_interval[1])

    # 3. Автоматизация браузера
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=silent)
        try:
            browser = browser.new_context(storage_state="access.json")
        except Exception:
            print("[ОШИБКА] Не удалось загрузить данные авторизации.")

        page = browser.new_page()

        time.sleep(0.2)

        print("Переход на страницу входа...")
        page.goto(selectors.get("One_ID_login_url"))
        time.sleep(0.2)

        # Вход
        print("Выполняется вход...")
        page.locator(selectors("One_ID_button_selector")).click()
        time.sleep(0.1)
        page.get_by_placeholder(selectors("login_field_placeholder")).fill(autorisation("login"))
        page.get_by_placeholder(selectors("password_field_placeholder")).fill(autorisation("password"))
        time.sleep(0.1)
        page.get_by_text(selectors("login_button_text")).first.click()
        try:
            page.wait_for_url(selectors("success_url"))
            print("Вход выполнен успешно!")
            page.context.storage_state(path="access.json")
        except Exception as e:
            print(f"[ОШИБКА] Вход не удался: {e}")
            autorisation["validity"] = -1
            return

        # 4. Подготовка данных
        print("Подготовка данных из Excel...")
        if not pathlib.Path(file_utils.normalize_path(settings.get("topics_file_path"))).is_file():
            base_directory = pathlib.Path(__file__).parent
            parent_directory = pathlib.Path(base_directory).parent

            file_utils.rename_single_excel(parent_directory)

        sheet = openpyxl.load_workbook(settings.get("topics_file_path")).active
        topic_names = excel_utils.read_topics_from_excel(sheet, settings.get("start_cell"), settings.get("mode"), settings.get("start_from_line"), settings.get("end_on_line"))
        time.sleep(0.5)
        print(f"Извлечено {len(topic_names)} записей из Excel.")
        time.sleep(0.5)

        # 5. Цикл автоматизации
        print("Запуск автоматизации...")
        page.goto(selectors.get("new_topic_url"))

        actual_length = settings.get("end_on_line") - settings.get("start_from_line") + 1
        counter = -1

        for current_topic_number in range(settings.get("start_from_line"), settings.get("end_on_line") + 1):
            counter += 1
            print(f"\n--- Обработка строки {counter + 1} из {actual_length} ---") # Counter + 1 because first element will be 1 AND we need to count which actual line we are on

            topic_name = topic_names[current_topic_number - 1] # current_topic_number and not counter, because topic_names contains all topics, not only which we need to fill
            topic_name_selector = selectors.get("prefix") + str(1000+counter) + selectors.get("topic_name_postfix")
            topic_file_selector = selectors.get("prefix") + str(1000+counter) + selectors.get("topic_file_postfix")
            homework_file_selector = selectors.get("prefix") + str(1000+counter) + selectors.get("homework_file_postfix")

            # Поиск файлов
            topic_file_path = file_utils.find_file_by_count(settings.get("classwork_folder"), current_topic_number)
            homework_file_path = file_utils.find_file_by_count(settings.get("homework_folder"), current_topic_number)

            if not topic_file_path:
                print(f"[ОШИБКА] Файл классной работы отсутствует в папке '{settings.get("classwork_folder")}'")
            if not homework_file_path:
                print(f"[ОШИБКА] Файл домашнего задания отсутствует в папке '{settings.get("homework_folder")}'")

            try:
                print("Нажатие 'Добавить строку'...")
                page.locator(selectors.get("add_line_button")).click()
                time.sleep(0.1)

                if not topic_name:
                    print("[КРИТИЧЕСКАЯ ОШИБКА] Имя темы не определено.")
                    sys.exit(1)

                print(f"Заполнение названия темы: '{topic_name}'")
                page.locator(topic_name_selector).fill(topic_name)

                if topic_file_path:
                    print(f"Загрузка файла темы: {topic_file_path}")
                    page.locator(topic_file_selector).set_input_files(topic_file_path)

                if homework_file_path:
                    print(f"Загрузка файла домашнего задания: {homework_file_path}")
                    page.locator(homework_file_selector).set_input_files(homework_file_path)

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
                page.wait_for_event("close")
            except Exception:
                if page.is_closed():
                    break
                continue

        # time.sleep(1)

if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print("\n\nВы остановили программу. Можно закрыть это окно.\n\n")
        time.sleep(999)
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] Необработанное исключение: {e}")
        time.sleep(1)
