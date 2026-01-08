@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: Title
TITLE Менеджер зависимостей

:: Set location to python, then of this file
set "PYTHON="python314\python""
chdir /d %~dp0
for /F "delims=#" %%a in ('prompt #$E# ^& for %%a in ^(1^) do rem') do set "ESC=%%a"
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

echo.
echo %ESC%[36m[ИНФО] Обновляем компоненты...%ESC%[0m
echo (?) Можете закрыть это окно, если обновление занимает слишком много времени

echo.

echo (?) Библиотека Playwright нужна для работы с веб-браузером
!PYTHON! -m pip install playwright --no-warn-script-location >nul
@REM timeout /T 1 >nul
echo Библиотека Playwright обновлена. 

echo.

echo (?) Библиотека OpenPyXL нужна для работы с Excel
!PYTHON! -m pip install openpyxl --no-warn-script-location >nul
@REM timeout /T 1 >nul
echo Библиотека OpenPyXL обновлена.

echo.

echo (?) Браузер будет использоваться для автоматизации
!PYTHON! -m playwright install >nul
@REM timeout /T 1 >nul
echo Браузер обновлен.

echo.

:: Close window / Next process
echo.
echo (?) Обновление завершено!
echo [ИНФО] Закрываем окно...
echo.
pause >nul
exit