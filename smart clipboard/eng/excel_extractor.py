import time
import threading
import pandas as pd
import keyboard
import pyperclip
import os
import json # ⭐ NEW: Import the JSON library

# --- New Global Variable for Stopping ---
RUNNING = True 
# ----------------------------------------

# ----------------------------------------------
# ⭐ CONFIGURATION LOADING ⭐
# ----------------------------------------------
CONFIG_FILE = "config.json"
try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    EXCEL_FILE = config['excel_file']
    START_CELL = config['start_cell']
    MODE = config.get('mode', "col") # Default to "col" if not specified
    SHEET_NAME = config.get('sheet_name', 0) # Default to first sheet
    
except FileNotFoundError:
    print(f"\n[CRITICAL ERROR] Configuration file '{CONFIG_FILE}' not found.")
    print("Please run the 'run_clipboard_script.cmd' to set up the configuration first.")
    exit(1)
except json.JSONDecodeError:
    print(f"\n[CRITICAL ERROR] Error reading '{CONFIG_FILE}'. Check the file contents.")
    exit(1)


# ----------------------------------------------
# SMART CLIPBOARD CONFIG
# (Configuration now loaded from config.json)
# ----------------------------------------------
SEQUENCE = []

_start_col = ''.join(filter(str.isalpha, START_CELL)).upper()
_start_row = int(''.join(filter(str.isdigit, START_CELL)))

# Helper to increment column letters
def next_col(col):
    result = list(col)
    i = len(result) - 1
    while i >= 0:
        if result[i] != 'Z':
            result[i] = chr(ord(result[i]) + 1)
            return ''.join(result)
        result[i] = 'A'
        i -= 1
    return 'A' + ''.join(result)

_cur_col = _start_col
_cur_row = _start_row

# ----------------------------------------------
# CORE LOGIC
# ----------------------------------------------

try:
    # Use the file path from the configuration
    print(f"[INFO] Attempting to load Excel file: {EXCEL_FILE}")
    data = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME) 
except FileNotFoundError:
    print(f"\n[CRITICAL ERROR] The Excel file '{EXCEL_FILE}' was not found.")
    print("Please check the file name and ensure it is in the correct folder.")
    exit(1)
except Exception as e:
    print(f"\n[CRITICAL ERROR] An error occurred loading the Excel file: {e}")
    exit(1)

def get_cell_value(cell_ref: str):
    col = ''.join(filter(str.isalpha, cell_ref)).upper()
    row = int(''.join(filter(str.isdigit, cell_ref))) - 1

    col_index = 0
    for c in col:
        col_index = col_index * 26 + (ord(c) - ord('A') + 1)
    col_index -= 1

    try:
        return data.iat[row, col_index]
    except IndexError:
        return None 

# Sequence generation loop
while True:
    cell_ref = f"{_cur_col}{_cur_row}"
    cell_value = get_cell_value(cell_ref)
    
    if pd.isna(cell_value) or str(cell_value).strip() == '':
        break

    SEQUENCE.append(cell_ref)
    
    if MODE == "col":
        _cur_row += 1
    elif MODE == "row":
        _cur_col = next_col(_cur_col)

values = [str(get_cell_value(ref)) for ref in SEQUENCE]

if not SEQUENCE:
    print("\n[INFO] The starting cell or column/row sequence was empty. Nothing to copy.")
    exit(0)

# Initialize index to -1 for correct first-press copy
index = -1 

# --- Stop Function ---
def stop_script():
    global RUNNING
    print("\n[STOP] Alt+C pressed. Smart Clipboard stopping...")
    RUNNING = False
    keyboard.unhook_all()
# -------------------------

def update_clipboard():
    global index, RUNNING
    
    if not RUNNING:
        return

    # 1. Increment index to prepare for the copy
    index += 1
    
    if index < len(values):
        # 2. Copy the value and print feedback
        value_to_copy = values[index]
        pyperclip.copy(value_to_copy)
        print(f"Copied: {value_to_copy}")
        
        # 3. Programmatically simulate paste after copying is done
        time.sleep(0.01)
        keyboard.press_and_release('ctrl+v')

    else:
        # 4. Stop the script when the sequence is finished.
        print("\nSequence finished. Smart Clipboard stopping...")
        RUNNING = False
        keyboard.unhook_all()


# Start the keyboard listeners in a separate thread
threading.Thread(target=lambda: keyboard.add_hotkey('ctrl+v', update_clipboard, suppress=True), daemon=True).start()
threading.Thread(target=lambda: keyboard.add_hotkey('alt+c', stop_script, suppress=True), daemon=True).start()


print(f"Smart Clipboard is running (Start Cell: {START_CELL}).")
print("  - Hotkey (Copy & Paste Next): 'Ctrl+V'")
print("  - Hotkey (Stop Script): 'Alt+C'")
print(f"Sequence Length: {len(SEQUENCE)} cells")

try:
    while RUNNING:
        time.sleep(1)
    print("Script terminated successfully.")

except Exception:
    print("\nAn unexpected error caused the script to stop.")
    pass