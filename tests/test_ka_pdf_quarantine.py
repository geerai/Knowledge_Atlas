from pathlib import Path

from scripts.ka_pdf_quarantine import validate_and_quarantine_pdf


MINIMAL_PDF = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n"


def test_validate_and_quarantine_pdf_accepts_minimal_pdf(tmp_path):
    src = tmp_path / "paper.pdf"
    src.write_bytes(MINIMAL_PDF)
    quarantine = tmp_path / "quarantine"

    result = validate_and_quarantine_pdf(src, quarantine)

    assert result.ok is True
    assert result.status == "accepted"
    assert result.quarantine_path is not None
    assert Path(result.quarantine_path).exists()
    assert result.sha256


def test_validate_and_quarantine_pdf_rejects_non_pdf_magic(tmp_path):
    src = tmp_path / "paper.pdf"
    src.write_bytes(b"not a pdf")
    quarantine = tmp_path / "quarantine"

    result = validate_and_quarantine_pdf(src, quarantine)

    assert result.ok is False
    assert result.status == "bad_file"
