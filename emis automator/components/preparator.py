import time
import os
import sys
from pathlib import Path

import openpyxl
from playwright.sync_api import sync_playwright, Browser, Page

import excel_utils
import file_utils
from file_utils import normalize_path

# from excel_utils import extract_topics
from data_utils import numbers_in_string
from config_manager import JsonTwin

# This script is used to prepare everything for smooth work of the main script.

# It does the following:
# 1. Checks if config.json exists and is valid, if not, creates/rewrites it.
# 2. Checks topics numbers interval.
# 3. Creates/Rewrites a config.db file. (containing all topic names and file paths)
# 4.


os.chdir(os.path.dirname(sys.argv[0]))


# Testing
test_mode = False


def test():
    configure_input_data(
        config_json=JsonTwin("config.json"), input_data_json=JsonTwin("input_data.json")
    )


def main():
    # Load all configurations
    default_json: JsonTwin = JsonTwin("default.json")

    cookies_json: JsonTwin = JsonTwin("cookies.json")
    credentials_json: JsonTwin = JsonTwin("credentials.json")
    config_json: JsonTwin = JsonTwin("config.json")
    input_data_json: JsonTwin = JsonTwin("input_data.json")
    web_json: JsonTwin = JsonTwin("web.json")

    headless = True
    if "--not-headless" in sys.argv:
        headless = False

    if len(sys.argv) > 1:
        if "--login" in sys.argv:
            ensure_login(headless=headless)
    else:
        # Ensure config.json is valid
        ensure_json_validity(config_json, default_json("config.json"))

        # Configure input_data.json
        configure_input_data(
            config_json=config_json,
            input_data_json=input_data_json,
        )

        # Ensure login
        ensure_login(
            cookies_json=cookies_json,
            credentials_json=credentials_json,
            web_json=web_json,
            headless=headless,
        )

        # # Ensure input_data.json is valid
        # ensure_json_validity(input_data_json, default_json, "input_data.json")

        # # Ensure web.json is valid
        # ensure_json_validity(web_json, default_json, "web.json")


def ask_credentials() -> tuple[str, str]:
    login: str = input("Введите ваш логин EMIS: ")
    password: str = input("Введите ваш пароль EMIS: ")
    return login, password


def ask_topics_interval() -> tuple[int, int]:
    start_topic: int = numbers_in_string(input("Введите номер первой темы: "))[0]
    end_topic: int = numbers_in_string(input("Введите номер последней темы: "))[0]
    print(f"Выбраны темы от {start_topic} до {end_topic}.")
    return start_topic, end_topic


def configure_input_data(
    config_json: JsonTwin = JsonTwin("config.json"),
    input_data_json: JsonTwin = JsonTwin("input_data.json"),
) -> None:
    """
    Configures input_data_json, using config_json as a reference.
    """
    # topics_file_path: str = normalize_path(config_json("topics_file_path"))
    start_cell: str = config_json("start_cell")
    mode: str = config_json("mode")
    classwork_folder: str = config_json("classwork_folder")
    homework_folder: str = config_json("homework_folder")

    classwork_interval: tuple[int, int] = file_utils.get_numerical_interval(
        classwork_folder
    )
    homework_interval: tuple[int, int] = file_utils.get_numerical_interval(
        homework_folder
    )
    start_from_line: int = min(classwork_interval[0], homework_interval[0])
    end_on_line: int = max(classwork_interval[1], homework_interval[1])
    print(f"Выбраны темы от {start_from_line} до {end_on_line}.")

    # config_json["start_from_line"] = start_from_line
    # config_json["end_on_line"] = end_on_line

    # Try to get topics from topics_file_path
    try:
        topics_sheet = openpyxl.load_workbook(
            filename=normalize_path("..\\КТП.xlsx"), data_only=True
        ).active
    except Exception:
        base_directory = Path(__file__).parent
        parent_directory = Path(base_directory).parent

        topics_file_path = file_utils.find_single_excel(parent_directory)
        if topics_file_path:
            topics_sheet = openpyxl.load_workbook(
                filename=topics_file_path, data_only=True
            ).active
        else:
            print(
                f"Файл КТП не найден или не является единственным Excel файлом в {parent_directory}"
            )

    topics = excel_utils.read_topics_from_excel(
        topics_sheet,
        start_cell=start_cell,
        mode=mode,
        starting_topic_number=start_from_line,
        ending_topic_number=end_on_line,
    )

    counter = 0
    for i in range(start_from_line, end_on_line + 1):
        input_data_json[counter] = {
            "topic_number": i,
            "topic_name": topics[counter],
            "classwork_file_path": file_utils.find_file_by_count(
                config_json.get("classwork_folder"), i
            ),
            "homework_file_path": file_utils.find_file_by_count(
                config_json.get("homework_folder"), i
            ),
        }
        counter += 1


