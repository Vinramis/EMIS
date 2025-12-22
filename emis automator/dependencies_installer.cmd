@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: Title
TITLE Менеджер зависимостей



:: Doesn't work as intended
@REM :: Check for internet connection
@REM :CHECK_CONNECTION
@REM ping 8.8.8.8 -n 1 | find "TTL=" >nul
@REM if errorlevel 0 (
@REM     goto :INSTALL_DEPS
@REM ) else (
@REM     goto :ERROR_MESSAGE
@REM )

@REM :ERROR_MESSAGE
@REM echo [ОШИБКА] Нет подключения к интернету. 
@REM echo (?) Пожалуйста, проверьте подключение и нажмите Enter
@REM pause >nul
@REM goto :CHECK_CONNECTION



set "PYTHON_PATH="python314\python""
set "PIP_PATH="python314\Scripts\pip""

echo.
echo [ИНФО] Обновляем компоненты (всего 3)...
echo (?) Можете закрыть это окно, если обновление занимает слишком много времени
echo.

echo (?) Библиотека Playwright нужна для работы с веб-браузером
!PIP_PATH! install playwright --no-warn-script-location >nul
TIMEOUT /T 1 >nul
echo Библиотека Playwright обновлена. 

echo.

echo (?) Библиотека OpenPyXL нужна для работы с Excel
!PIP_PATH! install openpyxl --no-warn-script-location >nul
TIMEOUT /T 1 >nul
echo Библиотека OpenPyXL обновлена.

echo.

echo (?) WebKit - это браузер, который будет использоваться для автоматизации
!PYTHON_PATH! -m playwright install webkit >nul
TIMEOUT /T 1 >nul
echo WebKit обновлен.

echo.

:: Close window / Next process
echo.
echo (?) Обновление завершено!
echo [ИНФО] Закрываем окно...
echo.
TIMEOUT /T 3 >nul
exit