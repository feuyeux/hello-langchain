#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd -P)
cd "$SCRIPT_DIR" || exit

# Only support Unix-like systems (Linux/macOS)
if [ "$(uname -s)" = "Linux" ] || [ "$(uname -s)" = "Darwin" ]; then
    if [ ! -d "lc_env" ]; then
        echo "Setting up virtual environment..."
        python -m venv lc_env
    else
        echo "Virtual environment already exists, skipping creation..."
    fi

    . "lc_env/bin/activate"
    which python
    echo "Upgrading pip..."
    pip install --upgrade pip
else
    echo "Unsupported OS. Use install.bat for Windows."
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt
echo "Setup complete!"
