@echo off

REM Change to the directory where the script is located
cd /d "%~dp0"

REM Set console to UTF-8 encoding
chcp 65001

call lc_win_env\Scripts\activate.bat
which python
python hello_profile.py