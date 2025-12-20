@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: --- Activate fullscreen mode ---
if not "%1"=="max" start /MAX cmd /c %0 max & exit/b
TITLE Автоматизатор EMIS v0.4.5

:: --- Welcome ---
echo.
echo.
echo.
echo === Настройка автоматизатора EMIS ===
echo.
echo Этот скрипт поможет настроить параметры для автоматизации, затем запустит её
echo.
echo.

:: --- Update dependencies ---
echo ---------------------------------------------------
echo Обновление компонентов в отдельном окне...
start /wait dependencies_installer.cmd
TIMEOUT /T 1 >nul

:: --- Setup ---
:: To be separated into a different file
setup_automator.cmd



:: REDUNDANT (hopefully)===============================================================================
@REM :: --- Step 1. Check for dependencies ---
@REM TIMEOUT /T 1 >nul 2>&1
@REM echo.
@REM echo ---------------------------------------------------
@REM echo Проверка компонентов...


@REM set "COMPONENT_WAS_NOT_INSTALLED=false"

@REM python --version >nul 2>&1
@REM if errorlevel 1 (
@REM     set "COMPONENT_WAS_NOT_INSTALLED=true"
@REM     dependencies_installer.cmd
@REM )


@REM @REM (
@REM @REM     echo from playwright.sync_api import sync_playwright
@REM @REM     echo import pandas
@REM @REM     echo import openpyxl
@REM @REM     echo with sync_playwright(^) as p: 
@REM @REM     echo     p.webkit.launch(headless=True^).new_page(^) 
@REM @REM )>test.py

@REM @REM python test.py >nul 2>&1
@REM if errorlevel 1 (
@REM     set "COMPONENT_WAS_NOT_INSTALLED=true"
@REM     dependencies_installer.cmd
@REM )
@REM @REM del test.py

@REM if "!COMPONENT_WAS_NOT_INSTALLED!"=="true" (
@REM     echo.
@REM     echo Компоненты установлены успешно
@REM ) else (
@REM     echo Все компоненты уже были установлены, ура
@REM )
:: ===============================================================================