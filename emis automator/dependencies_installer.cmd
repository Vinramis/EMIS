@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

TIMEOUT /T 2 >nul 2>&1
echo.
echo.
echo --- Установка библиотек и зависимостей ---
echo.
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Этап 1. Установка программы Python
    goto :INSTALL_PYTHON
)

echo Этап 2. Установка библиотек и зависимостей
echo (?) На это может потребоваться некоторое время.
goto :INSTALL_DEPS


:: Install Python (local)
:INSTALL_PYTHON
echo.
python_installer.exe /passive InstallAllUsers=0 PrependPath=1 >nul 2>&1
echo [ИНФО] Python установлен.
echo (?) Пожалуйста, закройте этот скрипт и запустите снова.
echo.

:INSTALL_DEPS
:: Install libraries
echo.
python -m pip install playwright pandas openpyxl >nul 2>&1
echo [ИНФО] Библиотеки установлены.
TIMEOUT /T 1 >nul 2>&1
:: Install only the WebKit engine
echo.
python -m playwright install webkit >nul 2>&1
echo [ИНФО] Зависимости установлены.
TIMEOUT /T 1 >nul 2>&1

echo.
echo (?) Всё готово :)
echo (?) Пожалуйста, закройте этот скрипт и запустите основную программу.
echo.

:: Closing window
:CLOSE_WINDOW
echo.
echo.
echo (?) Нажмите любую клавишу для выхода...
echo.
echo.
pause >nul