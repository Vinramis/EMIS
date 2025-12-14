@echo off
CHCP 65001 >nul 
setlocal enabledelayedexpansion

SET PYTHON_SCRIPT_NAME=excel_extractor.py

REM ----------------------------------------------------------------------
REM ПРОВЕРКА АРГУМЕНТА: Если аргумент не 'pro', переходим к простому выводу.
REM ----------------------------------------------------------------------
IF /I "%~1" NEQ "pro" GOTO SIMPLE_OUTPUT

:PRO_OUTPUT
REM -----------------------------------------------------------
REM ⭐ БЛОК ДЛЯ ПРОФЕССИОНАЛОВ (Полный вывод и информация)
REM -----------------------------------------------------------
echo.
echo === [ПРОФИ] Запуск Интеллектуального буфера обмена ===
echo.

:GET_FILE_PRO
set "EXCEL_FILE_PATH="
echo.
echo ПЕРЕТАЩИТЕ сюда файл Excel (например, C:\путь\к\файлу.xlsx) и нажмите ENTER:
set /p "EXCEL_FILE_PATH="

REM Очистка ввода: удаление кавычек
set "CLEAN_PATH=%EXCEL_FILE_PATH:"=%"

if not defined CLEAN_PATH (
    echo [ОШИБКА] Путь к файлу не может быть пустым.
    goto :GET_FILE_PRO
)

REM Экранирование обратных слешей для корректного JSON
set "ESCAPED_PATH=%CLEAN_PATH:\=\\%"

REM Получение имени файла
for %%F in ("!CLEAN_PATH!") do set "FILENAME_ONLY=%%~nxF"
SET "CONFIG_FILE=!FILENAME_ONLY!.json"

REM -----------------------------------------------------------
REM ПРОВЕРКА КОНФИГУРАЦИИ (ПРО)
REM -----------------------------------------------------------
if exist "!CONFIG_FILE!" (
    echo [ИНФО] Файл конфигурации для '%FILENAME_ONLY%' найден. Пропуск настройки.
    goto :INSTALL_DEPS_PRO
)

echo [НАСТРОЙКА] Требуется первичная настройка для файла '%FILENAME_ONLY%'.
echo ---------------------------------------------------

:GET_CELL_PRO
set "START_CELL_REF="
set /p "START_CELL_REF=Введите начальную ячейку (например, C2): "
if not defined START_CELL_REF (
    echo [ОШИБКА] Начальная ячейка не может быть пустой.
    goto :GET_CELL_PRO
)

:GET_MODE_PRO
set "MODE_CHOICE="
echo.
echo [НАСТРОЙКА] Выберите режим работы (нажмите C или R и ENTER):
echo     [C] - По Столбцу (C2, C3, C4...)
echo     [R] - По Строке (C2, D2, E2...)
set /p "MODE_CHOICE=Ваш выбор [C/R]: "

REM Удаляем пробелы и ограничиваем ввод одним символом
set "MODE_CHOICE=%MODE_CHOICE:~0,1%"
set "MODE_CHOICE=%MODE_CHOICE: =%"

REM ⭐ ИСПРАВЛЕНИЕ: Линейная логика для стабильности
if /I "%MODE_CHOICE%"=="C" set "SELECTED_MODE=col" & GOTO MODE_DONE_PRO
if /I "%MODE_CHOICE%"=="R" set "SELECTED_MODE=row" & GOTO MODE_DONE_PRO

REM Если не 'C' и не 'R', то ошибка и повторный запрос
echo [ОШИБКА] Неверный выбор (%MODE_CHOICE%). Пожалуйста, введите C или R.
goto :GET_MODE_PRO

:MODE_DONE_PRO
REM Создание содержимого JSON
echo {                      > "!CONFIG_FILE!"
echo "excel_file": "!ESCAPED_PATH!",  >> "!CONFIG_FILE!"
echo "start_cell": "!START_CELL_REF!",   >> "!CONFIG_FILE!"
echo "mode": "!SELECTED_MODE!",          >> "!CONFIG_FILE!"
echo "sheet_name": 0                     >> "!CONFIG_FILE!"
echo }                                   >> "!CONFIG_FILE!"

echo [УСПЕХ] Конфигурация сохранена в '!CONFIG_FILE!'. (Режим: !SELECTED_MODE!)

:INSTALL_DEPS_PRO
REM -----------------------------------------------------------
REM УСТАНОВКА ЗАВИСИМОСТЕЙ (ПРО)
REM -----------------------------------------------------------
echo.
echo [ИНФО] Установка/Проверка необходимых библиотек...
python -m pip install pandas keyboard pyperclip
echo.