def ensure_json_validity(target_json: JsonTwin, its_default: JsonTwin) -> bool:
    """Check for it's existance and for entries. If it doesn't exist it will not pass the difference check."""
    if target_json.super_keys().difference(its_default.super_keys()):
        target_json.pull(its_default)
        return False
    return True


def get_cookies(
    login: str,
    password: str,
    configuration: JsonTwin = JsonTwin("web.json")("login"),
    headless: bool = True,
):
    c: JsonTwin = configuration
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=headless)
        page: Page = browser.new_page()
        page.goto(c("One_ID_login_url"))
        page.click(c("One_ID_button_selector"))

        page.fill(c("login_field_selector"), login)
        page.fill(c("password_field_selector"), password)
        page.click(c("login_button_selector"))
        page.wait_for_load_state("networkidle")

        if page.url != c("success_url"):
            print("Не получилось войти.")
            return None
        cookies = page.context.storage_state()
        browser.close()
        return dict(cookies)


def hard_extract(
    target_json: JsonTwin = JsonTwin("cookies.json"), key: str = "expires"
) -> str:
    """Extracts literal value from a JsonTwin"""
    data = target_json.to_string(beautiful=False)
    value_chunk = data.split(key)[1].split(",")[0]
    value = value_chunk[2:].strip()
    return value


def cookies_expired(cookies_json: JsonTwin = JsonTwin("cookies.json")) -> bool:
    """Checks if cookies are expired"""
    return int(hard_extract(cookies_json, "expires")) < time.time().__int__() + 5 * 60


def cookie_practice_check(
    cookies: Path | str = "cookies.json",
    configuration: JsonTwin = JsonTwin("web.json")("login"),
    headless: bool = True,
):
    """Practically checks if cookies are valid"""
    c: JsonTwin = configuration
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=headless).new_context(
            storage_state=cookies
        )
        page: Page = browser.new_page()
        page.goto(c("One_ID_login_url"))
        page.wait_for_load_state("networkidle")
        return_value = page.url == c("success_url")
        browser.close()
        return return_value


def ensure_login(
    cookies_json: JsonTwin = JsonTwin("cookies.json"),
    credentials_json: JsonTwin = JsonTwin("credentials.json"),
    web_json: JsonTwin = JsonTwin("web.json"),
    headless: bool = True,
    looping: int = 3,
):
    try:
        if cookies_expired(cookies_json):
            pass
        elif cookie_practice_check(
            cookies_json.file_path, web_json("login"), headless=headless
        ):
            return
    except Exception:
        print("[ИНФО] Предыдущий вход больше не работает. Заново входим в EMIS...")
    os.remove(cookies_json.file_path)

    if credentials_json("validity") == -1:
        print(
            f"[ИНФО] При предыдущем входе произошла ошибка. Введите ваши учетные данные заново. Предыдущие данные: {credentials_json('login')}, {credentials_json('password')}\n"
        )
        credentials_json["login"], credentials_json["password"] = ask_credentials()
        credentials_json.set("validity", 0)

    cookies = get_cookies(
        login=credentials_json("login"),
        password=credentials_json("password"),
        configuration=web_json("login"),
        headless=headless,
    )
    cookies_json.pull(cookies)

    if cookie_practice_check(
        cookies_json.file_path, web_json("login"), headless=headless
    ):
        credentials_json.set("validity", 1)
        return
    else:
        credentials_json.set("validity", -1)

    if looping > 0:
        ensure_login(
            cookies_json=cookies_json,
            credentials_json=credentials_json,
            web_json=web_json,
            headless=headless,
            looping=looping - 1,
        )


if __name__ == "__main__":
    test() if test_mode else main()
