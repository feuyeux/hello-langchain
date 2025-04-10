@echo off

REM Change to the directory where the script is located
cd /d "%~dp0"

call cargo fmt
call cargo build
call cargo run --bin ollama