echo --------------------------------------------------------------------------------------------------
echo [ИНФО] Запуск скрипта. Используется конфигурация: !CONFIG_FILE!
echo --------------------------------------------------------------------------------------------------

REM Выполнение скрипта Python
python "!PYTHON_SCRIPT_NAME!" "!CONFIG_FILE!"

GOTO :END


:SIMPLE_OUTPUT
REM -----------------------------------------------------------
REM ⭐ БЛОК ДЛЯ ПРЕПОДАВАТЕЛЕЙ (Минимальный, чистый вывод)
REM -----------------------------------------------------------
echo.
echo === Запуск Интеллектуального буфера обмена ===
echo.

:GET_FILE_SIMPLE
set "EXCEL_FILE_PATH="
echo. 
echo ⭐ ПЕРЕТАЩИТЕ сюда файл Excel и нажмите ENTER:
set /p "EXCEL_FILE_PATH="

REM Очистка ввода: удаление кавычек
set "CLEAN_PATH=%EXCEL_FILE_PATH:"=%"

if not defined CLEAN_PATH (
    echo [ОШИБКА] Путь к файлу не может быть пустым.
    goto :GET_FILE_SIMPLE
)

REM Экранирование обратных слешей для корректного JSON
set "ESCAPED_PATH=%CLEAN_PATH:\=\\%"

REM Получение имени файла
for %%F in ("!CLEAN_PATH!") do set "FILENAME_ONLY=%%~nxF"
SET "CONFIG_FILE=!FILENAME_ONLY!.json"

REM -----------------------------------------------------------
REM ПРОВЕРКА КОНФИГУРАЦИИ (ПРОСТОЙ)
REM -----------------------------------------------------------
if exist "!CONFIG_FILE!" (
    goto :INSTALL_DEPS_SIMPLE
)

echo [НАСТРОЙКА] Введите начальную ячейку (например, C2):
set "START_CELL_REF="
set /p "START_CELL_REF="

if not defined START_CELL_REF (
    echo [ОШИБКА] Начальная ячейка не может быть пустой.
    pause >nul
    GOTO :END
)

:GET_MODE_SIMPLE
echo.
echo [НАСТРОЙКА] Выберите режим (C=Столбец, R=Строка):
set "MODE_CHOICE="
set /p "MODE_CHOICE=C/R: "

set "MODE_CHOICE=%MODE_CHOICE:~0,1%"
set "MODE_CHOICE=%MODE_CHOICE: =%"

REM ⭐ ИСПРАВЛЕНИЕ: Линейная логика для стабильности
if /I "%MODE_CHOICE%"=="C" set "SELECTED_MODE=col" & GOTO MODE_DONE_SIMPLE
if /I "%MODE_CHOICE%"=="R" set "SELECTED_MODE=row" & GOTO MODE_DONE_SIMPLE

REM Если не 'C' и не 'R', то ошибка и дефолтное значение
echo [ОШИБКА] Неверный выбор. Используется режим По Столбцу (C).
set "SELECTED_MODE=col"

:MODE_DONE_SIMPLE
REM Создание содержимого JSON
echo {                      > "!CONFIG_FILE!"
echo "excel_file": "!ESCAPED_PATH!",  >> "!CONFIG_FILE!"
echo "start_cell": "!START_CELL_REF!",   >> "!CONFIG_FILE!"
echo "mode": "!SELECTED_MODE!",          >> "!CONFIG_FILE!"
echo "sheet_name": 0                     >> "!CONFIG_FILE!"
echo }                                   >> "!CONFIG_FILE!"

:INSTALL_DEPS_SIMPLE
REM -----------------------------------------------------------
REM УСТАНОВКА ЗАВИСИМОСТЕЙ (Тихая)
REM -----------------------------------------------------------
echo [ИНФО] Установка необходимых библиотек... (может занять несколько минут, пожалуйста, не закрывайте это окно!)
python -m pip install pandas keyboard pyperclip >nul 2>&1

echo --------------------------------------------------------------------------------------------------
@REM echo [ИНФО] Скрипт запущен.
@REM echo Горячие клавиши: CTRL+V (Копировать далее) и ALT+C (Остановить).
@REM echo Подождите загрузки файла
@REM echo --------------------------------------------------------------------------------------------------

REM Выполнение скрипта Python
python "!PYTHON_SCRIPT_NAME!" "!CONFIG_FILE!"

GOTO :END


:END
echo.
echo Выполнение скрипта завершено.
echo Нажмите любую клавишу, чтобы закрыть это окно...
pause >nul
endlocal