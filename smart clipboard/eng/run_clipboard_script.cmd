@echo off
SET PYTHON_SCRIPT_NAME=excel_extractor.py
SET CONFIG_FILE=config.json

echo.
echo === Smart Clipboard Execution ===
echo.

:: -----------------------------------------------------------
:: ⭐ STEP 1: CHECK AND CREATE CONFIGURATION FILE ⭐
:: -----------------------------------------------------------
if exist "%CONFIG_FILE%" (
    echo [INFO] Configuration file found. Skipping setup.
    goto :INSTALL_DEPS
)

echo [SETUP] First-time setup required.
echo [SETUP] Please provide the configuration details.
echo ---------------------------------------------------

:GET_FILE
set "EXCEL_FILE_PATH="
echo.
echo ⭐ DRAG AND DROP your Excel file here (e.g., C:\path\to\data.xlsx) and press ENTER:
set /p "EXCEL_FILE_PATH="

:: Clean the input: Strip the quotes added by Windows during drag-and-drop
set "CLEAN_PATH=%EXCEL_FILE_PATH:"=%"

if not defined CLEAN_PATH (
    echo [ERROR] File path cannot be empty.
    goto :GET_FILE
)

:: ⭐ CRITICAL FIX: Escape backslashes for valid JSON (replaces \ with \\) ⭐
set "ESCAPED_PATH=%CLEAN_PATH:\=\\%"

:GET_CELL
set "START_CELL_REF="
set /p "START_CELL_REF=Enter the starting cell (e.g., C2): "
if not defined START_CELL_REF (
    echo [ERROR] Starting cell cannot be empty.
    goto :GET_CELL
)

:: Construct the JSON content using the ESCAPED_PATH variable
echo {                      > "%CONFIG_FILE%"
echo "excel_file": "%ESCAPED_PATH%",  >> "%CONFIG_FILE%"
echo "start_cell": "%START_CELL_REF%",   >> "%CONFIG_FILE%"
echo "mode": "col",                       >> "%CONFIG_FILE%"
echo "sheet_name": 0                     >> "%CONFIG_FILE%"
echo }                                   >> "%CONFIG_FILE%"

echo [SUCCESS] Configuration saved to %CONFIG_FILE%.

:INSTALL_DEPS
:: -----------------------------------------------------------
:: STEP 2: INSTALL DEPENDENCIES AND RUN
:: -----------------------------------------------------------
echo.
echo [INFO] Installing/Checking required libraries...
python -m pip install pandas keyboard pyperclip >nul 2>&1

echo --------------------------------------------------------------------------------------------------
echo [INFO] Running the Smart Clipboard script.
echo NOTE: Do NOT close this window. Stop the script by pressing 'Alt+C'.
echo --------------------------------------------------------------------------------------------------

:: Execute the Python script
python "%PYTHON_SCRIPT_NAME%"

:: The script should only reach this point if the Python script itself finished (sequence complete or Alt+C).
echo.
echo Script execution terminated.
echo Press any key to close this window...
pause >nul