
# This script is used to prepare everything for smooth work of the main script.

# It does the following:
# 1. Checks topics numbers interval.
# 2. Creates/Rewrites a config.db file. (containing all topic names and file paths)
# 3. 

import os
import json
import sqlite3
import openpyxl
import playwright
import file_utils
import excel_utils

