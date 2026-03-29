"""
loader.py
---------
Loads the input JSON file produced by PDFPlumber.

Each element in the list represents one page with the following keys:
  - page (int): page number
  - width, height (float): page dimensions in points
  - textboxhorizontal (list[dict]): text blocks with x0, x1, top, bottom, text
  - rects, line: geometric elements (not used here)
"""

from __future__ import annotations

import json
from pathlib import Path


def load_bulletin(path: str | Path) -> list[dict]:
    """Load and return the bulletin JSON as a list of page dicts.

    Args:
        path: Path to the *_001.json input file.

    Returns:
        List of page objects, each containing textboxhorizontal elements.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a valid JSON list.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list, got {type(data).__name__}")

    return data
