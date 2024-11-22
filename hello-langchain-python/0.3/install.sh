#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd -P)
cd "$SCRIPT_DIR" || exit

python -m venv lc_env

if [ "$(uname -s)" = "Linux" ] || [ "$(uname -s)" = "Darwin" ]; then
    # 对于 Linux 和 macOS
    . "lc_env/bin/activate"
elif [ "$(uname -s)" = "CYGWIN" ] || [ "$(uname -s)" = "MSYS" ] || [ "$(uname -s)" = "MINGW" ]; then
    # 对于 Cygwin 和 MSYS2
    . "lc_env/Scripts/activate"
else
    echo "Unsupported OS"
    exit 1
fi

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
