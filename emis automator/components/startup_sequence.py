from playwright.sync_api import sync_playwright

def main():
    # import os
    # os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("\n\n")
    print("--- Добро пожаловать в Автоматизатор EMIS! ---")
    print("\n\n")



    print("Проверяем подключение...")
    import connection_check
    connection_check.internet_available()

    print()

    print("Проверяем компоненты...")
    import preparator
    preparator.ensure_json_validity()

    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        print("Входим в EMIS...")
        preparator.ensure_login(browser=browser)
        browser = browser.new_context(storage_state="cookies.json", no_viewport=True)

        def choice(attempts: int = 0) -> str:
            if attempts == 0:
                print("Режимы работы")
                print("    1. План предмета")
                print("    2. План группы")

            user_choice = input("Выберите режим (нужная цифра): ")
            if user_choice in ("1", "2"):
                return user_choice
            else:
                print("Неверный выбор\n")
                return choice(attempts+1)

        print("\n")

        user_choice = choice()
        if user_choice == "1":
            print('Вы выбрали режим "План предмета"')
            preparator.configure_input_data()
            import automator
            automator.run_automation(browser=browser)
            formatted_exit("Работа завершена.")
        elif user_choice == "2":
            print('Вы выбрали режим "План группы"')
            preparator.configure_input_data()
            import enterer
            enterer.enter_topics_program(browser=browser)
            formatted_exit("Работа завершена.")



def formatted_exit(message: str):
    input(f"\n\n\n{message} Нажмите Enter для выхода...\n\n\n")
    exit()


if __name__ == "__main__":
    main()