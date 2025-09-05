@echo off
REM Create venv and install dependencies
python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Setup complete. To activate later: .venv\Scripts\activate.bat
pause
