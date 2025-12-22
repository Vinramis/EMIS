@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: --- Activate fullscreen mode ---
if not "%1"=="max" start /MAX cmd /c %0 max & exit/b
TITLE Автоматизатор EMIS v0.6.5

:: --- Welcome ---
echo.
echo.
echo. & TIMEOUT /T 1 >nul
echo === Настройка автоматизатора EMIS ===
echo. & TIMEOUT /T 1 >nul
echo Этот скрипт поможет настроить параметры для автоматизации, затем запустит её
echo.
echo.

:: --- Update dependencies ---
echo. & TIMEOUT /T 1 >nul
echo ---------------------------------------------------
echo Обновление компонентов в отдельном окне...
echo (?) Если вы закроете окно, на появившийся вопрос ответьте "N"
start /wait dependencies_installer.cmd
if errorlevel 0 (
    echo [ИНФО] Компоненты обновлены успешно
) else (
    echo [ИНФО] Компоненты не обновлены
)
echo. & TIMEOUT /T 1 >nul

:: --- Setup ---
:: To be separated into a different file
setup_automator.cmd
