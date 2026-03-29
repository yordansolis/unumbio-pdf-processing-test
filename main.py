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
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root — resolve paths relative to this file, not the working dir.
# Must be set before importing src.* so the package is always findable.
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Load .env (stdlib only — no external dependencies)
# ---------------------------------------------------------------------------


def _load_env(env_path: Path = PROJECT_ROOT / ".env") -> None:
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
# src imports — must come after _load_env() so env vars are set before
# module-level constants in each module are evaluated.
# ---------------------------------------------------------------------------

from src.loader import load_bulletin  # noqa: E402
from src.section_filter import filter_section, SECTION_START, SECTION_END  # noqa: E402
from src.column_parser import split_columns  # noqa: E402
from src.record_builder import build_records  # noqa: E402
from src.exporter import export_json  # noqa: E402

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_FILE = PROJECT_ROOT / os.environ.get(
    "INPUT_FILE", "TECHNICAL-TEST/BUL_EM_TM_2024000007_001.json"
)
OUTPUT_FILE = PROJECT_ROOT / os.environ.get(
    "OUTPUT_FILE", "output/BUL_EM_TM_2024000007_002.json"
)

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


def main() -> None:
    print(f"📄 Input:  {INPUT_FILE}")
    print(f"📁 Output: {OUTPUT_FILE}")
    print()

    try:
        print("⏳ Loading bulletin...")
        pages = load_bulletin(INPUT_FILE)
        print(f"   ✅ {len(pages)} pages loaded")

        print(f"⏳ Filtering section {SECTION_START} → {SECTION_END}...")
        b1_pages = filter_section(pages, SECTION_START, SECTION_END)
        print(f"   ✅ {len(b1_pages)} pages in section")

        print("⏳ Extracting records...")
        records = build_records(b1_pages, split_columns)
        print(f"   ✅ {len(records)} records found")

        print("⏳ Exporting output JSON...")
        export_json(records, OUTPUT_FILE)

        print()
        print("🎉 All done!")

    except FileNotFoundError as exc:
        print(f"\n❌ File not found: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"\n❌ Processing error: {exc}", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"\n❌ I/O error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
