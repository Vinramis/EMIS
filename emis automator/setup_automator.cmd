@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion
:: Define python path
set "PYTHON="python314\python""

:: --- Check for existing config file ---
echo.
echo ---------------------------------------------------
echo Проверка конфигурации...
if exist "config.json" (
    set "USE_EXISTING="
    set /p "USE_EXISTING=Конфигурация уже существует, использовать её? (введите 1 и нажмите Enter для нет или оставьте пустым и нажмите Enter для да): "
    TIMEOUT /T 1 >nul
    
    if "!USE_EXISTING!"=="1" (
        echo Перенастройка параметров...
        goto :RECONFIGURE
    ) else (
        echo Используется существующая конфигурация.
        goto :LAUNCH_AUTOMATOR
    )
) else (
    echo.
    echo --- Учетные данные ---

    TIMEOUT /T 1 >nul
    set /p "LOGIN=Введите ваш логин EMIS: "

    TIMEOUT /T 1 >nul
    set /p "PASSWORD=Введите ваш пароль EMIS: "
)
goto :GATHER_SETTINGS


:RECONFIGURE
echo.
echo --- Учетные данные ---
echo (?) Оставьте пустым и нажмите Enter, чтобы сохранить существующие
echo (?) Существующие учетные данные показаны в квадратных скобках
echo.

:: Parsing existing credentials
for /f "tokens=2 delims=:," %%a in ('findstr /R /C:"\"login\"" "config.json"') do set "EXISTING_LOGIN=%%~a"
for /f "tokens=2 delims=:," %%a in ('findstr /R /C:"\"password\"" "config.json"') do set "EXISTING_PASSWORD=%%~a"
:: Remove quotes
set "EXISTING_LOGIN=!EXISTING_LOGIN:"=!"
set "EXISTING_PASSWORD=!EXISTING_PASSWORD:"=!"
:: Remove leading spaces
set "EXISTING_LOGIN=!EXISTING_LOGIN:~1!"
set "EXISTING_PASSWORD=!EXISTING_PASSWORD:~1!"

set /p "LOGIN=Введите ваш логин EMIS [!EXISTING_LOGIN!]: "
TIMEOUT /T 1 >nul
set /p "PASSWORD=Введите ваш пароль EMIS [!EXISTING_PASSWORD!]: "
TIMEOUT /T 1 >nul
if not defined LOGIN set "LOGIN=!EXISTING_LOGIN!"
if not defined PASSWORD set "PASSWORD=!EXISTING_PASSWORD!"

:GATHER_SETTINGS
@REM DEPRECATED
@REM echo.
@REM echo.
@REM echo --- Параметры автоматизации ---
@REM echo (?) Оставьте пустым и нажмите Enter, чтобы сохранить значения по умолчанию
@REM echo (?) Значения по умолчанию показаны в квадратных скобках
@REM echo.

set "DEFAULT_TOPICS_FILE_PATH=КТП.xlsx"
set "DEFAULT_START_CELL=B6"
set DEFAULT_START_FROM_LINE=1
set DEFAULT_END_ON_LINE=6
set "DEFAULT_MODE=col"
set "DEFAULT_TOPICS_FOLDER=КЛ"
set "DEFAULT_HOMEWORK_FOLDER=ДЗ"

set "TOPICS_FILE_PATH="
@REM DEPRECATED
@REM set /p "TOPICS_FILE_PATH=Введите путь к файлу Excel с темами [%DEFAULT_TOPICS_FILE_PATH%]: "
if not defined TOPICS_FILE_PATH set "TOPICS_FILE_PATH=%DEFAULT_TOPICS_FILE_PATH%"

set "START_CELL="
@REM DEPRECATED
@REM set /p "START_CELL=Введите начальную ячейку в файле Excel [%DEFAULT_START_CELL%]: "
if not defined START_CELL set "START_CELL=%DEFAULT_START_CELL%"

set "START_FROM_LINE="
@REM DEPRECATED
@REM set /p "START_FROM_LINE=С какой темы начать обработку (номером) [%DEFAULT_START_FROM_LINE%]: "
if not defined START_FROM_LINE set "START_FROM_LINE=%DEFAULT_START_FROM_LINE%"

set "END_ON_LINE="
@REM DEPRECATED
@REM set /p "END_ON_LINE=На какой теме закончить обработку (номером) [%DEFAULT_END_ON_LINE%]: "
if not defined END_ON_LINE set "END_ON_LINE=%DEFAULT_END_ON_LINE%"

set "MODE_INPUT="
@REM DEPRECATED 
@REM set /p "MODE_INPUT=Выберите режим обработки (введите 1 для в строчку, что угодно другое для столбца) [%DEFAULT_MODE%]: "
@REM if "!MODE_INPUT!"=="1" (
@REM     set "MODE=row"
@REM ) else (
@REM     set "MODE=!DEFAULT_MODE!"
@REM )
set "MODE=%DEFAULT_MODE%"


set "TOPICS_FOLDER="
@REM DEPRECATED
@REM set /p "TOPICS_FOLDER=Введите имя папки для файлов классных работ [%DEFAULT_TOPICS_FOLDER%]: "
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
    echo         "TOPICS_FILE_PATH": "!JSON_TOPICS_FILE_PATH!",
    echo         "START_CELL": "!START_CELL!",
    echo         "START_FROM_LINE": !START_FROM_LINE!,
    echo         "END_ON_LINE": !END_ON_LINE!,
    echo         "MODE": "!MODE!",
    echo         "TOPICS_FOLDER": "!JSON_TOPICS_FOLDER!",
    echo         "HOMEWORK_FOLDER": "!JSON_HOMEWORK_FOLDER!"
    echo     }
    echo }
) > tmp_config.json

:: Add credentials to the JSON file
!PYTHON! -c "import json; d=json.load(open('tmp_config.json')); d['credentials']={'login':'!LOGIN!','password':'!PASSWORD!'}; json.dump(d, open('config.json','w'), indent=4, ensure_ascii=False)" >nul
del tmp_config.json

TIMEOUT /T 1 >nul
echo Конфигурация успешно сохранена.


:LAUNCH_AUTOMATOR
:: --- Launch Automator ---
echo.
echo ---------------------------------------------------
echo Настройка завершена. Запускаем автоматизатор...
echo.
echo.

!PYTHON! automator.py

:: Closing window
echo.
echo.
echo Кажется, браузер закрыт. Нажмите Enter для выхода...
echo (?) Или можно просто закрыть это окно
echo.
echo.
echo.
pause >nul