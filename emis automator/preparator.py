
# This script is used to prepare everything for smooth work of the main script.

# It does the following:
# 1. Checks if config.json exists and is valid, if not, creates/rewrites it.
# 2. Checks topics numbers interval.
# 3. Creates/Rewrites a config.db file. (containing all topic names and file paths)
# 4. 

import os
import sys
import json
import sqlite3
import openpyxl
import playwright
import file_utils
import excel_utils
from config_manager import ConfigManager

# Check if config.json exists and is valid
try:
    configuration = ConfigManager()
except Exception as e:
    print(f"[ОШИБКА] Не удалось загрузить конфигурацию: {e}")
    print("(?) Кажется, вы запустили программу неправильно. Попробуйте заново.")
    pause = input("Нажмите Enter...")
    sys.exit(1)

