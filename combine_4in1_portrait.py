import fitz  # PyMuPDF
import sys
import os
from pathlib import Path

from office_pdf_converter import ConversionError, input_as_pdf

# A4 size in points (72 DPI): 595 x 842
A4_WIDTH = 595
A4_HEIGHT = 842

def combine_pdf_4_in_1_a4(input_file):
    input_path = Path(input_file).expanduser().resolve()

    with input_as_pdf(input_path) as input_pdf:
        doc = fitz.open(input_pdf)
        output = fitz.open()

        cell_width = A4_WIDTH / 2
        cell_height = A4_HEIGHT / 2

        for i in range(0, len(doc), 4):
            new_page = output.new_page(width=A4_WIDTH, height=A4_HEIGHT)

            for j in range(4):
                if i + j >= len(doc):
                    break

                src_page = doc[i + j]
                original_rect = src_page.rect

                # Compute scale to fit in cell while preserving aspect ratio
                scale_x = cell_width / original_rect.width
                scale_y = cell_height / original_rect.height
                scale = min(scale_x, scale_y)

                # Calculate new size
                new_width = original_rect.width * scale
                new_height = original_rect.height * scale

                # Position in 2x2 grid
                row = j // 2
                col = j % 2
                pos_x = col * cell_width + (cell_width - new_width) / 2
                pos_y = row * cell_height + (cell_height - new_height) / 2

                # Target rectangle
                target_rect = fitz.Rect(pos_x, pos_y, pos_x + new_width, pos_y + new_height)

                new_page.show_pdf_page(
                    target_rect,
                    doc,
                    i + j,
                    keep_proportion=True
                )

        output_pdf = str(input_path.with_name(f"{input_path.stem}_4in1.pdf"))
        output.save(output_pdf)
        output.close()
        doc.close()

        print(f"Output saved to: {output_pdf}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python combine_4in1_portrait.py <input.pdf|docx|doc|pptx|ppt>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    # output_pdf = sys.argv[2] if len(sys.argv) > 2 else "output_4in1_A4.pdf"

    if not os.path.exists(input_pdf):
        print(f"❌ File not found: {input_pdf}")
        sys.exit(1)

    try:
        combine_pdf_4_in_1_a4(input_pdf)
    except ConversionError as exc:
        print(f"Conversion failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
