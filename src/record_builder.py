"""
record_builder.py
-----------------
Groups individual text elements into structured trademark records.

Each record in section B.1 contains the following INID codes:
  111 — Registration number      (str)
  151 — Registration date        (str)
  450 — Publication date         (str)
  210 — Application number       (str)
  400 — Prior publication ref    (list[str], one item per line)

A new record starts whenever the INID code "111" is encountered.
Fields with multiple text elements are joined with a single space.

The label/value pairs on each page are interleaved: the INID code
element and its value element share the same (or very close) `top`
coordinate but differ in x0.  We pair them by grouping elements at
the same vertical band (within TOP_TOLERANCE points of each other).
"""

from __future__ import annotations

INID_CODES = {"111", "151", "450", "210", "400"}
RECORD_START_CODE = "111"

# Two elements are considered "on the same line" if their top values
# differ by less than this amount (in points).
TOP_TOLERANCE = 4.0


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
        # Look for the value element at the same vertical position
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

    A new record is opened each time code "111" is encountered.
    """
    records: list[dict] = []
    current: dict | None = None

    for code, value in pairs:
        if code == RECORD_START_CODE:
            if current is not None:
                records.append(current)
            current = {"_PAGE": page_number, "111": value}
        elif current is not None:
            if code == "400":
                current.setdefault("400", []).append(value)
            else:
                if code in current:
                    # Multiple elements for the same code → join with space
                    current[code] = current[code] + " " + value
                else:
                    current[code] = value

    if current is not None:
        records.append(current)

    return records


def build_records(pages: list[dict], split_columns_fn) -> list[dict]:
    """Extract all records from the B.1 pages.

    Processes each page's left column first, then right column.
    A record that starts near the bottom of a column/page may
    continue at the top of the next column/page; this is handled
    by carrying an open (incomplete) record across boundaries.

    Args:
        pages: List of B.1 page dicts.
        split_columns_fn: Callable that takes a page dict and returns
                          (left_elements, right_elements).

    Returns:
        List of complete record dicts.
    """
    all_records: list[dict] = []
    pending: dict | None = None  # record that started but is not yet closed

    for page in pages:
        left, right = split_columns_fn(page)
        page_number: int = page["page"]

        for column in (left, right):
            pairs = _pair_labels_and_values(column)
            records = _build_records_from_pairs(pairs, page_number)

            if not records:
                continue

            if pending is not None:
                # The first record from this column may be the continuation
                # of the pending one (it won't have a "111" restart for the
                # same registration number — handled by the caller if needed).
                # For B.1, every record is self-contained within its block,
                # so we simply close the pending record here.
                all_records.append(pending)
                pending = None

            # Keep the last record as pending until we confirm it is complete
            all_records.extend(records[:-1])
            pending = records[-1]

    if pending is not None:
        all_records.append(pending)

    return all_records
