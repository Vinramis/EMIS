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

python -c "from playwright.sync_api import sync_playwright; import pandas; import openpyxl; with sync_playwright() as p: p.webkit.launch(headless=False).new_page()" >nul 2>&1
if errorlevel 1 (
    set "COMPONENT_WAS_NOT_INSTALLED=true"
    dependencies_installer.cmd
)


if "!COMPONENT_WAS_NOT_INSTALLED!"=="true" (
    echo.
    echo Компоненты установлены успешно
) else (
    echo Все компоненты уже были установлены, ура
)

:: --- Step 2. Setup automator ---
setup_automator.cmd