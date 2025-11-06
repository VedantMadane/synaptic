@echo off
REM Setup script for NautilusTrader Backtest (Windows)
REM Run with: setup.bat

echo ========================================
echo NautilusTrader Backtest Setup
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
echo.

REM Run tests
echo Running tests...
python test_backtest.py
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the backtest:
echo    1. Activate environment: venv\Scripts\activate.bat
echo    2. Run backtest: python run_backtest.py
echo.
echo To deactivate environment:
echo    deactivate
echo.

pause
