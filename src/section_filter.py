"""
section_filter.py
-----------------
Detects where a target section starts and ends in the bulletin pages.

Section markers are read from environment variables so the script can be
pointed at any section without changing source code:

  SECTION_START  — text that marks the first page of the target section (default: B.1.)
  SECTION_END    — text that marks the first page of the next section   (default: B.2.)

The function returns only the pages that belong to the target section, so
downstream modules do not need to be aware of the rest of the bulletin.
"""

import os

SECTION_START: str = os.environ.get("SECTION_START", "B.1.")
SECTION_END: str = os.environ.get("SECTION_END", "B.2.")


def _page_texts(page: dict) -> list[str]:
    """Return all stripped text values from a page's textboxhorizontal."""
    return [
        tb["text"].strip()
        for tb in page.get("textboxhorizontal", [])
    ]


def filter_section(
    pages: list[dict],
    start_marker: str = SECTION_START,
    end_marker: str = SECTION_END,
) -> list[dict]:
    """Return the subset of pages belonging to the target section.

    Args:
        pages: Full list of page dicts from the bulletin JSON.
        start_marker: Text that identifies the first page of the section.
        end_marker: Text that identifies the start of the following section.

    Returns:
        List of page dicts from the first matching start page up to
        (not including) the first matching end page.

    Raises:
        ValueError: If start_marker is not found in any page.
    """
    start_index: int | None = None
    end_index: int | None = None

    for i, page in enumerate(pages):
        texts = _page_texts(page)
        if start_index is None and start_marker in texts:
            start_index = i
        elif start_index is not None and end_marker in texts:
            end_index = i
            break

    if start_index is None:
        raise ValueError(
            f"Section start marker '{start_marker}' not found in bulletin."
        )

    return pages[start_index:end_index]
