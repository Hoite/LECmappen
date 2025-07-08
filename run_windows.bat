@echo off
REM LEC Mappen Generator - Windows Wrapper
REM Controleert of Python beschikbaar is en start het script

echo LEC Mappen Generator
echo.

REM Controleer of Python beschikbaar is
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is niet geinstalleerd of niet gevonden in PATH
    echo Download Python van https://python.org
    pause
    exit /b 1
)

REM Start het Python script in interactieve modus
python lec_mappen.py --interactive

pause
