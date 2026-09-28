# SPDX-License-Identifier: MIT
"""Command-line wrapper for OCRmyPDF-EasyOCR with Arabic defaults."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path


def build_command(
    executable: str,
    input_pdf: Path,
    output_pdf: Path,
    *,
    languages: str = "ara",
    gpu: bool = False,
    sidecar: Path | None = None,
    deskew: bool = False,
    rotate_pages: bool = False,
) -> list[str]:
    """Build an OCRmyPDF command that explicitly selects the EasyOCR plugin."""
    command = [
        executable,
        "--plugin",
        "ocrmypdf_easyocr",
        "--output-type",
        "pdf",
        "-l",
        languages,
    ]
    if not gpu:
        command.append("--easyocr-no-gpu")
    if sidecar is not None:
        command.extend(["--sidecar", str(sidecar)])
    if deskew:
        command.append("--deskew")
    if rotate_pages:
        command.append("--rotate-pages")
    command.extend([str(input_pdf), str(output_pdf)])
    return command


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arabic-pdf-ocr",
        description=(
            "Create a searchable PDF using EasyOCR through the OCRmyPDF plugin. "
            "Arabic is the default language."
        ),
    )
    parser.add_argument("input_pdf", type=Path, help="scanned or image-based PDF")
    parser.add_argument("output_pdf", type=Path, help="destination searchable PDF")
    parser.add_argument(
        "-l",
        "--languages",
        default="ara",
        help="OCRmyPDF language codes joined by '+', e.g. ara or ara+eng (default: ara)",
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="enable EasyOCR's GPU mode; by default the tool runs on CPU",
    )
    parser.add_argument(
        "--sidecar",
        type=Path,
        help="also save recognized text to this UTF-8 text file",
    )
    parser.add_argument(
        "--deskew",
        action="store_true",
        help="correct slightly crooked pages before OCR (uses OpenCV)",
    )
    parser.add_argument(
        "--rotate-pages",
        action="store_true",
        help="correct pages scanned in the wrong orientation (requires Tesseract)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    executable = shutil.which("ocrmypdf")
    if executable is None:
        parser.error(
            "could not find the 'ocrmypdf' command; install OCRmyPDF in this environment"
        )
    command = build_command(
        executable,
        args.input_pdf,
        args.output_pdf,
        languages=args.languages,
        gpu=args.gpu,
        sidecar=args.sidecar,
        deskew=args.deskew,
        rotate_pages=args.rotate_pages,
    )
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
