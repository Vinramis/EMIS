@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Unarchived check
chdir /d "%~dp0"
if not exist "components\" goto :archived_exit

:: Definitions
set "PYTHON="components\python314\python""
set "PYTHONW="components\python314\pythonw""
set PLAYWRIGHT_BROWSERS_PATH=0

:: Open GUI
start "" !PYTHONW! components/GUI.py
if not errorlevel 0 (goto :error_exit)
goto :empty_exit



:error_exit
echo.
echo.
echo Что-то пошло не так. Нажмите Enter для выхода...
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