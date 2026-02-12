#!/bin/bash
# Linux installation script for LangChain project

if [ ! -d "lc_linux_env" ]; then
    echo "Setting up virtual environment for Linux..."
    python3 -m venv lc_linux_env
else
    echo "Virtual environment already exists, skipping creation..."
fi

source lc_linux_env/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
