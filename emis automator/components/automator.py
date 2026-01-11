import time
import colorama
from playwright.sync_api import sync_playwright, Browser, Page
from config_manager import JsonTwin
import file_utils

import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))


def run_automation(headless: bool = False):
    print("\nВводимые данные будут выведены в формате:")
    print(
        "Номер строки, номер темы. 'Название темы', 'Файл классной работы', 'Файл домашнего задания'"
    )

    # 1. Загрузка конфигурации
    input_data_json: JsonTwin = JsonTwin("input_data.json")
    selectors: JsonTwin = JsonTwin("web.json").get("constants")

    # 2. Автоматизация браузера
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=headless).new_context(
            storage_state="cookies.json", no_viewport=True
        )
        page: Page = browser.new_page()

        # 3. Цикл автоматизации
        print("\n--- Запуск автоматизации ---\n")

        page.goto(selectors.get("all_topics_url"))
        page.goto(selectors.get("new_topic_url"))

        add_line_button = selectors.get("add_line_button")
        prefix = selectors.get("prefix")
        topic_name_postfix = selectors.get("topic_name_postfix")
        topic_file_postfix = selectors.get("topic_file_postfix")
        homework_file_postfix = selectors.get("homework_file_postfix")

        max_topic_name_length = 0
        max_topic_file_length = 0
        max_homework_file_length = 0
        for topic_material in input_data_json.get():
            topic_material = JsonTwin(topic_material)

            if (
                max_topic_name_length > 40
                and max_topic_file_length > 40
                and max_homework_file_length > 40
            ):
                max_topic_name_length = 40
                max_topic_file_length = 40
                max_homework_file_length = 40
                break

            max_topic_name_length = max(
                max_topic_name_length, len(topic_material("topic_name"))
            )
            max_topic_file_length = max(
                max_topic_file_length,
                len(file_utils.pure_name(topic_material("classwork_file_path"))),
            )
            max_homework_file_length = max(
                max_homework_file_length,
                len(file_utils.pure_name(topic_material("homework_file_path"))),
            )

        counter = -1
        for topic_material in input_data_json.get():
            topic_material = JsonTwin(topic_material)
            counter += 1

            topic_number = topic_material("topic_number")
            topic_name = topic_material("topic_name")
            topic_file_path = topic_material("classwork_file_path")
            homework_file_path = topic_material("homework_file_path")

            topic_name_selector = f"{prefix}{1000 + counter}{topic_name_postfix}"
            topic_file_selector = f"{prefix}{1000 + counter}{topic_file_postfix}"
            homework_file_selector = f"{prefix}{1000 + counter}{homework_file_postfix}"

            success_count = 0
            error_count = 0
            if fill_line(
                page=page,
                add_line_button=add_line_button,
                topic_selector=topic_name_selector,
                topic_file_selector=topic_file_selector,
                homework_file_selector=homework_file_selector,
                counter=counter,
                topic_number=topic_number,
                topic_name=topic_name,
                topic_file=topic_file_path,
                homework_file=homework_file_path,
            ):
                print_line(
                    counter=counter,
                    topic_material=topic_material,
                    cut_to_length=[
                        max_topic_name_length,
                        max_topic_file_length,
                        max_homework_file_length,
                    ],
                )
                success_count += 1
            else:
                error_count += 1
                if error_count > success_count + 5:
                    raise Exception("Проблемы при заполнении данных")

            # try:
            #     page.locator(add_line_button).click()
            #     # time.sleep(0.2)

            #     print(f"\n{counter + 1}, {topic_number}. '{topic_name}'")
            #     page.locator(topic_name_selector).fill(topic_name)

            #     print(f"{file_utils.pure_name(topic_file_path)}")
            #     page.locator(topic_file_selector).set_input_files(topic_file_path)

            #     print(f"{file_utils.pure_name(homework_file_path)}")
            #     page.locator(homework_file_selector).set_input_files(homework_file_path)

            # except Exception as e:
            #     print(f"Проблема заполнения на строке {counter + 1} (Номер темы - {topic_number}): {e}")

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


def print_line(
    counter: int,
    topic_material: JsonTwin,
    *,
    beautify: bool = True,
    cut_to_length: tuple[int, int, int] = (40, 40, 40),
):
    from data_utils import cut_string

    topic_number: int | str = topic_material("topic_number")
    cut_topic_name: str = cut_string(
        topic_material("topic_name"), to_length=cut_to_length[0]
    )
    cut_topic_file_path: str = cut_string(
        file_utils.pure_name(topic_material("classwork_file_path")),
        to_length=cut_to_length[1],
    )
    cut_homework_file_path: str = cut_string(
        file_utils.pure_name(topic_material("homework_file_path")),
        to_length=cut_to_length[2],
    )

    if beautify:
        name_extender = (
            " " * (cut_to_length[0] - len(cut_topic_name))
            if len(cut_topic_name) < cut_to_length[0]
            else " "
        )
        classwork_extender = (
            " " * (cut_to_length[1] - len(cut_topic_file_path))
            if len(cut_topic_file_path) < cut_to_length[1]
            else " "
        )
        # homework_extender = (
        #     " " * (cut_to_length[2] - len(cut_homework_file_path))
        #     if len(cut_homework_file_path) < cut_to_length[2]
        #     else " "
        # )
        print(
            f"Строка {counter + 1}, тема {topic_number}. '{cut_topic_name}',{name_extender}'{cut_topic_file_path}',{classwork_extender}'{cut_homework_file_path}'"
        )
    else:
        print(
            f"Строка {counter + 1}, тема {topic_number}. '{cut_topic_name}', '{cut_topic_file_path}', '{cut_homework_file_path}'"
        )


def fill_line(
    page: Page,
    add_line_button: str,
    topic_selector: str,
    topic_file_selector: str,
    homework_file_selector: str,
    counter: int,
    topic_number: int | str,
    topic_name: str,
    topic_file: str,
    homework_file: str,
) -> bool:
    no_error: bool = True
    page.click(add_line_button)

    try:
        page.set_input_files(topic_file_selector, topic_file)
    except Exception:
        no_error = False
        print(
            f"{colorama.Fore.RED}Проблема заполнения классной работы на строке {counter + 1} (Номер темы - {topic_number}){colorama.Style.RESET_ALL}"
        )
    try:
        page.set_input_files(homework_file_selector, homework_file)
    except Exception:
        no_error = False
        print(
            f"{colorama.Fore.RED}Проблема заполнения домашнего задания на строке {counter + 1} (Номер темы - {topic_number}){colorama.Style.RESET_ALL}"
        )
    page.fill(topic_selector, topic_name)

    return no_error


if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        input("\n\nВы остановили программу. Можно закрыть это окно.\n\n")
        # time.sleep(999)
        exit()
    except Exception as e:
        print(f"{colorama.Fore.RED}[КРИТИЧЕСКАЯ ОШИБКА] {e}{colorama.Style.RESET_ALL}")
        time.sleep(1)
