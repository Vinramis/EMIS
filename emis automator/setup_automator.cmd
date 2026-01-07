@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: Activate fullscreen mode
if not "%1"=="max" start /MAX cmd /c %0 max & exit/b
:: Define python path
set "PYTHON="components\python314\python""
set "PLAYWRIGHT=!PYTHON! -m playwright"
:: Set title
title Автоматизатор EMIS v2.5
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
!PLAYWRIGHT! install

echo.

echo Входим в EMIS...
!PYTHON! components/preparator.py --login
!PYTHON! components/connection_check.py all cookies.json
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

if !mode! == 1 (
    !PYTHON! components/automator.py
) else if !mode! == 2 (
    !PYTHON! components/enterer.py
)


:: Closing window
:exit
echo.
echo.
echo Кажется, браузер закрыт. Нажмите Enter для выхода...
echo (?) Можно просто закрыть это окно
echo.
echo.
echo.
pause >nul