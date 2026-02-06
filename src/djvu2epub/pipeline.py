from __future__ import annotations

import json
import logging
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .config import Settings
from .epub import build_epub, create_default_metadata


logger = logging.getLogger(__name__)


def collect_inputs(input_path: Path, recursive: bool = True) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if not input_path.is_dir():
        raise FileNotFoundError(f"Input path not found: {input_path}")
    pattern = "**/*.djv*" if recursive else "*.djv*"
    return sorted(path for path in input_path.glob(pattern) if path.is_file())


def convert_file(input_path: Path, output_path: Path, settings: Settings) -> dict:
    logger.info("Converting %s -> %s", input_path.name, output_path)
    title = input_path.stem.replace("_", " ").strip() or "Untitled"
    metadata = create_default_metadata(title=title, language=settings.languages[0])
    body = (
        "This is a placeholder EPUB created by the DjVu-to-EPUB MVP. "
        "OCR and layout analysis are not yet implemented."
    )
    css = _default_css(settings)
    build_epub(output_path, metadata, body, css)
    return {
        "input": str(input_path),
        "output": str(output_path),
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def run_conversion(inputs: list[Path], output_path: Path, settings: Settings) -> dict:
    results = []
    for input_file in inputs:
        target = _resolve_output_path(output_path, input_file)
        results.append(convert_file(input_file, target, settings))
    report = {
        "summary": {
            "total": len(results),
            "success": len([item for item in results if item["status"] == "success"]),
        },
        "settings": asdict(settings),
        "files": results,
    }
    report_path = output_path if output_path.suffix == ".json" else output_path.with_suffix(".json")
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def _resolve_output_path(output_path: Path, input_file: Path) -> Path:
    if output_path.suffix == ".epub":
        return output_path
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / f"{input_file.stem}.epub"


def _default_css(settings: Settings) -> str:
    direction = "rtl" if settings.languages and settings.languages[0] in {"heb", "he"} else "ltr"
    text_align = "right" if direction == "rtl" else "left"
    return (
        "body { font-family: serif; line-height: 1.5; margin: 5%; direction: "
        + direction
        + "; text-align: "
        + text_align
        + "; }\n"
        "h1 { font-size: 1.6em; margin-bottom: 0.5em; }\n"
        "p { margin: 0 0 1em 0; }\n"
    )
