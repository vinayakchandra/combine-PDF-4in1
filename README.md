# Combine PDF 4-in-1

Small Python tools and macOS Finder Quick Actions for combining PDF pages into a 2x2 layout.

## What It Does

- `combine_4in1_portrait.py` creates a portrait A4 output PDF.
- `combine_4in1_landscape.py` creates a landscape A4 output PDF, better for wide slides or landscape PDFs.
- Each output page contains up to 4 original PDF pages.
- Output files are created beside the input PDF.

## Requirements

- Python 3
- PyMuPDF

Install dependencies:

```bash
pip install -r requirements.txt
```

## Command Line Usage

Portrait A4:

```bash
python3 combine_4in1_portrait.py input.pdf
```

This creates:

```text
input_4in1.pdf
```

Landscape A4:

```bash
python3 combine_4in1_landscape.py input.pdf
```

This creates:

```text
input_4in1_landscape.pdf
```

## macOS Finder Quick Actions

This repo includes two Automator workflows:

- `pdf_4in1.workflow`
- `pdf_4in1_landscape.workflow`

To install a workflow into macOS:

1. Double-click the `.workflow` file.
2. macOS will ask to install it as a Quick Action.
3. Click `Install`.

After installing, use it from Finder:

1. Right-click a PDF file.
2. Open `Quick Actions`.
3. Select `pdf_4in1` or `pdf_4in1_landscape`.

The combined PDF will be created in the same folder as the original file.

## Notes

- Use the portrait workflow for normal portrait documents.
- Use the landscape workflow for wide PDFs, lecture slides, and landscape documents.
- The workflow files call the Python scripts from this project folder, so keep the project at:

```text
/Users/vinayak/IdeaProjects/python/combine-PDF-4in1
```
