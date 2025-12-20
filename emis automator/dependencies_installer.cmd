@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion
:: %= comment =% is a structure used to comment inside of a single line in batch files


:: REDUNDANT
@REM :: Check for what we need
@REM python --version >nul 2>&1
@REM if errorlevel 1 (
@REM     goto :INSTALL_PYTHON
@REM ) else (
@REM     goto :INSTALL_DEPS
@REM )
:: REDUNDANT


:: Install Python (local)
:INSTALL_PYTHON
::     Convert the relative path to a FULL absolute path
set "RELATIVE_PATH=python314"
for %%i in ("%RELATIVE_PATH%") do set "PYTHON_FULL_PATH=%%~fi"

echo.
echo [ИНФО] Устанавливаем Python, пожалуйста, не закрывайте окно...
python_installer.exe /passive InstallAllUsers=0 PrependPath=0 InstallLauncherAllUsers=0 Include_test=0 Include_doc=0 Include_pip=1 Shortcuts=1 TargetDir="!PYTHON_FULL_PATH!"
echo [ИНФО] Python установлен.
TIMEOUT /T 1 >nul 2>&1

goto :INSTALL_DEPS


:: Install dependencies
:INSTALL_DEPS
::     Check for internet connection
:CHECK_CONNECTION
ping -n 1 google.com >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Нет подключения к интернету.
    echo (?) Пожалуйста, проверьте подключение и нажмите Enter
    pause >nul 2>&1
    goto :CHECK_CONNECTION
)


::     Install libraries
echo.
echo [ИНФО] Устанавливаем библиотеки (всего 3), пожалуйста, не закрывайте окно...
echo.

TIMEOUT /T 1 >nul 2>&1
!PYTHON_PATH!\\python -m pip install playwright >nul 2>&1
echo Библиотека Playwright установлена. 
echo (?) Эта библиотека нужна для работы с веб-браузером

echo.

TIMEOUT /T 1 >nul 2>&1
!PYTHON_PATH!\python -m pip install pandas >nul 2>&1
echo Библиотека Pandas установлена.
echo (?) Эта библиотека нужна для работы с файлами

echo.

TIMEOUT /T 1 >nul 2>&1
!PYTHON_PATH!python -m pip install openpyxl >nul 2>&1
echo Библиотека OpenPyXL установлена.
echo (?) Эта библиотека нужна для работы с Excel

echo.
TIMEOUT /T 1 >nul 2>&1
echo [ИНФО] Все библиотеки установлены.

::     Install WebKit engine
echo.
echo [ИНФО] Устанавливаем зависимость (WebKit), пожалуйста, не закрывайте окно...
TIMEOUT /T 1 >nul 2>&1
echo (?) Это самый долгий процесс
TIMEOUT /T 3 >nul 2>&1
echo (?) WebKit - это браузер, который будет использоваться для автоматизации
TIMEOUT /T 1 >nul 2>&1
!PYTHON_PATH!python -m playwright install webkit >nul 2>&1
echo [ИНФО] Зависимости установлены.
echo.
TIMEOUT /T 1 >nul 2>&1

goto :CLOSE_WINDOW


:: Closing window
:CLOSE_WINDOW