$ErrorActionPreference = "Stop"

python -m venv .venv
. .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pyinstaller

pyinstaller --clean --onefile --name djvu2epub src\djvu2epub\cli.py

Write-Host "Built dist\\djvu2epub.exe"
