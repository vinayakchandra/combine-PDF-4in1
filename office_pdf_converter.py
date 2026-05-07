import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path


PDF_EXTENSIONS = {".pdf"}
WORD_EXTENSIONS = {".doc", ".docx"}
POWERPOINT_EXTENSIONS = {".ppt", ".pptx"}
SUPPORTED_EXTENSIONS = PDF_EXTENSIONS | WORD_EXTENSIONS | POWERPOINT_EXTENSIONS


class ConversionError(RuntimeError):
    pass


@contextmanager
def input_as_pdf(input_file):
    input_path = Path(input_file).expanduser().resolve()
    suffix = input_path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ConversionError(f"Unsupported file type '{suffix}'. Supported: {supported}")

    if suffix in PDF_EXTENSIONS:
        yield input_path
        return

    with tempfile.TemporaryDirectory(prefix="4in1-convert-") as temp_dir:
        output_pdf = Path(temp_dir) / f"{input_path.stem}.pdf"
        convert_to_pdf(input_path, output_pdf)
        yield output_pdf


def convert_to_pdf(input_path, output_pdf):
    errors = []

    for converter in _converters_for(input_path.suffix.lower()):
        try:
            converter(input_path, output_pdf)
            if output_pdf.exists() and output_pdf.stat().st_size > 0:
                return
            errors.append(f"{converter.__name__}: no PDF was created")
        except Exception as exc:
            errors.append(f"{converter.__name__}: {exc}")

    details = "\n".join(f"  - {error}" for error in errors)
    raise ConversionError(
        "Could not convert the input file to PDF.\n"
        "Make sure Microsoft Office / Pages are installed and allowed to be "
        "automated by Terminal/Automator.\n"
        f"{details}"
    )


def _converters_for(suffix):
    if suffix in WORD_EXTENSIONS:
        return [_convert_with_microsoft_word, _convert_with_pages]
    if suffix in POWERPOINT_EXTENSIONS:
        return [_convert_with_microsoft_powerpoint]

    return []


def _convert_with_microsoft_word(input_path, output_pdf):
    if not _app_exists("Microsoft Word"):
        raise ConversionError("Microsoft Word was not found")

    _run_osascript(
        """
        on run argv
            set inputPath to POSIX file (item 1 of argv)
            set outputPath to item 2 of argv
            tell application "Microsoft Word"
                open inputPath
                set theDoc to active document
                save as theDoc file name outputPath file format format PDF
                close theDoc saving no
            end tell
        end run
        """,
        input_path,
        output_pdf,
    )


def _convert_with_microsoft_powerpoint(input_path, output_pdf):
    if not _app_exists("Microsoft PowerPoint"):
        raise ConversionError("Microsoft PowerPoint was not found")

    _run_osascript(
        """
        on run argv
            set inputPath to POSIX file (item 1 of argv)
            set outputPath to POSIX file (item 2 of argv)
            tell application "Microsoft PowerPoint"
                open inputPath
                set thePresentation to active presentation
                save thePresentation in outputPath as save as PDF
                close thePresentation
            end tell
        end run
        """,
        input_path,
        output_pdf,
    )


def _convert_with_pages(input_path, output_pdf):
    if not _app_exists("Pages"):
        raise ConversionError("Pages was not found")

    _run_osascript(
        """
        on run argv
            set inputPath to POSIX file (item 1 of argv)
            set outputPath to POSIX file (item 2 of argv)
            tell application "Pages"
                open inputPath
                set theDoc to front document
                export theDoc to outputPath as PDF
                close theDoc saving no
            end tell
        end run
        """,
        input_path,
        output_pdf,
    )


def _run_osascript(script, input_path, output_pdf):
    result = subprocess.run(
        ["osascript", "-", str(input_path), str(output_pdf)],
        input=script,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        raise ConversionError(stderr or f"osascript exited with code {result.returncode}")


def _app_exists(app_name):
    candidates = [
        Path("/Applications") / f"{app_name}.app",
        Path.home() / "Applications" / f"{app_name}.app",
    ]
    return any(path.exists() for path in candidates)
