# WORK IN PROGRESS

import file_utils
# import time

import os
import playwright
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
import openpyxl
import excel_utils

from config_manager import JsonTwin

FIELD_SELECTOR_PART1 = "#StudyGuide_data_"
FIELD_SELECTOR_PART2 = "_topic_id"  # must be concatenated with index in the middle (from 0)
VIRTUAL_LIST_SELECTOR = "div.ant-select-item-option-content"
CHOOSER_FIELD_SELECTOR = "input[class='ant-select-input']"

config_json = JsonTwin("config.json")


def enter_topics_program():
    directory: str = os.path.dirname(__file__)
    os.chdir(directory)
    syllabus_path: str = file_utils.find_single_excel(os.path.dirname(directory))
    syllabus: openpyxl.Worksheet = openpyxl.load_workbook(syllabus_path).active
    topics: list[str] = excel_utils.read_topics_from_excel(syllabus, start_cell=config_json("start_cell"))

    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        browser: BrowserContext = browser.new_context(
            storage_state="cookies.json", no_viewport=True
        )
        page: Page = browser.new_page()
        page.goto("https://litsey.edu.uz/teacher/groups")

        print("В окне браузера:")
        print("  1) Выберите группу")
        print("  2) Перейдите на вкладку 'План предмета' ('O‘quv qo‘llanma')")
        print("  3) Выберите название плана ('Mavzu')")
        input("\nНажмите Enter, чтобы продолжить...")

        # buffer = ""
        # while (
        #     # "tab=journal" not in buffer
        #     # or "tab=study-guide" not in buffer or
        #     "group_number" not in buffer
        # ):
        #     time.sleep(0.05)
        #     page.wait_for_load_state("load")
        #     # page.wait_for_load_state("networkidle")
        #     buffer = page.evaluate("window.location.href")

        #     # print(buffer)
        # # print(page.locator("div").filter(has_text="O‘quv qo‘llanma").all_())
        # page.locator("div").filter(has_text="O‘quv qo‘llanma").nth(-1).click()
        # # study_guide_tab = page.evaluate("window.location.href") + "&tab=study-guide"
        # # page.goto(study_guide_tab)

        # page.wait_for_load_state("networkidle")
        # print(page.locator("role=combobox").all_text_contents())
        # # page.wait_for_timeout(999000)
        # page.get_by_role("combobox").click()
        # page.keyboard.type("Алгебра 2 курс")
        # # page.get_by_role("combobox").fill("Алгебра 2 курс")
        # page.keyboard.press("Enter")

        # input("Нажмите Enter, чтобы продолжить...")

        # time.sleep(2)
        # page.goto("https://litsey.edu.uz/teacher/groups/preview/3315/subject/34?name=Algebra+%28Chuqurlashtirilgan+fanlar%29&group_number=1&tab=study-guide")
        # page.fill("input[id='rc_select_0']", "Алгебра 2 курс")
        # page.keyboard.press("Enter")

        fields_count = int((len(page.locator("input[class='ant-select-input']").all()) - 1) / 2)

        success: int = 0
        first = int(input("Введите номер первой темы: ")) - 1
        topics = topics[first:]
        for i in range(min(fields_count, len(topics))):
            if enter_topic(page, i, topics[i])[0]:
                success += 1
        print(f"[ИНФО] Успешно заполнено {success} из {fields_count}.")

        # page.locator("button").filter(has_text="Saqlash").click()

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


def enter_topic(page: Page, count: int, name: str) -> tuple[bool, bool]:
    filled: bool = False
    not_out_of_range: bool = True
    try:
        page.fill(
            f"{FIELD_SELECTOR_PART1}{count}{FIELD_SELECTOR_PART2}", name, timeout=1000
        )
        page.keyboard.press("Enter")
        # first version of the code - more logical (in my opinion)
        
        # finding_options = page.locator("div[class='ant-select-item-option-content']").all()

        # if len(finding_options) < 2:
        #     page.keyboard.press("Enter")
        # elif len(page.locator("div[class='ant-select-item-option-content']").filter(has_text=name).all()) == 1:
        #     page.locator("div[class='ant-select-item-option-content']").filter(has_text=name).click()
        # elif len(page.locator("div[class='ant-select-item-option-content']").filter(has_text=name).all()) == 2:
        #     if len(page.locator("div[class='ant-select-item-option-content']").locator(f'text="{name}"').all()) == 1:
        #         page.locator("div[class='ant-select-item-option-content']").locator(f'text="{name}"').first.click()
        # else:
        #     page.keyboard.press("Enter")

        # # lets print all of those
        # print(page.locator("div[class='ant-select-item-option-content']").all())
        # print(page.locator("div[class='ant-select-item-option-content']").filter(has_text=name).all())
        # print(page.locator("div[class='ant-select-item-option-content']").locator(f'text="{name}"').all())
        # print(page.locator("div[class='ant-select-item-option-content']").filter(has_text=name).first.all())
        # print()
        
        field = page.get_by_text(name).all()
        filled = len(field) > 0
    except playwright._impl._errors.TimeoutError:
        not_out_of_range = False
    return filled, not_out_of_range


if __name__ == "__main__":
    try:
        enter_topics_program()
    except KeyboardInterrupt:
        pass
    #     print("\n\nВы остановили программу. Можно закрыть это окно.\n\n")
    #     time.sleep(999)
    # except Exception as e:
    #     print(f"[КРИТИЧЕСКАЯ ОШИБКА] Необработанное исключение: {e}")
    #     time.sleep(999)
