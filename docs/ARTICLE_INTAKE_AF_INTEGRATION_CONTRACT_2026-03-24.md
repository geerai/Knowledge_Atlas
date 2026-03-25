# Article Intake + AF Integration Contract

Date: 2026-03-24
Repos:
- `/Users/davidusa/REPOS/Knowledge_Atlas`
- `/Users/davidusa/REPOS/Article_Finder_v3_2_3`

Purpose: define the unified intake contract for Knowledge Atlas and tie it to real capabilities already present in the Article Finder stack.

## Main decision

There should be one core intake surface and one core intake backend.

Do not create:
- one public uploader
- one student uploader
- one PDF uploader
- one citation uploader

Instead, create:
- one intake surface with multiple input modes
- one backend contract
- identity-aware accounting and reporting

## Supported input modes

The intake surface should accept:
1. single PDF
2. batch / folder of PDFs
3. single pasted citation
4. pasted citation list
5. uploaded citation file:
   - `.txt`
   - `.csv`
   - `.ris`
   - `.bib`
6. optional DOI-only or title-only entry

## Identity model

### Anonymous / public
- may submit without login
- submission marked as `public_unclaimed`
- no student credit
- minimal dashboard

### Logged-in student
- submission linked to user ID
- accepted citation and PDF counts tracked
- visible progress vs. track targets
- queued items visible in student dashboard

### Logged-in contributor / maintainer
- submission linked to user ID
- reviewer/maintainer actions available
- moderation and adjudication tools visible

## Shared backend stages

Every intake item should pass through the same backend stages:

1. `receive`
2. `normalize`
3. `validate`
4. `deduplicate`
5. `metadata_enrich`
6. `stage`
7. `review`
8. `accept_or_reject`
9. `route_to_extraction`

## AF capabilities already available

The current Article Finder repo already contains the right primitives:

### Citation-side
- citation parser:
  - `ingest/citation_parser.py`
- file import:
  - `cmd_import` in `cli/main.py`
- DOI resolution:
  - `ingest/doi_resolver.py`
- Crossref/OpenAlex enrichment hooks:
  - `cmd_import`, resolver wiring in `cli/main.py`

### PDF-side
- PDF directory import:
  - `cmd_import_pdfs` in `cli/main.py`
- inbox-style PDF processing:
  - `cmd_inbox` in `cli/main.py`
- filename parsing + DOI extraction + PDF text verification:
  - `ingest/pdf_cataloger.py`
- hash computation:
  - `ingest/pdf_cataloger.py`

### Corpus-side
- duplicate-aware import/update behavior
- PDF matching
- citation network expansion
- export to Article Eater pipeline

Implication:
- KA should call or wrap AF capabilities
- KA should not invent a second disconnected intake engine

## Suggested KA -> AF adapter boundary

### Request object

```json
{
  "submission_id": "KA-IN-000123",
  "submitted_by": {
    "identity_type": "anonymous|student|contributor|maintainer",
    "user_id": "optional-user-id",
    "track": "optional-track-id"
  },
  "input_mode": "pdf_batch|pdf_single|citation_list|citation_file|doi_only|title_only",
  "items": [
    {
      "local_path": "optional path to uploaded file",
      "raw_text": "optional citation text",
      "doi": "optional doi",
      "title": "optional title"
    }
  ],
  "source_context": {
    "surface": "ka_article_propose",
    "course_context": "optional",
    "notes": "optional"
  }
}
```

### Response object

```json
{
  "submission_id": "KA-IN-000123",
  "items": [
    {
      "item_id": "KA-IN-000123-01",
      "input_mode": "pdf_single",
      "validation_status": "accepted|bad_file|encrypted|malformed|oversize",
      "duplicate_status": "duplicate_existing|possible_duplicate|not_duplicate",
      "metadata": {
        "doi": "optional",
        "title": "optional",
        "authors": [],
        "year": 2020,
        "confidence": "high|medium|low"
      },
      "next_state": "staged_pending_review|rejected_bad_file|duplicate_existing"
    }
  ]
}
```

## Review/accounting rules

### Accepted citation contribution
Count for a student if:
- item is accepted into corpus
- metadata is good enough to create or update a real paper record

### Accepted PDF contribution
Count for a student if:
- uploaded PDF is valid
- not duplicate
- linked to accepted paper record
- staged/accepted into extraction path

### Public contribution
Never counted toward student metrics.

## Security requirements

Anonymous uploads are untrusted.

Minimum enforcement:
1. magic-byte / MIME validation
2. parser validation
3. hash on receipt
4. quarantine before permanent storage
5. isolated worker processing
6. encrypted/malformed rejection
7. prompt deletion of rejected bad files

## GUI implications

### `ka_article_propose.html`
Should become a multi-mode intake page:
- PDF batch
- citation paste
- citation file upload
- DOI/title quick entry

### `ka_datacapture.html`
Currently still encodes single-item, citation-first assumptions and should be normalized or deprecated.

### Student dashboards
Should show:
- submitted citations
- accepted citations
- PDFs staged
- PDFs accepted
- duplicates blocked
- rejected items

### Anonymous users
Should see:
- low-friction submission
- duplicate result
- staged/review status if they keep a submission token

## API/secrets note

I do not currently assume access to live Elicit or other private API keys.

If David provides:
- Elicit API key
- Semantic Scholar key
- other relevant keys

then the adapter layer should use them through configured secrets, not hard-coded page logic.

## Immediate next implementation steps

1. normalize `ka_datacapture.html` or retire it behind the new intake model
2. define the KA intake adapter that calls AF import primitives
3. add identity-aware contribution accounting
4. add real quarantine + validation before any permanent file save
