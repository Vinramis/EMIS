
import time
import os
import sys
import json
import pathlib
from pathlib import Path

import openpyxl
from playwright.sync_api import sync_playwright, Browser, Page

import file_utils
import excel_utils
from config_manager import JsonTwin

# This script is used to prepare everything for smooth work of the main script.

# It does the following:
# 1. Checks if config.json exists and is valid, if not, creates/rewrites it.
# 2. Checks topics numbers interval.
# 3. Creates/Rewrites a config.db file. (containing all topic names and file paths)
# 4.
# from automator import run_automation

def main():
    # Load all configurations
    default_json: JsonTwin = JsonTwin("default.json")

    cookies_json: JsonTwin = JsonTwin("cookies.json")
    credentials_json: JsonTwin = JsonTwin("credentials.json")
    config_json: JsonTwin = JsonTwin("config.json")
    input_data_json: JsonTwin = JsonTwin("input_data.json")
    web_json: JsonTwin = JsonTwin("web.json")

    # Ensure config.json is valid
    ensure_json_validity(config_json, default_json, "config.json")


    # Ensure login
    ensure_login(
        cookies_json=cookies_json,
        credentials_json=credentials_json,
        web_json=web_json,
        headless=True,
    )


    # # Ensure credentials.json is valid
    # ensure_json_validity(credentials_json, default_json, "credentials.json")


    # # Ensure input_data.json is valid
    # ensure_json_validity(input_data_json, default_json, "input_data.json")


    # # Ensure web.json is valid
    # ensure_json_validity(web_json, default_json, "web.json")


def get_credentials():
    login = input("Введите ваш логин EMIS: ")
    password = input("Введите ваш пароль EMIS: ")
    return login, password

def ensure_json_validity(
    target_json: JsonTwin, default_json: JsonTwin, target_path: str
) -> bool:
    #     Check for it's existance and for entries
    if target_json.get() == {} or target_json.super_keys().difference(
        default_json.get(target_path).super_keys()
    ):
        target_json.pull(default_json(target_path))
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

        page.fill("input[autocomplete='username']", login)
        page.fill("input[autocomplete='current-password']", password)
        page.get_by_text(c("login_button_text"), exact=True).click()
        page.wait_for_load_state("networkidle")

        if page.url != c("success_url"):
            time.sleep(999)
            raise Exception("Login failed")
        cookies = page.context.storage_state()
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
            get_credentials()
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
        credentials_json.set("validity", -1)
