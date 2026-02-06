from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .config import Settings, apply_overrides, load_config, parse_languages
from .pipeline import collect_inputs, run_conversion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DjVu-to-EPUB Intelligent Converter (MVP)")
    parser.add_argument("input", help="Input DjVu file or directory")
    parser.add_argument("-o", "--output", required=True, help="Output EPUB file or directory")
    parser.add_argument("-l", "--languages", default="eng", help="OCR languages (comma-separated)")
    parser.add_argument("--layout-mode", default="reflowable", choices=["reflowable", "faithful"])
    parser.add_argument("--quality", default="standard", choices=["fast", "standard", "high"])
    parser.add_argument("--include-page-scans", action="store_true")
    parser.add_argument("--keep-page-markers", action="store_true")
    parser.add_argument("--spellcheck", action="store_true")
    parser.add_argument("--parallel", type=int, default=0)
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warn", "error"])
    parser.add_argument("--metadata-file")
    parser.add_argument("--config")
    parser.add_argument("--preserve-layout", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--ignore-validation-errors", action="store_true")
    parser.add_argument("--throttle", type=int)
    parser.add_argument("--max-memory", type=int)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    settings = Settings()
    settings.languages = parse_languages(args.languages)
    settings.layout_mode = args.layout_mode
    settings.quality = args.quality
    settings.include_page_scans = args.include_page_scans
    settings.keep_page_markers = args.keep_page_markers
    settings.spellcheck = args.spellcheck
    settings.parallel = args.parallel
    settings.log_level = args.log_level
    settings.metadata_file = args.metadata_file
    settings.config_file = args.config
    settings.preserve_layout = args.preserve_layout
    settings.keep_temp = args.keep_temp
    settings.ignore_validation_errors = args.ignore_validation_errors
    settings.throttle = args.throttle
    settings.max_memory = args.max_memory

    config_data = load_config(args.config)
    settings = apply_overrides(settings, config_data)

    logging.basicConfig(
        level=_parse_log_level(settings.log_level),
        format="%(asctime)s %(levelname)s %(message)s",
    )

    input_path = Path(args.input)
    output_path = Path(args.output)

    inputs = collect_inputs(input_path)
    if not inputs:
        raise SystemExit("No DjVu files found at input path.")

    run_conversion(inputs, output_path, settings)
    logging.info("Conversion complete. Report saved alongside output.")
    return 0


def _parse_log_level(level: str) -> int:
    mapping = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARNING,
        "error": logging.ERROR,
    }
    return mapping.get(level, logging.INFO)


if __name__ == "__main__":
    raise SystemExit(main())
