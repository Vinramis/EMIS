@echo off
CHCP 65001 >nul
setlocal enabledelayedexpansion

:: === EDIT START ===

set "PYTHON_PATH="python314""
echo [ОПТИМИЗАЦИЯ] Удаление лишних файлов...

:: Block 1. Delete unnecessary files
rd /s /q "%PYTHON_PATH%\Doc" 2>nul
rd /s /q "%PYTHON_PATH%\tcl" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\test" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\idlelib" 2>nul
rd /s /q "%PYTHON_PATH%\LICENSE.txt" 2>nul

:: Block 2. Delete all pycache folders recursively
for /d /r "%PYTHON_PATH%" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r "%PYTHON_PATH%" %%d in (pycache) do @if exist "%%d" rd /s /q "%%d"

:: Block 3. Delete large unnecessary libraries
rd /s /q "%PYTHON_PATH%\Lib\tkinter" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\unittest" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\sqlite3" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\lib2to3" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\dbm" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\curses" 2>nul
rd /s /q "%PYTHON_PATH%\Lib\ensurepip" 2>nul

:: Block 4. Clear garbage inside installed libraries (Pandas/Playwright)
for /d /r "%PYTHON_PATH%\Lib\site-packages" %%d in (*.dist-info) do rd /s /q "%%d" 2>nul

:: === EDIT END ===

:: Close window
echo.
echo [ИНФО] Оптимизация завершена.
echo.
echo.
@REM pause >nul