#!/bin/bash
cd "$(
  cd "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)/" || exit
set -e

git pull
git submodule update --remote
git add -A && git commit -m "up" && git push
