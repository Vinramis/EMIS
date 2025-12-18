@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion


:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    goto :INSTALL_PYTHON
)
goto :INSTALL_DEPS


:: Install Python (local)
:INSTALL_PYTHON
echo.
echo [ИНФО] Устанавливаем Python...
python_installer.exe /passive InstallAllUsers=0 PrependPath=1 >nul 2>&1
echo [ИНФО] Python установлен.
echo.
goto :CLOSE_WINDOW


:INSTALL_DEPS
:: Install libraries
echo.
echo [ИНФО] Устанавливаем библиотеки...
python -m pip install playwright pandas openpyxl >nul 2>&1
echo [ИНФО] Библиотеки установлены.
TIMEOUT /T 1 >nul 2>&1
:: Install WebKit engine
echo.
echo [ИНФО] Устанавливаем зависимости...
echo (?) Это обычно самый долгий процесс, пожалуйста, не закрывайте окно
python -m playwright install webkit >nul 2>&1
echo [ИНФО] Зависимости установлены.
echo.
TIMEOUT /T 1 >nul 2>&1


:: Closing window
:CLOSE_WINDOW