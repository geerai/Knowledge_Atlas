# Knowledge_Atlas Backup Batches

Date: 2026-03-24
Purpose: split the current dirty `Knowledge_Atlas` worktree into clean backup-safe commit groups

## Current dirty shape

Tracked modified:
- `TASKS.md`
- `ka_article_propose.html`
- `ka_datacapture.html`
- `ka_topics.html`

Untracked:
- large doc/spec layer
- `ka_mode_switch.js`
- intake scripts
- tests

## Recommended commit batches

### Batch 1 — IA and sprint governance docs

Files:
- `docs/CANONICAL_SITE_FAMILY_MAP_2026-03-24.md`
- `docs/DUPLICATE_PAGE_DISPOSITIONS_2026-03-24.md`
- `docs/EMBEDDED_DE_PAGE_DISPOSITIONS_2026-03-24.md`
- `docs/GUI_DATA_CONTRACTS_2026-03-24.md`
- `docs/GUI_RUTHLESS_AUDIT_2026-03-24.md`
- `docs/GUI_UNIFICATION_AND_REBUILD_SPRINT_PLAN_2026-03-24.md`
- `docs/SPRINT_STATUS_SUMMARY_2026-03-24.md`
- `docs/UNIFIED_NAV_MODEL_2026-03-24.md`
- `docs/TOPIC_SELECTION_POLICY_2026-03-24.md`
- `TASKS.md`

### Batch 2 — theory / neural architecture

Files:
- `docs/AG_THEORY_AND_MECHANISM_REVIEW_2026-03-24.md`
- `docs/INITIAL_NEURAL_PATHWAY_INVENTORY_2026-03-24.md`
- `docs/NEURAL_UNDERPINNINGS_ARCHITECTURE_2026-03-24.md`
- `docs/THEORY_GUIDES_ARCHITECTURE_2026-03-24.md`
- `docs/THEORY_GUIDES_INTEGRATION_PLAN_2026-03-24.md`
- `docs/TRACK2_NEURAL_PATHWAY_ASSIGNMENT_SHEET_2026-03-24.md`

### Batch 3 — mode switch and topic UI

Files:
- `ka_mode_switch.js`
- `ka_topics.html`
- relevant nav/mode docs:
  - `docs/MODE_SWITCH_COMPONENT_SPEC_2026-03-24.md`
  - `docs/NAV_PREFERENCE_SIGNUP_AND_SETUP_INTEGRATION_2026-03-24.md`

### Batch 4 — intake architecture and contributor flow

Files:
- `ka_article_propose.html`
- `ka_datacapture.html`
- `scripts/ka_af_intake_adapter.py`
- `scripts/ka_pdf_quarantine.py`
- `scripts/__init__.py`
- `tests/conftest.py`
- `tests/test_ka_af_intake_adapter.py`
- `tests/test_ka_pdf_quarantine.py`
- `docs/ARTICLE_INTAKE_AF_INTEGRATION_CONTRACT_2026-03-24.md`
- `docs/ARTICLE_INTAKE_POLICY_2026-03-24.md`
- `docs/ARTICLE_FINDER_API_OPERATIONS_2026-03-24.md`
- `docs/OPENALEX_SUPPORT_EMAIL_DRAFT_2026-03-24.md`

### Batch 5 — repo governance / backup cleanup

Files:
- `docs/REPO_INVENTORY_2026-03-24.md`
- `docs/REPO_STABILIZATION_AND_BACKUP_PLAN_2026-03-24.md`

## Existing earlier GUI-agent batch

Already pushed:
- GUI design agent docs/checker/test batch
- no action needed except to keep later work separate from it

## Non-commit noise to handle

Should not be committed:
- `scripts/__pycache__/`
- `tests/__pycache__/`

These should be ignored or left unstaged.
