@echo off

REM Change to the directory where the script is located
cd /d "%~dp0"
call .env.bat
call node ollama.js