@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Unarchived check
chdir /d "%~dp0"
if not exist "components\" goto :archived_exit

:: Activate fullscreen mode
if not "%1"=="max" start /MAX cmd /c %0 max & exit/b
title Автоматизатор EMIS

:: Definitions
set "PYTHON="components\python314\python""
set "PLAYWRIGHT=!PYTHON! -m playwright"
set PLAYWRIGHT_BROWSERS_PATH=0

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
!PYTHON! components/preparator.py

echo.

echo Режимы автоматизации:
echo     1 - План предмета (темы, классные и домашние работы; на вкладке "Mavzular" / "Темы")
echo     2 - План группы (темы; на вкладке "Guruhlar" / "Группы")
echo.
choice /C:12 /N /M "Выберите режим (нужная цифра): "
set mode=%errorlevel%
@REM :: only take one digit, when one digit is entered, automatically take it (no enter)

echo.
echo.

if !mode! == 1 (
    echo Выбиран режим "План предмета"...
    !PYTHON! components/automator.py
) else if !mode! == 2 (
    echo Выбиран режим "План группы"...
    !PYTHON! components/enterer.py
)
goto :exit



:exit
echo.
echo.
echo Кажется, браузер закрыт. Нажмите Enter для выхода...
echo (?) Можно просто закрыть это окно
echo.
echo.
echo.
pause >nul
goto :empty_exit

:archived_exit
echo.
echo.
color 0c & echo Вы запустили программу не распаковав архив. Пожалуйста, вернитесь к инструкции.
echo Нажмите Enter для выхода...
echo (?) Можно просто закрыть это окно
echo.
echo.
echo.
pause >nul
goto :empty_exit

:empty_exit
exit