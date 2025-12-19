@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: Check for internet connection
ping -n 1 google.com >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Нет подключения к интернету.
    echo (?) Пожалуйста, подключитесь к интернету и запустите скрипт снова.
    goto :CLOSE_WINDOW
)


:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    goto :INSTALL_PYTHON
) else (
    goto :INSTALL_DEPS
)


:: Install Python (local)
:INSTALL_PYTHON
echo.
echo [ИНФО] Устанавливаем Python, пожалуйста, не закрывайте окно...
python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 >nul 2>&1
echo [ИНФО] Python установлен.
echo.

goto :RESTART


:INSTALL_DEPS
:: Install libraries
echo.
echo [ИНФО] Устанавливаем библиотеки (всего 3), пожалуйста, не закрывайте окно...
echo.

python -m pip install playwright >nul 2>&1
echo Библиотека Playwright установлена. 
echo (?) Эта библиотека нужна для работы с веб-браузером

echo.

python -m pip install pandas >nul 2>&1
echo Библиотека Pandas установлена.
echo (?) Эта библиотека нужна для работы с файлами

echo.

python -m pip install openpyxl >nul 2>&1
echo Библиотека OpenPyXL установлена.
echo (?) Эта библиотека нужна для работы с Excel

echo.
echo [ИНФО] Все библиотеки установлены.
TIMEOUT /T 1 >nul 2>&1

:: Install WebKit engine
echo.
echo [ИНФО] Устанавливаем зависимость, пожалуйста, не закрывайте окно...
echo (?) Это самый долгий процесс
echo (?) 
python -m playwright install webkit >nul 2>&1
echo [ИНФО] Зависимости установлены.
echo.
TIMEOUT /T 1 >nul 2>&1

goto :CLOSE_WINDOW


:: Restart (to apply changes)
:RESTART
start "" "%~f0"
exit /b


:: Closing window
:CLOSE_WINDOW