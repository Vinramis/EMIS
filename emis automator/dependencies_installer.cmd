@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion





:: REDUNDANT
@REM :: Check for what we need
@REM python --version >nul 2>&1
@REM if errorlevel 1 (
@REM     goto :INSTALL_PYTHON
@REM ) else (
@REM     goto :INSTALL_DEPS
@REM )

@REM :: Install Python (local)
@REM :INSTALL_PYTHON
@REM ::     Convert the relative path to a FULL absolute path
@REM set "RELATIVE_PATH=python314"
@REM for %%i in ("%RELATIVE_PATH%") do set "PYTHON_FULL_PATH=%%~fi"

@REM echo.
@REM echo [ИНФО] Устанавливаем Python, пожалуйста, не закрывайте окно...
@REM python_installer.exe /passive InstallAllUsers=0 PrependPath=0 InstallLauncherAllUsers=0 Include_test=0 Include_doc=0 Include_pip=1 Shortcuts=1 TargetDir="!PYTHON_FULL_PATH!"
@REM echo [ИНФО] Python установлен.
@REM TIMEOUT /T 1 >nul 2>&1

@REM goto :INSTALL_DEPS

@REM :: Install dependencies
@REM :INSTALL_DEPS
@REM ::     Check for internet connection
@REM :CHECK_CONNECTION
@REM ping -n 1 google.com >nul 2>&1
@REM if errorlevel 1 (
@REM     echo [ОШИБКА] Нет подключения к интернету.
@REM     echo (?) Пожалуйста, проверьте подключение и нажмите Enter
@REM     pause >nul 2>&1
@REM     goto :CHECK_CONNECTION
@REM )
:: REDUNDANT



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





:: Install libraries
@REM :INSTALL_DEPS

@REM set "ROOT_DIR=%cd%"
@REM set "PYTHON_PATH="!ROOT_DIR!\python314\python""
@REM set "PIP_PATH="!ROOT_DIR!\python314\Scripts\pip""

set "PYTHON_PATH="python314\python""
set "PIP_PATH="python314\Scripts\pip""

echo.
echo [ИНФО] Обновляем библиотеки (всего 3), пожалуйста, не закрывайте окно...
echo.

echo (?) Библиотека Playwright нужна для работы с веб-браузером
!PIP_PATH! install playwright >nul
TIMEOUT /T 1 >nul
echo Библиотека Playwright обновлена. 

echo.

echo (?) Библиотека Pandas нужна для работы с файлами
!PIP_PATH! install pandas >nul
TIMEOUT /T 1 >nul
echo Библиотека Pandas обновлена.

echo.

echo (?) Библиотека OpenPyXL нужна для работы с Excel
!PIP_PATH! install openpyxl >nul
TIMEOUT /T 1 >nul
echo Библиотека OpenPyXL обновлена.

echo.
TIMEOUT /T 1 >nul
echo [ИНФО] Все библиотеки обновлены.

:: Install WebKit engine
echo.
echo.
echo [ИНФО] Обновляем зависимость (WebKit), пожалуйста, не закрывайте окно...
TIMEOUT /T 1 >nul
echo (?) Это самый долгий процесс
TIMEOUT /T 2 >nul
echo (?) WebKit - это браузер, который будет использоваться для автоматизации
TIMEOUT /T 1 >nul
!PYTHON_PATH! -m playwright install webkit >nul
echo [ИНФО] Зависимость обновлена.
echo.

:: Close window / Next process
exit