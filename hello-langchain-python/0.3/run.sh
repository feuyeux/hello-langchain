#!/bin/bash
cd "$(
    cd "$(dirname "$0")" >/dev/null 2>&1
    pwd -P
)/" || exit
set -e

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

python hello.py
