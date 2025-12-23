@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: Activate fullscreen mode
if not "%1"=="max" start /MAX cmd /c %0 max & exit/b
TITLE Автоматизатор EMIS v0.6.6

:: Welcome
echo.
echo.
echo.
echo === Добро пожаловать в Автоматизатор EMIS! ===
echo.
echo.
echo.


@REM DEPRECATED
@REM :: Update dependencies
@REM echo. & TIMEOUT /T 1 >nul
@REM echo ---------------------------------------------------
@REM echo Обновление компонентов в отдельном окне...
@REM TIMEOUT /T 1 >nul
@REM echo (?) Если вы закроете второе окно, на появившийся здесь вопрос ответьте "N"
@REM TIMEOUT /T 1 >nul

@REM start /wait dependencies_installer.cmd
@REM if errorlevel 0 (
@REM     echo [ИНФО] Компоненты обновлены успешно
@REM ) else (
@REM     echo [ИНФО] Компоненты не обновлены
@REM )
@REM TIMEOUT /T 1 >nul


:: Setup
::     To be separated into a different file from setup_automator.cmd

:: Run
setup_automator.cmd