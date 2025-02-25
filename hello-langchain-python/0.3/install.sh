#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd -P)
cd "$SCRIPT_DIR" || exit

if [ "$(uname -s)" = "Linux" ] || [ "$(uname -s)" = "Darwin" ]; then
    python -m venv lc_env
    . "lc_env/bin/activate"
    which python
    pip install --upgrade pip
elif [ "$(uname -s)" = "CYGWIN" ] || [ "$(uname -s)" = "MSYS" ] || [ "$(uname -s)" = "MINGW" ] || [[ "$(uname -s)" == MINGW64_NT* ]]; then
    python -m venv lc_win_env
    . "lc_win_env/Scripts/activate"
    which python
    python.exe -m pip install --upgrade pip
else
    echo "Unsupported OS"
    exit 1
fi
# 安装依赖
pip install -r requirements.txt
