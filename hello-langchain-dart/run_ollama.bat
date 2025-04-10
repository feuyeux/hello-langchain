@echo off
REM Change to the directory where the script is located
cd /d "%~dp0"

REM Load environment variables from external file
call .env.bat

REM Run Dart commands
call dart pub get
call dart ollama.dart