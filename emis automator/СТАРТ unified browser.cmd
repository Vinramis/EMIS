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
set PLAYWRIGHT_BROWSERS_PATH=0


:: Python transition
!PYTHON! components/startup_sequence.py
pause >nul
goto :empty_exit


:: Exits
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