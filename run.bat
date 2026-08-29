@echo off
REM YouTube Auto-Uploader - Windows Batch Starter

echo.
echo ========================================
echo YouTube Auto-Uploader
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo [2/3] Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [3/3] Starting server...
echo.
echo ========================================
echo Server is starting...
echo Wait for: "Application startup complete"
echo Then open: http://localhost:8000
echo ========================================
echo.

python main.py

pause
