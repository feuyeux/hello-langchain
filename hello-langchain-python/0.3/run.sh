#!/bin/bash
cd "$(
    cd "$(dirname "$0")" >/dev/null 2>&1
    pwd -P
)/" || exit
set -e

# Force Windows path for WSL or Git Bash on Windows
if [[ -d "lc_win_env/Scripts" ]]; then
    echo "Using Windows virtual environment"
    . "lc_win_env/Scripts/activate"
elif [ "$(uname -s)" = "Linux" ] || [ "$(uname -s)" = "Darwin" ]; then
    # 对于 Linux 和 macOS
    . "lc_env/bin/activate"
elif [ "$(uname -s)" = "CYGWIN" ] || [ "$(uname -s)" = "MSYS" ] || [ "$(uname -s)" = "MINGW" ] || [[ "$(uname -s)" == MINGW64_NT* ]]; then
    # 对于 Cygwin 和 MSYS2
    . "lc_win_env/Scripts/activate"
else
    echo "Unsupported OS"
    exit 1
fi

# python hello.py

# python ollama-translate.py

python prompt_engineering.py
