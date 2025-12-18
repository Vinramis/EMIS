@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

echo.
echo.
echo.
echo === Настройка автоматизатора EMIS ===
echo.
echo Этот Скрипт поможет настроить параметры для автоматизации, затем запустит её
echo.
echo.
echo.


:: --- Check for dependencies ---
TIMEOUT /T 1 >nul 2>&1
echo ---------------------------------------------------
echo Проверка компонентов...
set "COMPONENT_WAS_NOT_INSTALLED=false"

python --version >nul 2>&1
if errorlevel 1 (
    set "COMPONENT_WAS_NOT_INSTALLED=true"
    dependencies_installer.cmd
    TIMEOUT /T 3 >nul 2>&1
)

python -c "import playwright" >nul 2>&1
if errorlevel 1 (
    set "COMPONENT_WAS_NOT_INSTALLED=true"
    dependencies_installer.cmd
)

python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    set "COMPONENT_WAS_NOT_INSTALLED=true"
    dependencies_installer.cmd
)

python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    set "COMPONENT_WAS_NOT_INSTALLED=true"
    dependencies_installer.cmd
)

if "!COMPONENT_WAS_NOT_INSTALLED!"=="true" (
    TIMEOUT /T 3 >nul 2>&1
    echo.
    echo Компоненты установлены успешно
) else (
    echo Все компоненты уже были установлены, ура
)


:: --- Check for existing config file ---
TIMEOUT /T 1 >nul 2>&1
echo.
echo ---------------------------------------------------
echo Проверка конфигурации...
if exist "config.json" (
    set "USE_EXISTING="
    set /p "USE_EXISTING=Конфигурация уже существует, использовать её? (введите 1 для нет, пропуск для да): "
    
    if "!USE_EXISTING!"=="1" (
        echo Перенастройка параметров...
        goto :RECONFIGURE
    ) else (
        echo Используется существующая конфигурация.
        goto :LAUNCH_AUTOMATOR
    )
) else (
    echo --- Учетные данные ---
    TIMEOUT /T 1 >nul 2>&1
    set /p "LOGIN=Введите ваш логин EMIS: "

    TIMEOUT /T 1 >nul 2>&1
    set /p "PASSWORD=Введите ваш пароль EMIS: "
)
goto :GATHER_SETTINGS


:RECONFIGURE
echo.
echo --- Учетные данные ---
echo (?) Оставьте пустым и нажмите Enter, чтобы сохранить существующие
echo (?) Существующие учетные данные будут в квадратных скобках
echo.

:: Try to parse existing credentials to use as defaults
for /f "tokens=2 delims=:," %%a in ('findstr /R /C:"\"login\"" "config.json"') do set "EXISTING_LOGIN=%%~a"
for /f "tokens=2 delims=:," %%a in ('findstr /R /C:"\"password\"" "config.json"') do set "EXISTING_PASSWORD=%%~a"
:: Remove quotes
set "EXISTING_LOGIN=!EXISTING_LOGIN:"=!"
set "EXISTING_PASSWORD=!EXISTING_PASSWORD:"=!"
:: Remove leading spaces
set "EXISTING_LOGIN=!EXISTING_LOGIN:~1!"
set "EXISTING_PASSWORD=!EXISTING_PASSWORD:~1!"

set /p "LOGIN=Введите ваш логин EMIS [!EXISTING_LOGIN!]: "
TIMEOUT /T 1 >nul 2>&1
set /p "PASSWORD=Введите ваш пароль EMIS [!EXISTING_PASSWORD!]: "
TIMEOUT /T 1 >nul 2>&1
if not defined LOGIN set "LOGIN=!EXISTING_LOGIN!"
if not defined PASSWORD set "PASSWORD=!EXISTING_PASSWORD!"

:GATHER_SETTINGS
echo.
echo.
echo --- Параметры автоматизации ---
echo (?) Оставьте пустым и нажмите Enter, чтобы сохранить значения по умолчанию
echo (?) Значения по умолчанию будут в квадратных скобках
echo.

