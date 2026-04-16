from __future__ import annotations

import hashlib
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


DEFAULT_MAX_SIZE_BYTES = 100 * 1024 * 1024


@dataclass
class PDFValidationResult:
    source_path: str
    quarantine_path: Optional[str]
    sha256: Optional[str]
    file_size_bytes: int
    page_count: Optional[int]
    ok: bool
    status: str
    reason: str
    encrypted: bool = False
    used_parser: str = "minimal"

    def to_dict(self) -> dict:
        return asdict(self)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def looks_like_pdf(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            header = fh.read(8)
        return header.startswith(b"%PDF-")
    except OSError:
        return False


def has_pdf_eof(path: Path) -> bool:
    try:
        with path.open("rb") as fh:
            fh.seek(max(0, path.stat().st_size - 2048))
            tail = fh.read()
        return b"%%EOF" in tail
    except OSError:
        return False


def try_parse_pdf(path: Path) -> tuple[Optional[int], bool, str]:
    try:
        import pypdf  # type: ignore

        reader = pypdf.PdfReader(str(path))
        encrypted = bool(getattr(reader, "is_encrypted", False))
        page_count = len(reader.pages) if not encrypted else None
        return page_count, encrypted, "pypdf"
    except Exception:
        return None, False, "minimal"


def validate_and_quarantine_pdf(
    source_path: Path,
    quarantine_dir: Path,
    *,
    max_size_bytes: int = DEFAULT_MAX_SIZE_BYTES,
    max_pages: Optional[int] = None,
) -> PDFValidationResult:
    source_path = Path(source_path)
    quarantine_dir = Path(quarantine_dir)

    if not source_path.exists() or not source_path.is_file():
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=0,
            page_count=None,
            ok=False,
            status="missing",
            reason="Source file does not exist.",
        )

    file_size = source_path.stat().st_size
    if file_size <= 0:
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=file_size,
            page_count=None,
            ok=False,
            status="bad_file",
            reason="File is empty.",
        )

    if file_size > max_size_bytes:
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=file_size,
            page_count=None,
            ok=False,
            status="oversize",
            reason=f"File exceeds max size ({max_size_bytes} bytes).",
        )

    if source_path.suffix.lower() != ".pdf":
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=file_size,
            page_count=None,
            ok=False,
            status="bad_file",
            reason="File extension is not .pdf.",
        )

    if not looks_like_pdf(source_path):
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=file_size,
            page_count=None,
            ok=False,
            status="bad_file",
            reason="Magic bytes do not indicate a PDF.",
        )

    if not has_pdf_eof(source_path):
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=file_size,
            page_count=None,
            ok=False,
            status="malformed",
            reason="PDF EOF marker missing.",
        )

    page_count, encrypted, parser_name = try_parse_pdf(source_path)
    if encrypted:
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=file_size,
            page_count=page_count,
            ok=False,
            status="encrypted",
            reason="Encrypted PDFs are rejected.",
            encrypted=True,
            used_parser=parser_name,
        )

    if max_pages is not None and page_count is not None and page_count > max_pages:
        return PDFValidationResult(
            source_path=str(source_path),
            quarantine_path=None,
            sha256=None,
            file_size_bytes=file_size,
            page_count=page_count,
            ok=False,
            status="oversize",
            reason=f"PDF exceeds max pages ({max_pages}).",
            used_parser=parser_name,
        )

    file_hash = sha256_file(source_path)
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    quarantine_path = quarantine_dir / f"{file_hash}.pdf"
    shutil.copy2(source_path, quarantine_path)

    return PDFValidationResult(
        source_path=str(source_path),
        quarantine_path=str(quarantine_path),
        sha256=file_hash,
        file_size_bytes=file_size,
        page_count=page_count,
        ok=True,
        status="accepted",
        reason="Validated and copied to quarantine.",
        used_parser=parser_name,
    )
