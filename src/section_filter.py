"""
section_filter.py
-----------------
Detects where section B.1 starts and ends in the bulletin pages.

Strategy:
  - Section B.1 begins on the page that contains the text "B.1."
  - Section B.1 ends just before the page that contains "B.2."

The function returns only the pages that belong to B.1, so downstream
modules do not need to be aware of the rest of the bulletin.
"""

SECTION_START = "B.1."
SECTION_END = "B.2."


def _page_texts(page: dict) -> list[str]:
    """Return all stripped text values from a page's textboxhorizontal."""
    return [
        tb["text"].strip()
        for tb in page.get("textboxhorizontal", [])
    ]


def filter_section_b1(pages: list[dict]) -> list[dict]:
    """Return the subset of pages that belong to section B.1.

    Args:
        pages: Full list of page dicts from the bulletin JSON.

    Returns:
        List of page dicts from the first B.1 page up to (not including)
        the first B.2 page.

    Raises:
        ValueError: If the B.1 section start marker is not found.
    """
    start_index: int | None = None
    end_index: int | None = None

    for i, page in enumerate(pages):
        texts = _page_texts(page)
        if start_index is None and SECTION_START in texts:
            start_index = i
        elif start_index is not None and SECTION_END in texts:
            end_index = i
            break

    if start_index is None:
        raise ValueError(f"Section start marker '{SECTION_START}' not found in bulletin.")

    return pages[start_index:end_index]
