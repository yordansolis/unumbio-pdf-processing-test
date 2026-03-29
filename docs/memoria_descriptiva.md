# Descriptive Report — PDF Bulletin Processing

**UNUMBIO SpA | Technical Test**
*2026-03-29*

---

## 1. Overview

This report describes the main challenges encountered when extracting trademark records from section B.1 of the bulletin `BUL_EM_TM_2024000007`, and the solutions implemented in the Python script.

---

## 2. Challenges and Solutions

### 2.1 Section Filter

**Challenge:** The input JSON contains the full bulletin (166 pages, multiple sections). Only section B.1 must be processed.

**Solution:** Scan each page's `textboxhorizontal` elements for the string `"B.1."` to mark the start, and `"B.2."` to mark the end. Only the slice of pages between those markers is passed to downstream modules (`section_filter.py`).

---

### 2.2 Column Reconstruction

**Challenge:** PDFPlumber extracts all text elements from a page in a flat list. The PDF has two columns and their elements are interleaved in the list, so a naive top-to-bottom sort would mix records from both columns.

**Solution:** Use the `x0` coordinate as a column discriminator. Analysis of the actual data shows:

| Column | Label x0 | Value x0 |
|--------|----------|----------|
| Left   | ≈ 56.7   | ≈ 79.4   |
| Right  | ≈ 311.8  | ≈ 334.5  |

A threshold of `x0 < 255` separates left from right. Each column is then sorted independently by `top` (ascending). The left column is always processed before the right to maintain reading order (`column_parser.py`).

---

### 2.3 Record Identification

**Challenge:** There is no explicit record delimiter in the JSON. Records must be inferred from the presence of INID code `111` (registration number), which marks the start of each new record.

**Solution:** Within each column, label elements (those whose text matches a known INID code) are paired with their value elements using `top` proximity (within 4 pt tolerance). The resulting `(code, value)` pairs are then walked sequentially: each `111` opens a new record, and all subsequent codes are accumulated into it until the next `111` appears (`record_builder.py`).

---

### 2.4 Multi-line and Page Break Handling

**Challenge:** A record may start at the bottom of a column and continue at the top of the next column, or even on the following page. Splitting processing at column/page boundaries would produce incomplete records.

**Solution:** A `pending` record variable is maintained across column and page boundaries. The last record of each column is held as `pending` and only committed once the next column starts (confirming it is complete). This ensures records that span two columns or two pages are assembled correctly.

---

## 3. Output Structure

```json
{
  "B": {
    "1": [
      {
        "_PAGE": <int>,
        "111": <str>,
        "151": <str>,
        "450": <str>,
        "210": <str>,
        "400": [<str>]
      }
    ]
  }
}
```

- `_PAGE`: page number where the first field of the record was observed.
- `400`: stored as `list[str]` (one element per source line).
- All other fields: stored as `str`. Multiple sub-elements joined with `" "`.

---

## 4. Module Summary

| Module | Responsibility |
|--------|---------------|
| `loader.py` | Load and validate the input JSON |
| `section_filter.py` | Identify and return only B.1 pages |
| `column_parser.py` | Split and sort elements by column |
| `record_builder.py` | Pair labels/values and group into records |
| `exporter.py` | Wrap records in the output schema and write JSON |
| `main.py` | Orchestrate the full pipeline |
