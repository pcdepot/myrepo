# djvu2epub (MVP)

This repository contains an MVP CLI application for converting DjVu files into placeholder EPUB outputs.
The current implementation focuses on application structure, CLI options, and EPUB packaging. OCR and
layout analysis are stubbed for future development.

## Features

- CLI with flags aligned to the DjVu-to-EPUB PRD
- Batch conversion for directories
- Minimal EPUB 3 packaging with navigation and CSS
- JSON conversion report generation

## Quick Start

```bash
pip install -e .

djvu2epub input.djvu -o output.epub
```

### Batch Conversion

```bash
# Convert all DjVu files in a directory

djvu2epub ./input_dir -o ./output_dir
```

### Configuration

Only JSON configuration files are supported in this MVP.

```bash
cat > config.json <<'JSON'
{
  "languages": ["eng", "rus"],
  "quality": "high",
  "layout_mode": "reflowable"
}
JSON

djvu2epub input.djvu -o output.epub --config config.json
```

## Notes

- The EPUB content currently contains placeholder text and styling.
- OCR, layout analysis, and validation features will be implemented in future iterations.

## Executable Builds (macOS & Windows)

Use the helper scripts to produce standalone executables with PyInstaller.

### macOS

```bash
./scripts/build-macos.sh
```

### Windows (PowerShell)

```powershell
.\scripts\build-windows.ps1
```

Artifacts are written to the `dist/` directory.
