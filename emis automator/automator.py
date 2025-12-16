
import time
import sys
from playwright.sync_api import sync_playwright

# Import local modules
try:
    from config_manager import ConfigManager
    import file_utils
    import excel_utils
except ImportError as e:
    print(f"[CRITICAL ERROR] Could not import modules: {e}")
    print("Ensure config_manager.py, file_utils.py, and excel_utils.py are in the same directory.")
    sys.exit(1)

def run_automation():
    # 1. Load Configuration
    cfg = ConfigManager()

    # 2. File Organization
    # Updates TOPICS_FOLDER and HOMEWORK_FOLDER if they were effectively split
    cfg.TOPICS_FOLDER, cfg.HOMEWORK_FOLDER = file_utils.organize_files(cfg.TOPICS_FOLDER, cfg.HOMEWORK_FOLDER)

    # 3. Browser Automation
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        page = browser.new_page()

        print(f"Navigating to login page...")
        page.goto(cfg.ONE_ID_LOGIN_URL)

        # Login
        print("Logging in...")
        try:
            page.locator(cfg.ONE_ID_BUTTON_SELECTOR).click()
            page.get_by_placeholder(cfg.LOGIN_FIELD_PLACEHOLDER).fill(cfg.LOGIN)
            page.get_by_placeholder(cfg.PASSWORD_FIELD_PLACEHOLDER).fill(cfg.PASSWORD)
            # Click the first matching login button
            page.get_by_text(cfg.LOGIN_BUTTON_TEXT).first.click()
            
            page.wait_for_url(cfg.SUCCESS_URL)
            print("Login successful!")
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            return

        # 4. Prepare Data
        print("Preparing data from Excel...")
        topic_names = excel_utils.read_topics_from_excel(
            cfg.TOPICS_FILE_PATH, 
            cfg.START_CELL, 
            cfg.MODE
        )
        print(f"Extracted {len(topic_names)} records from Excel.")

        # 5. Automation Loop
        print("Starting automation... \n(?) Press Ctrl+C in terminal to stop.")
        page.goto(cfg.NEW_TOPIC_URL)

        if cfg.LINE_COUNT < cfg.START_FROM_LINE:
            print(f"[CRITICAL ERROR] Line count ({cfg.LINE_COUNT}) is less than start line ({cfg.START_FROM_LINE}).")
            return

        actual_length = min(cfg.LINE_COUNT, len(topic_names))
        # Adjust logic to match original counter behavior
        # Original: for i in range(START_FROM_LINE - 1, actual_length): ... counter += 1
        # It used a separate counter variable for the UI logic
        
        counter = -1
        
        for i in range(cfg.START_FROM_LINE - 1, actual_length):
            counter += 1
            print(f"\n--- Processing line {i + 1} of {actual_length} ---")

            topic_name = topic_names[i]
            # check_for matches the index (1-based)
            check_for = str(i + 1)

            # Find files
            topic_file_path = file_utils.find_file_by_prefix(cfg.TOPICS_FOLDER, check_for)
            homework_file_path = file_utils.find_file_by_prefix(cfg.HOMEWORK_FOLDER, check_for)

            if not topic_file_path: 
                print(f"   - Topic file missing in '{cfg.TOPICS_FOLDER}'")
            if not homework_file_path: 
                print(f"   - Homework file missing in '{cfg.HOMEWORK_FOLDER}'")

            try:
                print("Clicking 'Add Line'...")
                page.locator(cfg.ADD_LINE_BUTTON).click()
                time.sleep(0.01) # Small delay as in original

                if not topic_name:
                    print("[CRITICAL ERROR] Topic name is undefined.")
                    sys.exit(1)

                print(f"Filling topic name: '{topic_name}'")
                # Selector logic from original: "#topics_{1000+counter}_name"
                # Using constants from config
                page.locator(f"{cfg.TOPICS_PREFIX}{1000+counter}{cfg.TOPIC_NAME_SUFFIX}").fill(topic_name)

                if topic_file_path:
                    print(f"Uploading topic file: {topic_file_path}")
                    page.locator(f"{cfg.TOPICS_PREFIX}{1000+counter}{cfg.TOPIC_FILE_SUFFIX}").set_input_files(topic_file_path)

                if homework_file_path:
                    print(f"Uploading homework file: {homework_file_path}")
                    page.locator(f"{cfg.TOPICS_PREFIX}{1000+counter}{cfg.HOMEWORK_FILE_SUFFIX}").set_input_files(homework_file_path)

            except Exception as e:
                print(f"[CRITICAL ERROR] at line {counter + 1} (Process item {i+1}): {e}")
                print("Saving error screenshot.")
                page.screenshot(path="error_screenshot.png")
                break

        print("\n--- Automation Complete! ---")
        print("\n\n\n(?) You can now interact with the browser. Script will exit when browser is closed.\n\n\n")

        # Wait for user to close browser
        while True:
            try:
                if page.is_closed():
                    break
                page.wait_for_event("close", timeout=1000)
            except Exception:
                # Timeout or other issue, check if closed
                if page.is_closed():
                    break
                continue
        
        print("Browser closed. Exiting script.\n")
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"[CRITICAL ERROR] Unhandled exception: {e}")
        # Keep window open if crashed so user sees error?
        # Only if NOT run from unexpected environment. 
        # Original had time.sleep(999999)
        time.sleep(10)
