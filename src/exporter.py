"""
exporter.py
-----------
Serialises the extracted records into the required output JSON structure
and writes it to disk.

Output schema:
  {
    "B": {
      "1": [
        {
          "_PAGE": <int>,
          "111": <str>,
          "151": <str>,
          "450": <str>,
          "210": <str>,
          "400": [<str>, ...]
        },
        ...
      ]
    }
  }
"""

import json
from pathlib import Path


def build_output(records: list[dict]) -> dict:
    """Wrap a flat list of records in the required B > 1 schema.

    Args:
        records: List of record dicts produced by record_builder.

    Returns:
        Dict matching the output JSON specification.
    """
    return {"B": {"1": records}}


def export_json(records: list[dict], output_path: str | Path) -> None:
    """Write records to the output JSON file.

    Args:
        records: List of record dicts produced by record_builder.
        output_path: Destination file path for the output JSON.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = build_output(records)

    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    print(f"Output written to: {output_path}  ({len(records)} records)")
