import time
import pathlib
import openpyxl
from playwright.sync_api import sync_playwright, Browser, Page
from config_manager import JsonTwin
import file_utils
import excel_utils

import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))


def run_automation(headless: bool = False):
    # 1. Загрузка конфигурации
    input_data_json: JsonTwin = JsonTwin("input_data.json")
    selectors: JsonTwin = JsonTwin("web.json").get("constants")

    print("\nВводимые данные будут выведены в формате:")
    print("Номер строки, номер темы. 'Название темы'")
    print("Файл классной работы")
    print("Файл домашнего задания\n")


    # 3. Автоматизация браузера
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=headless).new_context(
            storage_state="cookies.json", no_viewport=True
        )
        page: Page = browser.new_page()

        # 5. Цикл автоматизации
        print("--- Запуск автоматизации ---")
        page.goto(selectors.get("new_topic_url"))

        counter = -1
        for topic_material in input_data_json.get():
            topic_material = JsonTwin(topic_material)
            counter += 1
            # print(f"\n--- Обработка строки {counter + 1} из {len(input_data_json.get())} ---")

            topic_number = topic_material("topic_number")
            topic_name = topic_material("topic_name")
            topic_file_path = topic_material("classwork_file_path")
            homework_file_path = topic_material("homework_file_path")

            topic_name_selector = f"{selectors.get('prefix')}{1000 + counter}{selectors.get('topic_name_postfix')}"
            topic_file_selector = f"{selectors.get('prefix')}{1000 + counter}{selectors.get('topic_file_postfix')}"
            homework_file_selector = f"{selectors.get('prefix')}{1000 + counter}{selectors.get('homework_file_postfix')}"

            try:
                page.locator(selectors.get("add_line_button")).click()
                time.sleep(0.1)

                print(f"\n{counter + 1}, {topic_number}. '{topic_name}'")
                page.locator(topic_name_selector).fill(topic_name)

                print(f"{file_utils.pure_name(topic_file_path)}")
                page.locator(topic_file_selector).set_input_files(topic_file_path)

                print(f"{file_utils.pure_name(homework_file_path)}")
                page.locator(homework_file_selector).set_input_files(homework_file_path)

            except Exception as e:
                print(
                    f"[КРИТИЧЕСКАЯ ОШИБКА] на строке {counter + 1} (Номер темы - {topic_number}): {e}"
                )

        print("\n--- Автоматизация завершена! ---")
        print(
            "\n\n(?) Теперь вы можете взаимодействовать с браузером. Не закрывайте это окно!\n\n"
        )

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


def fill_line(
    page: Page,
    counter: int,
    resources: JsonTwin = JsonTwin("input_data.json"),
    web_json: JsonTwin = JsonTwin("web.json"),
):
    topic_selector: str = (
        f"{web_json('prefix')}{1000 + counter}{web_json('topic_name_postfix')}"
    )
    topic_file_selector: str = (
        f"{web_json('prefix')}{1000 + counter}{web_json('topic_file_postfix')}"
    )
    homework_file_selector: str = (
        f"{web_json('prefix')}{1000 + counter}{web_json('homework_file_postfix')}"
    )
    add_line_button: str = web_json("add_line_button")

    topic_name: str = resources("topic_name")
    topic_file: str = resources("topic_file")
    homework_file: str = resources("homework_file")

    try:
        page.locator(add_line_button).click()
        page.locator(topic_selector).fill(topic_name)
        if topic_file and topic_file != "":
            page.locator(topic_file_selector).set_input_files(topic_file)
        if homework_file and homework_file != "":
            page.locator(homework_file_selector).set_input_files(homework_file)
    except Exception as e:
        print(f"[ОШИБКА] Возникла ошибка при заполнении строки: {e}")
        time.sleep(1)


if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print("\n\nВы остановили программу. Можно закрыть это окно.\n\n")
        time.sleep(999)
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] {e}")
        time.sleep(1)
