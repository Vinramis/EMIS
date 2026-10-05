@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
chdir /d "%~dp0"

:: Unarchived check
if not exist "components\" goto :archived_exit

@REM :: Activate minisize mode
@REM if not "%1"=="min" start /MIN cmd /c %0 min & exit/b

:: Activate fullscreen mode
if not "%1"=="max" start /MAX cmd /c %0 max & exit/b

@REM :: Set title
@REM title Автоматизатор EMIS v2.7.2

:: Definitions
set "PYTHON="components\python314\python""
@REM set "PLAYWRIGHT=!PYTHON! -m playwright"
@REM set "CURRENT_DIR=%cd%"
@REM set "INPUT_DATA="%CURRENT_DIR%\components\input_data.json""
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

timeout /t 1 /nobreak >nul
!PYTHON! components/enterer.py


@REM :: Welcome user
@REM echo.
@REM echo.
@REM echo.
@REM echo === Добро пожаловать в Автоматизатор EMIS! ===
@REM echo.
@REM echo.
@REM echo.

@REM :: Sequence
@REM echo Проверяем подключение...
@REM !PYTHON! components/connection_check.py internet

@REM echo.

@REM echo Подготавливаем компоненты... (это может занять некоторое время)
@REM !PLAYWRIGHT! install chromium >nul 2>&1

@REM echo.

@REM echo Входим в EMIS...
@REM !PYTHON! components/preparator.py --login
@REM if errorlevel 1 goto :error_exit
@REM !PYTHON! components/connection_check.py emis cookies.json
@REM if errorlevel 1 goto :error_exit

@REM echo.

@REM echo Подготавливаем данные...
@REM del %INPUT_DATA%
@REM !PYTHON! components/preparator.py
@REM if errorlevel 1 goto :error_exit

@REM echo.

@REM @REM echo Режимы автоматизации:
@REM @REM echo     1 - План предмета (темы, классные и домашние работы; на вкладке "Mavzular" / "Темы")
@REM @REM echo     2 - План группы (темы; на вкладке "Guruhlar" / "Группы")
@REM @REM echo.
@REM @REM choice /C:12 /N /M "Выберите режим (нужная цифра): "
@REM @REM set mode=%errorlevel%
@REM @REM :: only take one digit, when one digit is entered, automatically take it (no enter)

@REM set mode=1

@REM if !mode! == 1 !PYTHON! components/automator.py
@REM if !mode! == 2 !PYTHON! components/enterer.py

:: Closing window
:successfull_exit
timeout /t 2 /nobreak >nul
echo.
echo.
echo Кажется, браузер закрыт. Нажмите Enter для выхода...
echo (?) Можно просто закрыть это окно
echo.
echo.
echo.
pause >nul
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
color 0c
echo Вы запустили программу не распаковав архив. Пожалуйста, вернитесь к инструкции.
echo Нажмите Enter для выхода...
echo (?) Можно просто закрыть это окно
echo.
echo.
echo.
pause >nul
goto :empty_exit

:empty_exit
exit