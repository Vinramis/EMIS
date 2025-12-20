:: --- Activate fullscreen mode ---
mode con: cols=120 lines=30

@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: --- Step 0. Welcome ---
echo.
echo.
echo.
echo === Настройка автоматизатора EMIS ===
echo.
echo Этот скрипт поможет настроить параметры для автоматизации, затем запустит её
echo.
echo.


:: --- Step 1. Check for dependencies ---
TIMEOUT /T 1 >nul 2>&1
echo.
echo ---------------------------------------------------
echo Проверка компонентов...


set "COMPONENT_WAS_NOT_INSTALLED=false"

python --version >nul 2>&1
if errorlevel 1 (
    set "COMPONENT_WAS_NOT_INSTALLED=true"
    dependencies_installer.cmd
)

:: DEPRECATED
@REM python -c "from playwright.sync_api import sync_playwright; import pandas; import openpyxl; with sync_playwright() as p: p.webkit.launch(headless=False).new_page()" >nul 2>&1

@REM (
@REM     echo from playwright.sync_api import sync_playwright
@REM     echo import pandas
@REM     echo import openpyxl
@REM     echo with sync_playwright(^) as p: 
@REM     echo     p.webkit.launch(headless=True^).new_page(^) 
@REM )>test.py

@REM python test.py >nul 2>&1
if errorlevel 1 (
    set "COMPONENT_WAS_NOT_INSTALLED=true"
    dependencies_installer.cmd
)
@REM del test.py

if "!COMPONENT_WAS_NOT_INSTALLED!"=="true" (
    echo.
    echo Компоненты установлены успешно
) else (
    echo Все компоненты уже были установлены, ура
)

:: --- Step 2. Setup ---
setup_automator.cmd

@REM @echo off
@REM cd /d "%~dp0"

@REM :: Create the file with a check
@REM echo Writing test.py...
@REM (
@REM     echo from playwright.sync_api import sync_playwright
@REM     echo import pandas
@REM     echo import openpyxl
@REM     echo print()
@REM     echo print("File written successfully!")
@REM )>test.py

@REM if not exist test.py (
@REM     echo [ERROR] test.py was NEVER created! Check folder permissions.
@REM     pause
@REM     exit
@REM )

@REM echo Running test.py...
@REM python test.py
@REM pause