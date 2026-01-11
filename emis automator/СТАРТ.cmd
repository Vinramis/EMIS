@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion
:: Unarchived check
if not exist "components\" (
    color 0c
    echo Вы запустили программу неправильно. Пожалуйста, следуйте инструкции.
    set /p dummy=Нажмите Enter для выхода...
    exit
)

:: Activate fullscreen mode
if not "%1"=="max" start /MAX cmd /c %0 max & exit/b

:: Set title
title Автоматизатор EMIS v2.7.1

:: Definitions
set "PYTHON="components\python314\python""
set "PLAYWRIGHT=!PYTHON! -m playwright"
@REM for /F "delims=#" %%a in ('prompt #$E# ^& for %%a in ^(1^) do rem') do set "ESC=%%a"
@REM syntax:
@REM echo %ESC%[31mThis text is Red!%ESC%[0m
@REM colors:
@REM 30m = Black
@REM 31m = Red
@REM 32m = Green
@REM 33m = Yellow
@REM 34m = Blue
@REM 35m = Magenta
@REM 36m = Cyan
@REM 37m = White

:: Welcome user
echo.
echo.
echo.
echo === Добро пожаловать в Автоматизатор EMIS! ===
echo.
echo.
echo.

:: Sequence
echo Проверяем подключение...
!PYTHON! components/connection_check.py internet

echo.

echo Подготавливаем компоненты...
!PLAYWRIGHT! install chromium >nul

echo.

echo Входим в EMIS...
!PYTHON! components/preparator.py --login
!PYTHON! components/connection_check.py emis cookies.json

echo.

echo Подготавливаем данные...
del components/input_data.json
!PYTHON! components/preparator.py

echo.

@REM echo Режимы автоматизации:
@REM echo     1 - План предмета (темы, классные и домашние работы; на вкладке "Mavzular" / "Темы")
@REM echo     2 - План группы (темы; на вкладке "Guruhlar" / "Группы")
@REM echo.
@REM choice /C:12 /N /M "Выберите режим (нужная цифра): "
@REM set mode=%errorlevel%
@REM :: only take one digit, when one digit is entered, automatically take it (no enter)

set mode=1

if !mode! == 1 !PYTHON! components/automator.py
if !mode! == 2 !PYTHON! components/enterer.py

:: Closing window
:exit
timeout /t 2 /nobreak >nul
echo.
echo.
echo Кажется, браузер закрыт. Нажмите Enter для выхода...
echo (?) Можно просто закрыть это окно
echo.
echo.
echo.
pause >nul