import time
import os
import sys
import json
import pathlib
from pathlib import Path

import openpyxl
from playwright.sync_api import sync_playwright, Browser, Page

from file_utils import normalize_path
from excel_utils import *
from data_utils import numbers_in_string
from config_manager import JsonTwin
# from automator import run_automation

# This script is used to prepare everything for smooth work of the main script.

# It does the following:
# 1. Checks if config.json exists and is valid, if not, creates/rewrites it.
# 2. Checks topics numbers interval.
# 3. Creates/Rewrites a config.db file. (containing all topic names and file paths)
# 4.


def main():
    # Load all configurations
    default_json: JsonTwin = JsonTwin("default.json")

    cookies_json: JsonTwin = JsonTwin("cookies.json")
    credentials_json: JsonTwin = JsonTwin("credentials.json")
    config_json: JsonTwin = JsonTwin("config.json")
    input_data_json: JsonTwin = JsonTwin("input_data.json")
    web_json: JsonTwin = JsonTwin("web.json")

    # Ensure config.json is valid
    ensure_json_validity(config_json, default_json("config.json"))

    # Ensure login
    ensure_login(
        cookies_json=cookies_json,
        credentials_json=credentials_json,
        web_json=web_json,
        headless=True,
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
    return start_topic, end_topic


def configure_input_data(config_json: JsonTwin = JsonTwin("config.json"), input_data_json: JsonTwin = JsonTwin("input_data.json")) -> None:
    """
    Configures input_data.json, using config.json as a reference.
    If 
    """
    topics_file_path: str = normalize_path(config_json("topics_file_path"))
    topics = openpyxl.load_workbook(filename=topics_file_path, data_only=True).active
    print(type(topics))


def ensure_json_validity(target_json: JsonTwin, its_default: JsonTwin) -> bool:
    #     Check for it's existance and for entries. If it doesn't exist it will not pass the difference check.
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
            
            raise Exception("Не получилось войти. ")
        cookies = page.context.storage_state()
        browser.close()
        return dict(cookies)


def extract_expires(cookies_json: JsonTwin = JsonTwin("cookies.json")) -> int:
    """Extracts expires from cookies.json"""
    return cookies_json.super_get("expires")


def hard_extract(
    cookies_json: JsonTwin = JsonTwin("cookies.json"), key: str = "expires"
) -> str:
    """Extracts expires from cookies.json"""
    data = cookies_json.to_string(beautiful=False)
    value_chunk = data.split(key)[1].split(",")[0]
    value = value_chunk[2:].strip()
    return value


def cookies_expired(cookies_json: JsonTwin = JsonTwin("cookies.json")) -> bool:
    """Checks if cookies are expired"""
    return int(hard_extract(cookies_json, "expires")) < time.time().__int__() + 30


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
    if cookies_json.get() and cookies_json.get() != {}:
        if cookie_practice_check(
            cookies_json.file_path, web_json("login"), headless=headless
        ):
            # print("Cookies are valid")
            return
        # else:
        #     if not cookies_expired(cookies_json):
        # print("Cookies are not expired, but are invalid")
    else:
        os.remove(cookies_json.file_path)
        # print("Cookies are invalid")
        if credentials_json("validity") == -1:
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
    else:
        if looping > 0:
            ensure_login(
                cookies_json=cookies_json,
                credentials_json=credentials_json,
                web_json=web_json,
                headless=headless,
                looping=looping - 1,
            )
        credentials_json.set("validity", -1)


if __name__ == "__main__":
    main()
