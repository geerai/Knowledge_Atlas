# Ruthless Review Status — 2026-04-19

**Target reviewed:** tip of `master` in `Knowledge_Atlas` at review time  
**Verdict:** `CLEANED`  
**Summary:** two Codex-authored fix commits landed. The candidate tree now has 0 validator errors, the topic variants have their promised crosswalk payload, the approval dashboard is gated before its data becomes visible, and the tracked security leak found during Probe 9 has been removed.

## Probe-by-probe finding count

| Probe | Finding count | Notes |
|---|---:|---|
| 1. Broken links | 4 fixed | Repaired the stale PNU article link in `ka_articles.html`, restored the missing `#evidence` anchor target, repointed the stale archive replacement link, and removed the dead sibling-repo links from `ka_explain_system.html` by turning them into non-clickable source references. |
| 2. Unauthenticated admin paths | 1 fixed | `160sp/ka_approve.html` lacked the `isAdmin()`-style pre-display gate. A fixed overlay gate now blocks the page until `sessionStorage['ka.admin'] === 'yes'`. |
| 3. Persona-awareness regressions | 3 fixed | Removed maintainer-only footer notes from the public and student topic variants, simplified jargon on the home-page evidence strip, and kept the public topic surface on the public contribute path. |
| 4. Copy contradictions | 0 | The live top-level surfaces checked here matched the stated anchors; several older audit/docs references were stale, but the shipped pages were not contradicting the canonical numbers. |
| 5. Validator warnings above threshold | 0 blockers | `python3 scripts/site_validator.py` now reports **0 errors, 106 warnings**. The remaining `LNK001` warnings are archive items, template placeholders, or the validator’s encoded-space false positives. No remaining `SEC001` warning on an instructor-only page was judged deploy-blocking after the `ka_approve.html` gate was added. |
| 6. Mobile breakage | 0 blockers found | I did not run a live browser emulator inside this session. I inspected the responsive rules on the reviewed pages and found no release-blocking structural defect. A real staging-device pass is still prudent. |
| 7. Dead code | 7 flagged, retainable | No deletions beyond the sensitive snapshot. Retainable dead-code candidates remain: `ka_article.html`, `ka_demo.html`, `ka_demo_v04.html`, `ka_evidence.html`, `ka_gaps.html`, `160sp/article_finder_assignment_v1_archive.html`, and the frozen snapshot/archive trees. |
| 8. Payload staleness | 1 fixed | The five topic variants were wired to `data/ka_payloads/topic_crosswalk.json`, but the builder never emitted it. `scripts/build_ka_adapter_payloads.py` now generates the payload; the live file now exists with **102 rows, 18 outcomes, 9 architectural families**. |
| 9. Security leaks | 2 fixed | Deleted the tracked `160sp/ka_server_snapshot.txt` VM dump containing real user records, and removed the literal local-dev bootstrap password string from current and frozen code/docs. |

## Commits landed

- `0196b57` — `Ruthless-review fix: restore live topic and article navigation`
- `e6c0704` — `Ruthless-review fix: remove tracked sensitive artifacts`

## DK-decision items still open

1. Decide whether the retainable dead-code surfaces should stay in-tree as reference material or move to a separate archive branch/directory outside the deploy candidate.
2. Decide whether to spend another pass reducing the remaining 106 validator warnings, most of which are non-blocking placeholders or historical pages.
3. Run the planned staging-browser pass for the mobile probe, since this review could only do structural inspection rather than live viewport interaction.

## Verification state

- `python3 scripts/site_validator.py` → `0 errors`, `106 warnings`
- `python3 -m pytest tests/test_topic_crosswalk_builder.py -q` → `1 passed`
- `rg -n "atlas2026|ka_server_snapshot.txt" .` now finds only the local-output path inside `160sp/ka_server_snapshot.sh`, not a tracked snapshot or a literal credential string.

## Notes

- `data/ka_auth_secret.txt` exists locally but is already gitignored and was **not** a tracked repo leak.
- An unrelated untracked file, `160sp/ka_t4_page.css`, was left untouched.
