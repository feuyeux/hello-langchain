#!/bin/bash
cd "$(
    cd "$(dirname "$0")" >/dev/null 2>&1
    pwd -P
)/" || exit
set -e
#cat "$HOME"/.gitconfig
#cargo clean
cargo fmt
cargo build
cargo run --bin ollama
