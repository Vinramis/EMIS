

# WORK IN PROGRESS

import time
import json
import openpyxl
# import excel_utils
import os
from playwright.sync_api import sync_playwright, Browser, Page

FIELD_SELECTOR_PART1 = "#StudyGuide_data_"
FIELD_SELECTOR_PART2 = "_topic_id" # must be concatenated with index in the middle (from 0)
VIRTUAL_LIST_SELECTOR = "div.ant-select-item-option-content"
VIRTUAL_LIST_PLACEHOLDER = "" # whatever topic you have, but cut or smth, don't remember

def test():
    # syllabus = openpyxl.load_workbook("syllabus.xlsx").active
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        page: Page = browser.new_page()
        page.goto("https://litsey.edu.uz/login")
        page.click("#root > div > div > div > main > div > div > a")
        page.get_by_placeholder("Loginni kiriting").fill("muravleva_natalya")
        page.get_by_placeholder("Parolni kiriting").fill("6R8t2vLEuZzV_C")
        page.get_by_text("Kirish").click()
        page.wait_for_url("https://litsey.edu.uz")
        page.goto("https://litsey.edu.uz/teacher/groups/preview/3315/subject/34?name=Algebra+%28Chuqurlashtirilgan+fanlar%29&group_number=1&tab=study-guide")
        input("Press Enter when ready...")

        all = 0
        success = 0
        for i in range(10):
            if enter_topic(page, i, "чальный контро"):
                success += 1
            all += 1
        print(f"[ИНФО] Успешно заполнено {success}/{all}.")
        input("Press Enter to close...")


def enter_topic(page: Page, count: int, name: str) -> bool:
    try:
        page.fill(f"{FIELD_SELECTOR_PART1}{count}{FIELD_SELECTOR_PART2}", name)
        time.sleep(0.5)
        page.keyboard.press("Enter")
    except Exception:
        return False
    return True


if __name__ == "__main__":
    try:
        test()
    except KeyboardInterrupt:
        print("\n\nВы остановили программу. Можно закрыть это окно.\n\n")
        time.sleep(999)
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] Необработанное исключение: {e}")
        time.sleep(999)
