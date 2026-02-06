#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pyinstaller

pyinstaller --clean --onefile --name djvu2epub src/djvu2epub/cli.py

echo "Built dist/djvu2epub"
