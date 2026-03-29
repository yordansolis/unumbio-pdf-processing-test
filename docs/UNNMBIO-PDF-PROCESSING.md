# PDF Processing – Technical Test

**UNUMBIO SpA | PROPRIETARY & CONFIDENTIAL | WHEN APPLICABLE: © ALL RIGHTS RESERVED**
*2026-03-26*

---

## 1. Test Inputs

For this challenge, you are provided with 5 files:

- **2 PDF files:** The original bulletins (for visual reference).

- **2 JSON files with suffix 001**: contain the elements of each PDF, extracted with PDFPlumber. It contains a list of objects, where each one represents a page. Each page in turn has sub-elements, the most relevant being:
  - `page`: Page number.
  - `textboxhorizontal`: text blocks.
  - `rects` and `line`: elements that can be used to detect separator lines.
  - In turn, the elements can contain parameters such as:
    - `text`: Textual content for the text blocks.
    - `x0`, `x1`: Horizontal position (left and right).
    - `top`, `bottom`: Vertical position (distance from the top edge).

- **1 JSON file with suffix 002:** A sample of the final schema that your script must generate.

---

## 2. Objective

Your mission is to write a Python script that processes the file **`BUL_EM_TM_2024000007_001.json`** to extract exclusively the records from **Section B.1.** and generate the file **`BUL_EM_TM_2024000007_002.json`**.

---

## 3. Challenges to Solve (Evaluation Criteria)

You must demonstrate how you solve the following geometric and logical problems through code:

- **Section Filter:** The source file contains the entire bulletin. Your script must identify where section **B.1** starts and ends based on the text content and its hierarchy.

- **Column Reconstruction:** The data in the PDF is arranged in two columns. You must use the `x0` and `x1` coordinates to correctly separate the information and prevent the text from the left column from mixing with the right one.

- **Record Identification:** Each trademark record typically starts with an INID code (e.g. code `111`). You must implement logic that groups all text elements belonging to the same record before moving on to the next one.

- **Multi-line and Page Break Handling:** Some records may be split across two columns or pages. The script must be able to group that information so that the output JSON does not have duplicate or incomplete records.

---

## 4. Delivery Requirements

- Clean Python code (following PEP 8).
- Use of standard or data processing libraries (e.g. `json`). It is not necessary to use PDF libraries since the input JSON already has the coordinates.
- A descriptive report explaining the main challenges encountered and the characteristics of the solutions proposed.
- The resulting **`BUL_EM_TM_2024000007_002.json`** file. It must comply with the same data structure shown in the document `BUL_EM_TM_2024000007_001.json`.

> If you are unable to complete the objective within the stipulated time, you may still submit the descriptive report, explaining the steps completed and those that were left to do. You may create pseudocode or a code template, specifying the functionalities that were left pending for development.

Files can be submitted as email attachments or as a link to a GitHub repository.

---

## 5. Notes on the Output JSON Structure

- **Output JSON structure:**
  - It must be an object with a key for each "section". In this case only section `"B"` is required.
  - Each section must be an object with a key for each "sub-section". In this case only sub-section `"1"` is required.
  - The sub-section must contain a list of objects, one for each record found.
  - The first parameter of the section must be `"_PAGE"`, and it indicates the first page where the first field of the record was seen. Most records have all their fields within the same page, but in some cases records may continue on the next page. In these cases `"_PAGE"` must be the page where the record started.
  - `"_PAGE"` must be of type `int`, and the field `"400"` must be stored as a list of `str`, with one element per line present. The remaining fields must be stored as `str`. If a text field has several text elements, they must be unified into a single element, joining the sub-parts with a space in between (`" "`).