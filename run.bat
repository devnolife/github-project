@echo off
REM GitHub Proposal Generator - Windows Run Script

echo Starting GitHub Proposal Generator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing/updating requirements...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo Warning: .env file not found
    echo Please copy .env.example to .env and configure your settings
    echo.
    pause
)

REM Run the application
echo.
echo Starting application...
echo.
python src\main.py

pause
