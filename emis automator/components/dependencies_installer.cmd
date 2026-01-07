@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: Title
TITLE Менеджер зависимостей

:: Set location to python, then of this file
set "PYTHON="python314\python""
chdir /d %~dp0

echo.
echo [ИНФО] Обновляем компоненты...
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