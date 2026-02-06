from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class Settings:
    languages: list[str] = field(default_factory=lambda: ["eng"])
    layout_mode: str = "reflowable"
    quality: str = "standard"
    include_page_scans: bool = False
    keep_page_markers: bool = False
    spellcheck: bool = False
    parallel: int = 0
    log_level: str = "info"
    metadata_file: str | None = None
    config_file: str | None = None
    output: str | None = None
    preserve_layout: bool = False
    keep_temp: bool = False
    ignore_validation_errors: bool = False
    throttle: int | None = None
    max_memory: int | None = None


def load_config(path: str | None) -> dict:
    if not path:
        return {}
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    if config_path.suffix.lower() in {".json"}:
        return json.loads(config_path.read_text(encoding="utf-8"))
    raise ValueError("Only JSON configuration files are supported in this MVP.")


def apply_overrides(settings: Settings, overrides: dict) -> Settings:
    for key, value in overrides.items():
        if not hasattr(settings, key):
            continue
        setattr(settings, key, value)
    return settings


def parse_languages(value: str | Iterable[str]) -> list[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [item.strip() for item in value if item.strip()]
