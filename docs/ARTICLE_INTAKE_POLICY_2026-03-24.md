# Article Intake Policy

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Purpose: define the operating policy for PDF-first article intake in Knowledge Atlas

## Working reminder

When we return to gold-standard ontology or rebuild adjudication work, switch to extra-high reasoning.

For current GUI and intake work, that is not necessary.

## Intake goals

The intake flow should optimize for:
1. low friction for Track 2 contributors
2. immediate duplicate protection
3. relevance control without blocking uploads in real time
4. minimal wasted disk usage
5. safe handling of anonymous or public uploads
6. support multiple intake modes without forcing one workflow on everyone
7. distinguish student accounting from ordinary public contribution

## Intake audiences

Public contributors and COGS 160 Track 2 students should use the same core intake surface and backend contract.

What differs is not the basic intake mechanism. What differs is:
- attribution
- quota/accounting
- workflow hints
- dashboard/reporting

### Shared intake surface

The system should support all of these entry modes:
1. upload one PDF
2. upload a batch or folder of PDFs
3. paste one citation
4. paste a list of citations
5. upload a citation file (`.txt`, `.csv`, `.ris`, `.bib` / BibTeX)
6. optionally enrich from DOI/title lookup before or after upload

### Identity-dependent behavior

If the user is anonymous / public:
- allow submission without login
- attribute as public/unclaimed contributor
- do not count toward student quotas

If the user is a logged-in Track 2 student:
- attribute submissions to that student
- count accepted citation and PDF contributions
- expose progress against course targets
- preserve the same underlying intake mechanics

### Track 2 discipline still matters

Even if students use the same intake surface, the course still expects them to:
- search systematically
- screen citations and abstracts
- decide Include / Exclude / Uncertain
- acquire PDFs for Include-status papers
- then push accepted candidates into intake

So:
- same intake surface
- different surrounding pedagogy and accounting

## Recommended intake sequence

### 1. Immediate duplicate check

As soon as the user selects or drops a PDF:
- inspect the PDF locally
- try to extract DOI, title, author, and year
- check against existing article records immediately

Decision:
- if the article is already in KA, stop intake immediately
- do not keep a second stored copy of the PDF
- show the user the matched existing record

This should be real-time.

## 2. Temporary intake staging

If the article does not appear to be a duplicate:
- allow temporary staging
- attach extracted metadata
- defer final acceptance until review

The staged object should be treated as:
- pending
- not yet accepted into the permanent corpus

## 2.5. File safety and hostile-upload protection

Anonymous/public upload means the backend must treat every uploaded file as untrusted.

Minimum requirements:
1. verify actual file type by magic bytes and parser inspection, not filename alone
2. reject encrypted, password-protected, malformed, oversized, or suspicious PDFs
3. quarantine uploads before any permanent save
4. compute file hash immediately for dedupe and audit
5. never execute or render uploaded active content directly in the main web app context
6. process PDFs in an isolated worker/container
7. virus-scan and structure-check before promoting from quarantine
8. delete rejected bad files promptly

Recommended concrete checks:
- extension check: `.pdf`
- MIME sniff / magic bytes check: `%PDF-`
- parser validation with a real PDF library
- max file size cap
- max page count cap
- encrypted-file rejection
- hash-based duplicate detection
- quarantine directory separate from permanent corpus

Operational rule:
- viewing the filename is not enough
- "named pdf" is not trusted
- only validated PDFs advance past quarantine

## 3. Relevance triage should be asynchronous

Relevance should not be the main real-time bottleneck.

Recommended policy:
- allow staging first
- run relevance triage in a nightly or scheduled review process

Reason:
- real-time relevance review slows contributors down
- many borderline cases require comparative judgment, not immediate gatekeeping
- nightly review gives maintainers a chance to batch decisions coherently

## 4. Storage rule for staged PDFs

Because disk space is constrained:
- do not retain rejected staged PDFs indefinitely

Recommended rule:
1. if duplicate: do not save permanent copy
2. if staged and later rejected as irrelevant:
- remove the staged PDF promptly
- keep metadata/audit record of the rejection
3. if accepted:
- move to the permanent intake/extraction queue

## 5. Audit record

Even when a staged PDF is deleted, retain a lightweight audit record:
- why it was rejected
- who submitted it
- when it was reviewed
- whether it matched an existing article

This gives traceability without keeping the file.

## Recommended states

Use these intake states:
- `duplicate_existing`
- `staged_pending_review`
- `accepted_for_extraction`
- `rejected_irrelevant`
- `rejected_bad_file`

## Operational rule

Immediate:
- duplicate detection

Deferred:
- relevance adjudication
- final retention decision

## Design implication for the GUI

The intake page should therefore be PDF-first and show:
1. metadata extraction
2. duplicate test
3. staging confirmation
4. later review status

It should not force the contributor to do full APA and relevance judgment before the file can enter staging.

It should also:
1. explain that files are scanned/validated before acceptance
2. offer multiple input modes, not just one-at-a-time PDF upload
3. adapt hints and progress display based on user identity
4. route Track 2 users toward the assignment/setup material when they need the fuller course workflow
