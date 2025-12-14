@REM This script demonstrates switching between the primary and alternate screen buffers in a terminal.
@echo off

:: 1. Initial Content on the Primary Screen
echo ==================================================
echo   [STEP 1] PRIMARY SCREEN: Normal terminal view.
echo   This content will be PERMANENTLY cleared in 3 seconds.
echo ==================================================

timeout /t 3 /nobreak > nul

:: 2. Clear the screen (The 'Disappear' Magic)
cls

:: 3. Content on the temporary 'screen'
echo **************************************************
echo         [STEP 2] TEMPORARY SCREEN IS ACTIVE
echo **************************************************
echo The previous history has been cleared from the buffer.
echo This screen will remain active until you press a key.

:: Pause until a key is pressed
pause > nul

:: 4. Clear the screen one final time before exiting
cls

:: The command prompt returns here.



@echo off
setlocal enabledelayedexpansion

:: --- Define the Carriage Return (CR) character ---
:: This trick uses a prompt's ability to hold special characters.
for /f %%a in ('copy /Z "%~dpf0" nul') do set "CR=%%a"

set "SPINNERS=|/-\"
set "RUN_TIME=5"  :: Run the spinner for 5 seconds

echo.
echo Processing, please wait...

set "START_TIME=%TIME%"
call :GetSeconds start_sec "%START_TIME%"
set /a END_SEC = start_sec + RUN_TIME

set /a "i=0"
:LOOP
    set "CURRENT_TIME=%TIME%"
    call :GetSeconds current_sec "%CURRENT_TIME%"
    
    if %current_sec% geq %END_SEC% goto :END_LOOP
    
    :: 1. Get the next spinner character
    set /a "CHAR_INDEX=!i! %% 4"
    set "CHAR=!SPINNERS:~%CHAR_INDEX%,1!"
    
    :: 2. Print the character, followed by the Carriage Return (CR)
    :: The carriage return moves the cursor back to the start of the line.
    <nul set /p "=!CHAR!!CR!"
    
    :: 3. Wait a short period (this is an approximation of 100ms delay)
    @REM ping -n 1 -w 100
    timeout /t 100m > nul
    @REM powershell -Command "Start-Sleep -Milliseconds 1"


    set /a "i+=1"
    goto :LOOP

:END_LOOP
:: 4. Final cleanup: Print spaces to overwrite the spinner, and a final message
<nul set /p "= Done!   "
echo.
echo.
goto :EOF


:: --- Subroutine to convert HH:MM:SS.XX time to total seconds ---
:GetSeconds
    set "t=%~2"
    set /a "h=10%t:~0,2%%%100"
    set /a "m=10%t:~3,2%%%100"
    set /a "s=10%t:~6,2%%%100"
    set /a %1 = h*3600 + m*60 + s
    exit /b