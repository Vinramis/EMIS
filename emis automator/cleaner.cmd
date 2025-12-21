@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: === EDIT START ===

set "PYTHON_PATH="python314""

:: Delete unnecessary files
echo [ОПТИМИЗАЦИЯ] Удаление лишних файлов...
rd /s /q "%PYTHON_PATH%\Doc" 2>nul
rd /s /q "%PYTHON_PATH%\tcl" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\test" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\idlelib" 2>nul
rd /s /q "%PYTHON_PATH%\LICENSE.txt" 2>nul

:: Delete all pycache folders recursively
for /d /r "%PYTHON_PATH%" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

:: === EDIT END ===

:: Close window
echo.
echo [ИНФО] Оптимизация завершена.
echo.
echo.
pause >nul