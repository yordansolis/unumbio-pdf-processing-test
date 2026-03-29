"""
column_parser.py
----------------
Splits a page's text elements into left and right columns based on x0,
then sorts each column top-to-bottom.

Column boundaries (measured in points on a ~595 pt wide page):
  Left column:   INID label x0 ≈ 56.7,  value x0 ≈ 79.4
  Right column:  INID label x0 ≈ 311.8, value x0 ≈ 334.5
  Dividing line: x0 < COLUMN_SPLIT → left, x0 >= COLUMN_SPLIT → right

The page header elements (e.g. "EUTM XXXXXXXXX", "Part B.1.") are
filtered out before returning the columns.
"""

COLUMN_SPLIT = 255.0  # horizontal dividing line in points

# Text patterns that identify page header/footer elements to skip
_HEADER_PREFIXES = ("EUTM ", "Part B", "PART B", "Part A", "PART A")


def _is_header(text: str) -> bool:
    """Return True if the text element is a page header/footer to skip."""
    t = text.strip()
    return any(t.startswith(prefix) for prefix in _HEADER_PREFIXES)


def _sorted_by_top(elements: list[dict]) -> list[dict]:
    return sorted(elements, key=lambda e: e["top"])


def split_columns(page: dict) -> tuple[list[dict], list[dict]]:
    """Split text elements of a page into (left_column, right_column).

    Both lists are sorted vertically (ascending top).
    Header/footer elements are excluded.

    Args:
        page: A single page dict from the bulletin JSON.

    Returns:
        Tuple of (left_elements, right_elements), each sorted by top.
    """
    left: list[dict] = []
    right: list[dict] = []

    for tb in page.get("textboxhorizontal", []):
        text = tb.get("text", "").strip()
        if not text or _is_header(text):
            continue
        if tb["x0"] < COLUMN_SPLIT:
            left.append(tb)
        else:
            right.append(tb)

    return _sorted_by_top(left), _sorted_by_top(right)
