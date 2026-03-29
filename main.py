"""
main.py
-------
Entry point for the PDF bulletin processing pipeline.

Configuration is read from a .env file in the project root.
Supported variables:
  INPUT_FILE   — path to the *_001.json bulletin (default: TECHNICAL-TEST/BUL_EM_TM_2024000007_001.json)
  OUTPUT_FILE  — path for the generated *_002.json   (default: output/BUL_EM_TM_2024000007_002.json)

Usage:
    python main.py
"""

import os
from pathlib import Path

from src.loader import load_bulletin
from src.section_filter import filter_section, SECTION_START, SECTION_END
from src.column_parser import split_columns
from src.record_builder import build_records
from src.exporter import export_json

# ---------------------------------------------------------------------------
# Load .env (stdlib only — no external dependencies)
# ---------------------------------------------------------------------------

def _load_env(env_path: Path = Path(".env")) -> None:
    """Parse a simple KEY=VALUE .env file and set missing env variables."""
    if not env_path.exists():
        return
    with env_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


_load_env()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_FILE = Path(os.environ.get("INPUT_FILE", "TECHNICAL-TEST/BUL_EM_TM_2024000007_001.json"))
OUTPUT_FILE = Path(os.environ.get("OUTPUT_FILE", "output/BUL_EM_TM_2024000007_002.json"))

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print()

    print("Loading bulletin...")
    pages = load_bulletin(INPUT_FILE)
    print(f"  Total pages: {len(pages)}")

    print(f"Filtering section {SECTION_START} → {SECTION_END}...")
    b1_pages = filter_section(pages, SECTION_START, SECTION_END)
    print(f"  Pages in section: {len(b1_pages)}")

    print("Extracting records...")
    records = build_records(b1_pages, split_columns)
    print(f"  Records found: {len(records)}")

    print("Exporting output JSON...")
    export_json(records, OUTPUT_FILE)
    print("Done.")


if __name__ == "__main__":
    main()
