@echo off

REM Change to the directory where the script is located
cd /d "%~dp0"

REM Load environment variables from external file
call .env.bat

call go run infer.go openai.go