set DEFAULT_LINE_COUNT=6
set "DEFAULT_TOPICS_FILE_PATH=КТП.xlsx"
set "DEFAULT_START_CELL=B6"
set DEFAULT_START_FROM_LINE=1
set "DEFAULT_MODE=col"
set "DEFAULT_TOPICS_FOLDER=КЛ"
set "DEFAULT_HOMEWORK_FOLDER=ДЗ"

set "TOPICS_FILE_PATH="
@REM DEPRECATED
@REM set /p "TOPICS_FILE_PATH=Введите путь к файлу Excel с темами [%DEFAULT_TOPICS_FILE_PATH%]: "
if not defined TOPICS_FILE_PATH set "TOPICS_FILE_PATH=%DEFAULT_TOPICS_FILE_PATH%"

set "START_CELL="
set /p "START_CELL=Введите начальную ячейку в файле Excel [%DEFAULT_START_CELL%]: "
if not defined START_CELL set "START_CELL=%DEFAULT_START_CELL%"

set "START_FROM_LINE="
set /p "START_FROM_LINE=С какой темы начать обработку (номером) [%DEFAULT_START_FROM_LINE%]: "
if not defined START_FROM_LINE set "START_FROM_LINE=%DEFAULT_START_FROM_LINE%"

set "LINE_COUNT="
set /p "LINE_COUNT=На какой теме закончить обработку (номером) [%DEFAULT_LINE_COUNT%]: "
if not defined LINE_COUNT set "LINE_COUNT=%DEFAULT_LINE_COUNT%"


@REM echo.
@REM :GET_MODE
@REM DEPRECATED 
@REM set "MODE_INPUT="
@REM @REM echo Выберите режим обработки (введите 1 для в строчку, что угодно другое для столбца) [%DEFAULT_MODE%]:
@REM set /p "MODE_INPUT=Выберите режим обработки (введите 1 для в строчку, что угодно другое для столбца) [%DEFAULT_MODE%]: "
@REM if "!MODE_INPUT!"=="1" (
@REM     set "MODE=row"
@REM ) else (
@REM     set "MODE=!DEFAULT_MODE!"
@REM )
set "MODE=%DEFAULT_MODE%"

echo.
echo.
@REM DEPRECATED
@REM echo (?) Если все файлы находятся в одной папке, укажите ЕЁ для обеих категорий.
@REM echo.


set "TOPICS_FOLDER="
@REM DEPRECATED
@REM set /p "TOPICS_FOLDER=Введите имя папки для файлов тем [%DEFAULT_TOPICS_FOLDER%]: "
if not defined TOPICS_FOLDER set "TOPICS_FOLDER=%DEFAULT_TOPICS_FOLDER%"

@REM echo.
set "HOMEWORK_FOLDER="
@REM DEPRECATED
@REM set /p "HOMEWORK_FOLDER=Введите имя папки для файлов домашних заданий [%DEFAULT_HOMEWORK_FOLDER%]: "
if not defined HOMEWORK_FOLDER set "HOMEWORK_FOLDER=%DEFAULT_HOMEWORK_FOLDER%"

:: --- Escape backslashes for JSON compatibility ---
set "JSON_TOPICS_FILE_PATH=!TOPICS_FILE_PATH:\=\\!"
set "JSON_TOPICS_FOLDER=!TOPICS_FOLDER:\=\\!"
set "JSON_HOMEWORK_FOLDER=!HOMEWORK_FOLDER:\=\\!"

:: --- Create config.json ---
echo.
echo ---------------------------------------------------
echo Сохранение конфигурации...

