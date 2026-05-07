import fitz  # PyMuPDF
import sys
import os

# A4 size in points (72 DPI): 595 x 842
A4_WIDTH = 595
A4_HEIGHT = 842

def combine_pdf_4_in_1_a4(input_pdf):
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

    output_pdf=f"{input_pdf[:-4]}_4in1.pdf"
    print(output_pdf)

    output.save(output_pdf)
    print(f"✅ Output saved to: {output_pdf}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python c4.py <input.pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    # output_pdf = sys.argv[2] if len(sys.argv) > 2 else "output_4in1_A4.pdf"

    if not os.path.exists(input_pdf):
        print(f"❌ File not found: {input_pdf}")
        sys.exit(1)

    combine_pdf_4_in_1_a4(input_pdf)


if __name__ == "__main__":
    main()
