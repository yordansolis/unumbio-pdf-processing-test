"""
record_builder.py
-----------------
Groups individual text elements into structured trademark records.

All configurable values are read from environment variables so the script
can be adapted to different bulletin types without changing source code:

  INID_CODES        — comma-separated set of valid field codes  (default: 111,151,450,210,400)
  RECORD_START_CODE — code that opens a new record              (default: 111)
  LIST_FIELDS       — comma-separated codes stored as list[str] (default: 400)
  TOP_TOLERANCE     — max vertical distance (pts) to pair a
                      label with its value element              (default: 4.0)

A new record starts whenever RECORD_START_CODE is encountered.
Fields listed in LIST_FIELDS accumulate one entry per source line.
All other fields are stored as str; multiple sub-elements are joined
with a single space.
"""

from __future__ import annotations

import os


def _csv_set(env_key: str, default: str) -> set[str]:
    return {v.strip() for v in os.environ.get(env_key, default).split(",") if v.strip()}


INID_CODES: set[str] = _csv_set("INID_CODES", "111,151,450,210,400")
RECORD_START_CODE: str = os.environ.get("RECORD_START_CODE", "111")
LIST_FIELDS: set[str] = _csv_set("LIST_FIELDS", "400")
TOP_TOLERANCE: float = float(os.environ.get("TOP_TOLERANCE", "4.0"))


def _pair_labels_and_values(elements: list[dict]) -> list[tuple[str, str]]:
    """Pair INID label elements with their value elements by top position.

    Returns a list of (inid_code, value_text) tuples in vertical order.
    Unpaired elements (e.g. section headers that slipped through) are
    discarded.
    """
    paired: list[tuple[str, str]] = []
    used: set[int] = set()

    for i, elem in enumerate(elements):
        if i in used:
            continue
        text = elem["text"].strip()
        if text not in INID_CODES:
            continue
        for j, candidate in enumerate(elements):
            if j in used or j == i:
                continue
            if candidate["text"].strip() in INID_CODES:
                continue
            if abs(candidate["top"] - elem["top"]) <= TOP_TOLERANCE:
                paired.append((text, candidate["text"].strip()))
                used.add(i)
                used.add(j)
                break

    return paired


def _build_records_from_pairs(
    pairs: list[tuple[str, str]],
    page_number: int,
) -> list[dict]:
    """Convert a flat list of (code, value) pairs into record dicts.

    A new record is opened each time RECORD_START_CODE is encountered.
    """
    records: list[dict] = []
    current: dict | None = None

    for code, value in pairs:
        if code == RECORD_START_CODE:
            if current is not None:
                records.append(current)
            current = {"_PAGE": page_number, RECORD_START_CODE: value}
        elif current is not None:
            if code in LIST_FIELDS:
                current.setdefault(code, []).append(value)
            elif code in current:
                current[code] = current[code] + " " + value
            else:
                current[code] = value

    if current is not None:
        records.append(current)

    return records


def build_records(pages: list[dict], split_columns_fn) -> list[dict]:
    """Extract all records from the section pages.

    Processes each page's left column first, then right column.
    A record that starts near the bottom of a column/page may continue
    at the top of the next; this is handled by carrying a pending record
    across column and page boundaries.

    Args:
        pages: List of section page dicts.
        split_columns_fn: Callable(page) → (left_elements, right_elements).

    Returns:
        List of complete record dicts.
    """
    all_records: list[dict] = []
    pending: dict | None = None

    for page in pages:
        left, right = split_columns_fn(page)
        page_number: int = page["page"]

        for column in (left, right):
            pairs = _pair_labels_and_values(column)
            records = _build_records_from_pairs(pairs, page_number)

            if not records:
                continue

            if pending is not None:
                all_records.append(pending)
                pending = None

            all_records.extend(records[:-1])
            pending = records[-1]

    if pending is not None:
        all_records.append(pending)

    return all_records
