"""
main.py
-------
Entry point for the PDF bulletin processing pipeline.

Usage:
    python main.py

Reads:  TECHNICAL-TEST/BUL_EM_TM_2024000007_001.json
Writes: output/BUL_EM_TM_2024000007_002.json
"""

from pathlib import Path

from src.loader import load_bulletin
from src.section_filter import filter_section_b1
from src.column_parser import split_columns
from src.record_builder import build_records
from src.exporter import export_json

INPUT_FILE = Path("TECHNICAL-TEST/BUL_EM_TM_2024000007_001.json")
OUTPUT_FILE = Path("output/BUL_EM_TM_2024000007_002.json")


def main() -> None:
    print("Loading bulletin...")
    pages = load_bulletin(INPUT_FILE)
    print(f"  Total pages: {len(pages)}")

    print("Filtering section B.1...")
    b1_pages = filter_section_b1(pages)
    print(f"  Pages in B.1: {len(b1_pages)}")

    print("Extracting records...")
    records = build_records(b1_pages, split_columns)
    print(f"  Records found: {len(records)}")

    print("Exporting output JSON...")
    export_json(records, OUTPUT_FILE)
    print("Done.")


if __name__ == "__main__":
    main()
