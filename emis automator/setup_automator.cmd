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


:: --- Check for existing config file ---
if exist "config.json" (
    echo [ИНФО] Найден существующий файл 'config.json'.
    set "USE_EXISTING="
    set /p "USE_EXISTING=Вы хотите использовать эту конфигурацию? (введите 1 для нет, пропуск для да): "
    
    if "!USE_EXISTING!"=="1" (
        echo.
        echo Перенастройка параметров...
        goto :RECONFIGURE
    ) else (
        echo.
        echo Используется существующая конфигурация.
        goto :INSTALL_DEPS
    )
)

echo.
echo [ИНФО] Файл 'config.json' не найден. Запуск первоначальной настройки.
echo.

:CREATE_NEW_CONFIG
echo --- Учетные данные ---
set /p "LOGIN=Введите ваш логин EMIS: "
set /p "PASSWORD=Введите ваш пароль EMIS: "
echo.
goto :GATHER_SETTINGS

:RECONFIGURE
echo --- Учетные данные (оставьте пустым, чтобы сохранить существующие) ---
echo (?) Существующие учетные данные будут показаны в квадратных скобках.
:: Try to parse existing credentials to use as defaults
for /f "tokens=2 delims=:," %%a in ('findstr /R /C:"\"login\"" "config.json"') do set "EXISTING_LOGIN=%%~a"
for /f "tokens=2 delims=:," %%a in ('findstr /R /C:"\"password\"" "config.json"') do set "EXISTING_PASSWORD=%%~a"
:: Remove quotes
set "EXISTING_LOGIN=!EXISTING_LOGIN:"=!"
set "EXISTING_PASSWORD=!EXISTING_PASSWORD:"=!"
:: Test output
@REM echo Existing login: '!EXISTING_LOGIN!'
@REM echo Existing password: '!EXISTING_PASSWORD!'
:: Remove leading spaces
set "EXISTING_LOGIN=!EXISTING_LOGIN:~1!"
set "EXISTING_PASSWORD=!EXISTING_PASSWORD:~1!"
:: test output
@REM echo Existing login: '!EXISTING_LOGIN!'
@REM echo Existing password: '!EXISTING_PASSWORD!'


set /p "LOGIN=Логин [!EXISTING_LOGIN!]: "
set /p "PASSWORD=Пароль [!EXISTING_PASSWORD!]: "
if not defined LOGIN set LOGIN=!EXISTING_LOGIN!
if not defined PASSWORD set "PASSWORD=!EXISTING_PASSWORD!"
echo.

:GATHER_SETTINGS
echo --- Параметры автоматизации (нажмите ENTER для значений по умолчанию) ---
echo (?) Значения по умолчанию будут показаны в квадратных скобках.
echo.
set DEFAULT_LINE_COUNT=3
set "DEFAULT_TOPICS_FILE_PATH=КТП.xlsx"
set "DEFAULT_START_CELL=B6"
set DEFAULT_START_FROM_LINE=1
set "DEFAULT_MODE=col"
set "DEFAULT_TOPICS_FOLDER=КЛ"
set "DEFAULT_HOMEWORK_FOLDER=ДЗ"

echo.
set "TOPICS_FILE_PATH="
set /p "TOPICS_FILE_PATH=Введите путь к файлу Excel с темами [%DEFAULT_TOPICS_FILE_PATH%]: "
if not defined TOPICS_FILE_PATH set "TOPICS_FILE_PATH=%DEFAULT_TOPICS_FILE_PATH%"

echo.
set "START_CELL="
set /p "START_CELL=Введите начальную ячейку в файле Excel [%DEFAULT_START_CELL%]: "
if not defined START_CELL set "START_CELL=%DEFAULT_START_CELL%"

echo.
set "START_FROM_LINE="
set /p "START_FROM_LINE=С какой темы начать обработку (номером) [%DEFAULT_START_FROM_LINE%]: "
if not defined START_FROM_LINE set "START_FROM_LINE=%DEFAULT_START_FROM_LINE%"

set "LINE_COUNT="
set /p "LINE_COUNT=На какой теме закончить обработку (номером) [%DEFAULT_LINE_COUNT%]: "
if not defined LINE_COUNT set "LINE_COUNT=%DEFAULT_LINE_COUNT%"


echo.
:GET_MODE
@REM DEPRECATED 
@REM set "MODE_INPUT="
@REM @REM echo Выберите режим обработки (введите 1 для в строчку, что угодно другое для столбца) [%DEFAULT_MODE%]:
@REM set /p "MODE_INPUT=Выберите режим обработки (введите 1 для в строчку, что угодно другое для столбца) [%DEFAULT_MODE%]: "
@REM if "!MODE_INPUT!"=="1" (
@REM     set "MODE=row"
@REM ) else (
@REM     set "MODE=!DEFAULT_MODE!"
@REM )
set "MODE_INPUT=%DEFAULT_MODE%"

echo.
echo.
@REM DEPRECATED
@REM echo (?) Если все файлы находятся в одной папке, укажите ЕЁ для обеих категорий.
@REM echo.
set "TOPICS_FOLDER="
set /p "TOPICS_FOLDER=Введите имя папки для файлов тем [%DEFAULT_TOPICS_FOLDER%]: "
if not defined TOPICS_FOLDER set "TOPICS_FOLDER=%DEFAULT_TOPICS_FOLDER%"

echo.
set "HOMEWORK_FOLDER="
set /p "HOMEWORK_FOLDER=Введите имя папки для файлов домашних заданий [%DEFAULT_HOMEWORK_FOLDER%]: "
if not defined HOMEWORK_FOLDER set "HOMEWORK_FOLDER=%DEFAULT_HOMEWORK_FOLDER%"

:: --- Escape backslashes for JSON compatibility ---
set "JSON_TOPICS_FILE_PATH=!TOPICS_FILE_PATH:\=\\!"
set "JSON_TOPICS_FOLDER=!TOPICS_FOLDER:\=\\!"
set "JSON_HOMEWORK_FOLDER=!HOMEWORK_FOLDER:\=\\!"

:: --- Create config.json ---
echo.
echo ---------------------------------------------------
echo Создание файла 'config.json'...

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
python -c "import json; d=json.load(open('tmp_config.json')); d['credentials']={'login':'!LOGIN!','password':'!PASSWORD!'}; json.dump(d, open('config.json','w'), indent=4, ensure_ascii=False)"
del tmp_config.json

echo Файл 'config.json' успешно создан.
echo.

:INSTALL_DEPS
:: --- Install/Check Dependencies ---
echo.
echo ---------------------------------------------------
echo (?) Необходимо при первом запуске установить библиотки и зависимости.
set "library_install=0"
set /p "library_install=Установить библиотки и зависимости? (1 для да, пропуск для нет): "
@REM if not defined library_install set "library_install=n"
if "!library_install!"=="1" (
    @REM winget install Python >nul 2>&1
    @REM python -m pip install playwright pandas openpyxl >nul 2>&1
    @REM python -m playwright install >nul 2>&1
    @REM pip install playwright >nul 2>&1
    @REM playwright install >nul 2>&1
    @REM pip install openpyxl >nul 2>&1


    :: Install Python
    winget install Python --silent --accept-source-agreements >nul 2>&1

    :: Install libraries
    python -m pip install playwright pandas openpyxl >nul 2>&1

    :: Install only the Safari/WebKit engine
    python -m playwright install webkit >nul 2>&1

    echo Зависимости установлены.
)

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

echo ---------------------------------------------------
echo.
echo Настройка завершена! Запускаем автоматизатор...
echo.

python automator.py

:: Closing window
endlocal
exit /b 0