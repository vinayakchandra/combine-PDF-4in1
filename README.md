# Combine PDF 4-in-1

Small Python tools and macOS Finder Quick Actions for combining PDF, Word, and PowerPoint files into a 2x2 layout.

## What It Does

- `combine_4in1_portrait.py` creates a portrait A4 output PDF.
- `combine_4in1_landscape.py` creates a landscape A4 output PDF, better for wide slides or landscape PDFs.
- Supported inputs: `.pdf`, `.doc`, `.docx`, `.ppt`, and `.pptx`.
- Word and PowerPoint files are converted to a temporary PDF first, then combined.
- Each output page contains up to 4 original pages or slides.
- Output files are created beside the input file.

## Requirements

- Python 3
- PyMuPDF
- Microsoft PowerPoint for PowerPoint conversion
- Microsoft Word or Pages for Word conversion

Install dependencies:

```bash
pip install -r requirements.txt
```

## Command Line Usage

Portrait A4:

```bash
python3 combine_4in1_portrait.py input.pdf
python3 combine_4in1_portrait.py input.docx
python3 combine_4in1_portrait.py input.pptx
```

This creates:

```text
input_4in1.pdf
```

Landscape A4:

```bash
python3 combine_4in1_landscape.py input.pdf
python3 combine_4in1_landscape.py input.docx
python3 combine_4in1_landscape.py input.pptx
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

1. Right-click a PDF, Word, or PowerPoint file.
2. Open `Quick Actions`.
3. Select `pdf_4in1` or `pdf_4in1_landscape`.

The combined PDF will be created in the same folder as the original file.

## Notes

- Use the portrait workflow for normal portrait documents.
- Use the landscape workflow for wide PDFs, lecture slides, and landscape documents.
- macOS may ask for permission the first time Automator controls Microsoft Office or Pages.
- The workflow files call the Python scripts from this project folder, so keep the project at:

```text
/Users/vinayak/IdeaProjects/python/combine-PDF-4in1
```
