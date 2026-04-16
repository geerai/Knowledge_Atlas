from __future__ import annotations

import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    from scripts.ka_pdf_quarantine import validate_and_quarantine_pdf
except ImportError:  # pragma: no cover
    from ka_pdf_quarantine import validate_and_quarantine_pdf


ROOT = Path(__file__).resolve().parents[1]
REPOS_ROOT = ROOT.parent
AF_ROOT = REPOS_ROOT / "Article_Finder_v3_2_3"
if str(AF_ROOT) not in sys.path:
    sys.path.insert(0, str(AF_ROOT))

from ingest.citation_parser import CitationParser  # type: ignore  # noqa: E402
from ingest.pdf_cataloger import FilenameParser  # type: ignore  # noqa: E402


@dataclass
class IntakeIdentity:
    identity_type: str
    user_id: Optional[str] = None
    track: Optional[str] = None


@dataclass
class IntakeItem:
    item_id: str
    input_mode: str
    local_path: Optional[str] = None
    raw_text: Optional[str] = None
    doi: Optional[str] = None
    title: Optional[str] = None


@dataclass
class IntakeSubmission:
    submission_id: str
    submitted_by: IntakeIdentity
    input_mode: str
    items: list[IntakeItem]
    source_context: dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedIntakeItem:
    item_id: str
    input_mode: str
    validation_status: str
    duplicate_status: str
    metadata: dict[str, Any]
    next_state: str
    quarantine: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict:
        return asdict(self)


class KAArticleIntakeAdapter:
    def __init__(self, quarantine_dir: Path):
        self.quarantine_dir = Path(quarantine_dir)
        self.citation_parser = CitationParser()
        self.filename_parser = FilenameParser()

    def process_submission(self, submission: IntakeSubmission) -> dict[str, Any]:
        normalized = []
        for item in submission.items:
            if item.input_mode.startswith("pdf"):
                normalized.append(self._process_pdf_item(item))
            else:
                normalized.append(self._process_citation_item(item))

        return {
            "submission_id": submission.submission_id,
            "identity": asdict(submission.submitted_by),
            "items": [n.to_dict() for n in normalized],
        }

    def _process_pdf_item(self, item: IntakeItem) -> NormalizedIntakeItem:
        if not item.local_path:
            return NormalizedIntakeItem(
                item_id=item.item_id,
                input_mode=item.input_mode,
                validation_status="bad_file",
                duplicate_status="unknown",
                metadata={},
                next_state="rejected_bad_file",
            )

        source_path = Path(item.local_path)
        validation = validate_and_quarantine_pdf(source_path, self.quarantine_dir)
        if not validation.ok:
            return NormalizedIntakeItem(
                item_id=item.item_id,
                input_mode=item.input_mode,
                validation_status=validation.status,
                duplicate_status="unknown",
                metadata={},
                next_state="rejected_bad_file",
                quarantine=validation.to_dict(),
            )

        parsed = self.filename_parser.parse(source_path.name)
        metadata = {
            "doi": parsed.doi,
            "title": parsed.title,
            "authors": parsed.authors,
            "year": parsed.year,
            "confidence": parsed.confidence,
            "extraction_method": parsed.extraction_method,
            "sha256": validation.sha256,
        }
        return NormalizedIntakeItem(
            item_id=item.item_id,
            input_mode=item.input_mode,
            validation_status=validation.status,
            duplicate_status="not_checked",
            metadata=metadata,
            next_state="staged_pending_review",
            quarantine=validation.to_dict(),
        )

    def _process_citation_item(self, item: IntakeItem) -> NormalizedIntakeItem:
        raw = item.raw_text or item.title or item.doi or ""
        parsed = self.citation_parser.parse(raw)
        metadata = {
            "doi": parsed.doi or item.doi,
            "title": parsed.title or item.title,
            "authors": parsed.authors,
            "year": parsed.year,
            "venue": parsed.venue,
            "confidence": parsed.confidence,
            "parse_method": parsed.parse_method,
        }
        return NormalizedIntakeItem(
            item_id=item.item_id,
            input_mode=item.input_mode,
            validation_status="accepted",
            duplicate_status="not_checked",
            metadata=metadata,
            next_state="staged_pending_review",
        )


def derive_submission_credit_status(identity: IntakeIdentity) -> dict[str, Any]:
    if identity.identity_type == "student":
        return {
            "counts_for_student_credit": True,
            "dashboard_mode": "student_progress",
            "contribution_bucket": f"track:{identity.track or 'unassigned'}",
        }
    if identity.identity_type in {"contributor", "maintainer"}:
        return {
            "counts_for_student_credit": False,
            "dashboard_mode": "contributor_review",
            "contribution_bucket": identity.identity_type,
        }
    return {
        "counts_for_student_credit": False,
        "dashboard_mode": "public_unclaimed",
        "contribution_bucket": "public_unclaimed",
    }
