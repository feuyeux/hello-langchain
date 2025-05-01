@echo off

REM Change to the directory where the script is located
cd /d "%~dp0"

call lc_win_env\Scripts\activate.bat
python hello_ollama_profile_png.py