(
    echo {
    echo     "automation_settings": {
    echo         "LINE_COUNT": !LINE_COUNT!,
    echo         "TOPICS_FILE_PATH": "!JSON_TOPICS_FILE_PATH!",
    echo         "START_CELL": "!START_CELL!",
    echo         "START_FROM_LINE": !START_FROM_LINE!,
    echo         "MODE": "!MODE!",
    echo         "TOPICS_FOLDER": "!JSON_TOPICS_FOLDER!",
    echo         "HOMEWORK_FOLDER": "!JSON_HOMEWORK_FOLDER!"
    echo     }
    echo }
) > tmp_config.json

:: Add credentials to the JSON file
python -c "import json; d=json.load(open('tmp_config.json')); d['credentials']={'login':'!LOGIN!','password':'!PASSWORD!'}; json.dump(d, open('config.json','w'), indent=4, ensure_ascii=False)" >nul 2>&1
del tmp_config.json

echo Конфигурация успешно сохранена.


@REM WAS PUT INTO SEPARATE SCRIPT


@REM :INSTALL_DEPS
@REM :: --- Install/Check Dependencies ---
@REM echo.
@REM echo ---------------------------------------------------
@REM echo (?) Необходимо при первом запуске.
@REM @REM set library_install="0"
@REM @REM set /p "library_install=Установить библиотки и зависимости? (1 для да, пропуск для нет): "
@REM @REM if not defined library_install set "library_install=n"

@REM @REM echo.
@REM set "library_install="
@REM set /p "library_install=Установить библиотки и зависимости? (1 для да, пропуск для нет): "
@REM if not defined library_install set "library_install=0"
@REM TIMEOUT /T 1 >nul 2>&1
@REM echo !library_install!
@REM echo "!library_install!"=="1"
@REM TIMEOUT /T 1 >nul 2>&1

@REM if "!library_install!"=="1" (
@REM     @REM winget install Python >nul 2>&1
@REM     @REM python -m pip install playwright pandas openpyxl >nul 2>&1
@REM     @REM python -m playwright install >nul 2>&1
@REM     @REM pip install playwright >nul 2>&1
@REM     @REM playwright install >nul 2>&1
@REM     @REM pip install openpyxl >nul 2>&1

@REM     TIMEOUT /T 2 >nul 2>&1
@REM     echo Установка библиотек и зависимостей...
@REM     echo (?) На это может потребоваться некоторое время.

@REM     :: Local Install Python
@REM     @REM winget install Python --silent --accept-source-agreements >nul 2>&1 apparantly doesn't work
@REM     python_installer.exe /passive InstallAllUsers=0 PrependPath=1 >nul 2>&1
@REM     echo Python установлен.
@REM     TIMEOUT /T 2 >nul 2>&1
@REM     echo.

@REM     :: Install libraries
@REM     python -m pip install playwright pandas openpyxl >nul 2>&1
@REM     echo Библиотеки установлены.
@REM     TIMEOUT /T 2 >nul 2>&1
@REM     echo.

@REM     :: Install only the WebKit engine
@REM     python -m playwright install webkit >nul 2>&1
@REM     echo Зависимости установлены.
@REM     TIMEOUT /T 2 >nul 2>&1
@REM     echo.
@REM )

@REM DEPRECATED
@REM :: Check if Python is installed
@REM python --version >nul 2>&1
@REM if errorlevel 1 (
@REM     winget install Python >nul 2>&1
@REM )
@REM :: Install libraries if not installed
@REM winget install Python >nul 2>&1
@REM python -m pip install playwright pandas  >nul 2>&1
@REM python -m playwright install >nul 2>&1
@REM pip install playwright >nul 2>&1
@REM playwright install >nul 2>&1
@REM pip install openpyxl >nul 2>&1


:LAUNCH_AUTOMATOR
:: --- Launch Automator ---
echo.
echo ---------------------------------------------------
echo Настройка завершена. Запускаем автоматизатор...
echo.
echo.

TIMEOUT /T 1 >nul 2>&1
python automator.py

:: Closing window
echo.
echo.
echo Кажется, браузер был закрыт. Нажмите любую клавишу для выхода...
echo.
echo.
pause >nul