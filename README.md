# unumbio-pdf-processing-test

Technical test: extract trademark records from a PDF bulletin JSON into a structured output JSON.

---

## Understanding the Input Data

### JSON coordinates — what they represent

PDFPlumber extracts every text block with its exact position on the page. Think of the PDF as a coordinate plane:

```
(0,0) ────────────────────────────► X (horizontal)
  │
  │      [text here x0=50, x1=200]
  │
  │      [another text x0=50, x1=200]
  │
  ▼
  Y (vertical, increases downward)
```

| Field    | Measures                  | Analogy                         |
|----------|---------------------------|---------------------------------|
| `x0`     | Left edge of text block   | Where the word starts           |
| `x1`     | Right edge of text block  | Where the word ends             |
| `top`    | Top edge                  | How far down from the top       |
| `bottom` | Bottom edge               | Lower boundary of the block     |

Example:

```json
{
    "text": "111",
    "x0": 50,
    "x1": 80,
    "top": 150,
    "bottom": 170
}
```

```
x=0                x=50   x=80
│                    │      │
│                  [111]        ← top=150, bottom=170
│
```

---

## Bulletin Structure (`BUL_EM_TM_2024000007`)

### Page map (166 pages total)

```
Page 2        → PART A / A.1.   (trademark records, type A)
Pages 87-88   → A.2.x           (A sub-sections)
Page 89       → PART B / B.1.   ← START of target section
Pages 90-122  → B.1. (interior)
Page 123      → B.2.            ← END of B.1.
Page 135      → B.3.
Page 136+     → B.4.
```

---

### Two-column layout (interior pages, e.g. page 90)

Each page is ~595 pts wide, split into two columns at approximately x ≈ 255:

```
┌──────────────────────────────────────────────────────────────┐
│   [HEADER: EUTM 018808640              Part B.1.]            │
│──────────────────────────────────────────────────────────────│
│  LEFT COLUMN            │    RIGHT COLUMN                    │
│  (x0 ≈ 56–80)           │    (x0 ≈ 311–334)                  │
│─────────────────────────│────────────────────────────────────│
│  400 | 03/10/2023...    │  111 | 018856421                   │
│                         │  151 | 10/01/2024                  │
│                         │  450 | 11/01/2024                  │
│  111 | 018808640        │  210 | 018856421                   │
│  151 | 10/01/2024       │  400 | 03/10/2023 - 2023/187 - A.1│
│  450 | 11/01/2024       │                                    │
│  210 | 018808640        │  111 | 018858443                   │
│  400 | 03/10/2023...    │  151 | 10/01/2024                  │
│                         │  ...                               │
│  111 | 018825895        │                                    │
│  ...                    │                                    │
└──────────────────────────────────────────────────────────────┘
```

INID codes (labels) and their values appear as adjacent text elements sorted by `top`. The label is always to the left of its value:

| Column | Label x0 | Value x0 |
|--------|----------|----------|
| Left   | ≈ 56.7   | ≈ 79.4   |
| Right  | ≈ 311.8  | ≈ 334.5  |

---

### Special case — page 89 (first page of B.1)

The section header occupies the left side, so the first records appear only in the right column:

```
┌──────────────────────────────────────────────────────────────┐
│         PART B        (section header, centered)             │
│         B.1.          (sub-section label)                    │
│                                                              │
│  [LEFT COLUMN empty]  │  450 | 11/01/2024                   │
│                       │  210 | 018752778                     │
│                       │  400 | 03/10/2023 - 2023/187 - A.1  │
│                       │                                      │
│                       │  111 | 018775536                     │
│                       │  ...                                 │
└──────────────────────────────────────────────────────────────┘
```

---

## INID Codes

Standard international codes for trademark bibliographic data:

| Code | Meaning |
|------|---------|
| `111` | Registration number |
| `151` | Registration date |
| `450` | Publication date in bulletin |
| `210` | Application number |
| `400` | Prior publication reference (date - bulletin - section) |

---

## A Complete Record

As it appears in the PDF (page 90, left column):

```
111 | 018808640
151 | 10/01/2024
450 | 11/01/2024
210 | 018808640
400 | 03/10/2023 - 2023/187 - A.1
```

As it must appear in the output JSON:

```json
{
  "B": {
    "1": [
      {
        "_PAGE": 90,
        "111": "018808640",
        "151": "10/01/2024",
        "450": "11/01/2024",
        "210": "018808640",
        "400": ["03/10/2023 - 2023/187 - A.1"]
      }
    ]
  }
}
```

Type rules:
- `_PAGE` → `int` (page where the record **starts**)
- `400` → `list[str]` (one entry per line)
- All other fields → `str`

---

## The 4 Challenges

| Challenge | What to detect |
|-----------|---------------|
| **Section filter** | B.1 starts when text `"B.1."` appears; ends when `"B.2."` appears |
| **Column reconstruction** | Split by x0 < ~255 (left) vs x0 > ~255 (right); process left column first, then right, per page |
| **Record identification** | Each record begins with INID code `111`; group all fields until the next `111` |
| **Page break handling** | A record may span two columns or two pages; the page header (e.g. `"EUTM 018808640"`) signals continuation |

---

## Script Flow

```
Read input JSON
    │
    ▼
Filter pages belonging to section B.1
    │
    ▼
For each page:
    ├─ Separate text elements by column (x0 < 255 → left, x0 ≥ 255 → right)
    ├─ Sort each column by top (ascending)
    └─ Process left column first, then right column
    │
    ▼
Identify records (each starts with code "111")
    │
    ▼
Group fields per record; handle cross-column and cross-page breaks
    │
    ▼
Write output JSON  →  BUL_EM_TM_2024000007_002.json
```

---

## Quick Reference — Why Coordinates Matter

| # | Purpose | Field used |
|---|---------|------------|
| 1 | Separate left / right columns | `x0` |
| 2 | Order text vertically within a column | `top` |
| 3 | Group elements belonging to the same record | `top` (proximity) |
