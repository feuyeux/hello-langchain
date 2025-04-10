#!/bin/bash
cd "$(
    cd "$(dirname "$0")" >/dev/null 2>&1
    pwd -P
)/" || exit
set -e
source .env.sh # 使用 source 命令加载环境变量，确保它们在当前 shell 中生效
dart pub get
dart ollama.dart
