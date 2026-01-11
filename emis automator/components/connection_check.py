from typing import Any
from time import sleep

import sys
import os

os.chdir(os.path.dirname(sys.argv[0]))


def main():
    if len(sys.argv) == 1:
        internet_available()
    else:
        if sys.argv[1] == "emis":
            emis_available(sys.argv[2])
        elif sys.argv[1] == "internet":
            internet_available()
        elif sys.argv[1] == "all":
            internet_available()
            emis_available(sys.argv[2])
        else:
            site_available(sys.argv[1])


def wait_for(function: callable, *, to_be: Any = True, check_interval: float = 1):
    """
    Wait for a function to return a specific value.
    """
    while function() != to_be:
        sleep(check_interval)


def check_connection(url: str = "https://www.google.com/", timeout: float = 5) -> bool:
    """
    Checks if a connection to the URL is available.
    If URL is not specified, checks for connection to Google.
    """
    import requests

    try:
        requests.get(url=url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def emis_is_up(
    login_information: str = "cookies.json",
    *,
    headless: bool = True,
    emis_url: str = "https://litsey.edu.uz/",
) -> bool:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        browser = browser.new_context(storage_state=login_information)
        page = browser.new_page()
        page.goto(emis_url)
        try:
            page.wait_for_load_state("networkidle")
            page.click("img[alt='error-404']", timeout=1000)
            return False
        except Exception:
            return True


def internet_available():
    if not check_connection():
        print("[ИНФО] Отсутствует подключение к интернету.")
        print("(?) Восстановите подключение, не закрывайте это окно.")
        wait_for(function=lambda: check_connection(), to_be=True, check_interval=3)
        print("[ИНФО] Подключение к интернету восстановлено.")


def emis_available(login_information: str = "cookies.json"):
    if not emis_is_up(login_information=login_information):
        print("[ИНФО] EMIS сейчас недоступен.")
        print(
            "(?) Работа автоматически продолжится когда EMIS станет доступен, не закрывайте это окно."
        )
        wait_for(function=lambda: emis_is_up(login_information=login_information), to_be=True, check_interval=20)
        print("[ИНФО] EMIS стал доступен.")


def site_available(site_url: str):
    if not check_connection(site_url):
        print(f"\n[ИНФО] Отсутствует подключение к {site_url}.")
        print("(?) Восстановите подключение, не закрывайте это окно.")
        wait_for(
            function=lambda: check_connection(site_url), to_be=True, check_interval=3
        )
        print(f"[ИНФО] Подключение к {site_url} восстановлено.")


if __name__ == "__main__":
    main()