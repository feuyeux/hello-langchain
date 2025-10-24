@echo off
REM Windows installation script for LangChain project

IF NOT EXIST lc_win_env (
    echo Setting up virtual environment for Windows...
    python -m venv lc_win_env
) ELSE (
    echo Virtual environment already exists, skipping creation...
)

call lc_win_env\Scripts\activate.bat

echo Upgrading pip...
call python -m pip install --upgrade pip

echo Installing dependencies...
call pip install -r requirements.txt

echo Setup complete!