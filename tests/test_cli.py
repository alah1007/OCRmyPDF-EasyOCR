# SPDX-License-Identifier: MIT

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

# Load the lightweight CLI module directly so unit tests do not import EasyOCR,
# download models, or require heavyweight OCR dependencies just to test argv.
CLI_PATH = Path(__file__).parents[1] / "ocrmypdf_easyocr" / "cli.py"
CLI_SPEC = spec_from_file_location("ocrmypdf_easyocr_cli", CLI_PATH)
assert CLI_SPEC is not None and CLI_SPEC.loader is not None
cli = module_from_spec(CLI_SPEC)
CLI_SPEC.loader.exec_module(cli)


def test_build_command_defaults_to_arabic_and_cpu():
    command = cli.build_command("ocrmypdf", Path("scan.pdf"), Path("searchable.pdf"))

    assert command == [
        "ocrmypdf",
        "--plugin",
        "ocrmypdf_easyocr",
        "--output-type",
        "pdf",
        "-l",
        "ara",
        "--easyocr-no-gpu",
        "scan.pdf",
        "searchable.pdf",
    ]


def test_build_command_supports_bilingual_gpu_and_extras():
    command = cli.build_command(
        "ocrmypdf",
        Path("scan.pdf"),
        Path("searchable.pdf"),
        languages="ara+eng",
        gpu=True,
        sidecar=Path("recognized.txt"),
        deskew=True,
        rotate_pages=True,
    )

    assert "ara+eng" in command
    assert "--easyocr-no-gpu" not in command
    assert command[command.index("--sidecar") + 1] == "recognized.txt"
    assert "--deskew" in command
    assert "--rotate-pages" in command
    assert command[-2:] == ["scan.pdf", "searchable.pdf"]


def test_main_returns_ocrmypdf_status(monkeypatch):
    expected = [
        "/usr/bin/ocrmypdf",
        "--plugin",
        "ocrmypdf_easyocr",
        "--output-type",
        "pdf",
        "-l",
        "ara",
        "--easyocr-no-gpu",
        "scan.pdf",
        "searchable.pdf",
    ]
    monkeypatch.setattr(cli.shutil, "which", lambda _: "/usr/bin/ocrmypdf")

    class Completed:
        returncode = 7

    def fake_run(command, *, check):
        assert command == expected
        assert check is False
        return Completed()

    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    assert cli.main(["scan.pdf", "searchable.pdf"]) == 7


def test_main_explains_missing_ocrmypdf(monkeypatch):
    monkeypatch.setattr(cli.shutil, "which", lambda _: None)

    with pytest.raises(SystemExit) as error:
        cli.main(["scan.pdf", "searchable.pdf"])

    assert error.value.code == 2
