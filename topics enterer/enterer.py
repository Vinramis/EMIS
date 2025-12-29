

# WORK IN PROGRESS


# push edit button   button.ant-btn:nth-child(2)
# edit first name   #StudyGuide_data_0_topic_id

# stupid list of topics any button selector   div.ant-select-item-option-content

import time
import json
import os
from playwright.sync_api import sync_playwright

# EDIT_BUTTON_SELECTOR = "button.ant-btn:nth-child(2)"
FIELD_SELECTOR_PART1 = "#StudyGuide_data_"
FIELD_SELECTOR_PART2 = "_topic_id" # must be concatenated with index in the middle (from 0)
# ARROW_SELECTOR = "#StudyGuide > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(3) > div:nth-child(1) > span:nth-child(2)"
VIRTUAL_LIST_SELECTOR = "div.ant-select-item-option-content"
VIRTUAL_LIST_PLACEHOLDER = "" # whatever topic you have, but cut or smth, don't remember


if __name__ == "__main__":
    # TEST
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://litsey.edu.uz/login")
        page.click("#root > div > div > div > main > div > div > a")
        page.get_by_placeholder("Loginni kiriting").fill("muravleva_natalya")
        page.get_by_placeholder("Parolni kiriting").fill("6R8t2vLEuZzV_C")
        page.get_by_role("button", name="Kirish").click()
        page.wait_for_url("https://litsey.edu.uz")
        page.wait_for_url("https://litsey.edu.uz/")
        page.goto("https://litsey.edu.uz/teacher/groups/preview/3315/subject/34?name=Algebra+%28Chuqurlashtirilgan+fanlar%29&group_number=1&tab=study-guide")
        input("Press Enter when ready...")
        page.fill("#StudyGuide_data_0_topic_id", "чальный контро")
        # try:
        #     page.get_by_role("option", name="Начальный").click(timeout=1000)
        #     print("Option clicked successfully!")
        # except Exception as e:
        #     print(e)
        #     pass
        try:
            page.get_by_text("чальный контро").first.click(timeout=1000)
            print("Text clicked successfully!")
        except Exception as e:
            print(e)
            pass
        # try:
        #     page.get_by_placeholder("Начальный контроль").click(timeout=1000)
        #     print("Placeholder clicked successfully!")
        # except Exception as e:
        #     print(e)
        #     pass
        # try:
        #     page.click("div.ant-select-item-option-content", timeout=1000)
        #     print("Virtual list clicked successfully!")
        # except Exception as e:
        #     print(e)
        #     pass
        input("Press Enter to close...")