import os
import sys
from pathlib import Path

import fitz  # PyMuPDF

# A4 landscape size in points (72 DPI): 842 x 595
A4_LANDSCAPE_WIDTH = 842
A4_LANDSCAPE_HEIGHT = 595


def combine_pdf_4_in_1_a4_landscape(input_pdf):
    doc = fitz.open(input_pdf)
    output = fitz.open()

    cell_width = A4_LANDSCAPE_WIDTH / 2
    cell_height = A4_LANDSCAPE_HEIGHT / 2

    for i in range(0, len(doc), 4):
        new_page = output.new_page(
            width=A4_LANDSCAPE_WIDTH,
            height=A4_LANDSCAPE_HEIGHT,
        )

        for j in range(4):
            if i + j >= len(doc):
                break

            src_page = doc[i + j]
            original_rect = src_page.rect

            # Fit each source page inside a wide landscape cell.
            scale_x = cell_width / original_rect.width
            scale_y = cell_height / original_rect.height
            scale = min(scale_x, scale_y)

            new_width = original_rect.width * scale
            new_height = original_rect.height * scale

            row = j // 2
            col = j % 2
            pos_x = col * cell_width + (cell_width - new_width) / 2
            pos_y = row * cell_height + (cell_height - new_height) / 2

            target_rect = fitz.Rect(pos_x, pos_y, pos_x + new_width, pos_y + new_height)

            new_page.show_pdf_page(
                target_rect,
                doc,
                i + j,
                keep_proportion=True,
            )

    input_path = Path(input_pdf)
    output_pdf = str(input_path.with_name(f"{input_path.stem}_4in1_landscape.pdf"))

    output.save(output_pdf)
    output.close()
    doc.close()

    print(f"Output saved to: {output_pdf}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python c4_landscape.py <input.pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]

    if not os.path.exists(input_pdf):
        print(f"File not found: {input_pdf}")
        sys.exit(1)

    combine_pdf_4_in_1_a4_landscape(input_pdf)


if __name__ == "__main__":
    main()
