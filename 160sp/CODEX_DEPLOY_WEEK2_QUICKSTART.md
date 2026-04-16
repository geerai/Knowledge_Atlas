# Codex Deployment Prompt: Week 2 Quickstart + CORS + Context File Updates

**Created**: 2026-04-08
**Author**: CW (Cowork session)
**For**: Codex to deploy to xrlab.ucsd.edu
**Priority**: URGENT — class is tomorrow (Wed April 9)

---

## Task Summary

Deploy 8 files from the local Knowledge_Atlas repo to the live server at `xrlab.ucsd.edu`. Then add a "Quickstart" link to the existing `week2_exercises.html` page. All files are already created and ready — this is purely a deployment task.

## Files to Deploy

All source files are in `/Users/davidusa/REPOS/Knowledge_Atlas/`. Deploy them to the matching paths on `xrlab.ucsd.edu/ka/`.

| Local Path | Server Path | What It Is |
|-----------|------------|------------|
| `160sp/week2_quickstart.html` | `/ka/160sp/week2_quickstart.html` | **NEW** — Student quickstart guide for Week 2 exercises |
| `data/ka_payloads/.htaccess` | `/ka/data/ka_payloads/.htaccess` | **NEW** — Enables CORS headers so student code can fetch JSON data when running locally |
| `160sp/context/context_ex0_mechanism_pathway.md` | `/ka/160sp/context/context_ex0_mechanism_pathway.md` | **UPDATED** — Full `https://xrlab.ucsd.edu/ka/` URLs added to Technical Environment section |
| `160sp/context/context_exA_trust_panel.md` | `/ka/160sp/context/context_exA_trust_panel.md` | **UPDATED** — Same URL update |
| `160sp/context/context_exB_debate_visualizer.md` | `/ka/160sp/context/context_exB_debate_visualizer.md` | **UPDATED** — Same URL update |
| `160sp/context/context_exC_warrant_calculator.md` | `/ka/160sp/context/context_exC_warrant_calculator.md` | **UPDATED** — Same URL update |
| `160sp/context/context_exD_search_filter.md` | `/ka/160sp/context/context_exD_search_filter.md` | **UPDATED** — Same URL update |

## Modification to Existing Page

**File**: `160sp/week2_exercises.html` (already on server)

**Change**: Add a "Quickstart" link to the top navigation bar. Find this HTML block:

```html
<nav class="top-nav">
  <a href="../ka_home.html" class="nav-brand">K-ATLAS</a>
  <span class="nav-sep">|</span>
  <a href="ka_schedule.html" class="nav-link">Schedule</a>
  <a href="ka_student_setup.html" class="nav-link">Setup</a>
  <a href="week2_agenda.html" class="nav-link">Week 2</a>
  <a href="../ka_evidence.html" class="nav-link">Evidence</a>
  <a href="../ka_demo_v04.html" class="nav-link">Ask</a>
```

Insert this line after the "Setup" link:

```html
  <a href="week2_quickstart.html" class="nav-link" style="background:rgba(232,135,42,0.2); color:#F5A623; font-weight:600;">⚡ Quickstart</a>
```

This gives it a subtle amber highlight so students notice it.

**Also**: Add a prominent quickstart callout near the top of the page content (after the hero section and before the "How This Works" section). Insert this block:

```html
<div class="page-wrap" style="padding-top: 0;">
  <div style="background: #FFF3E0; border: 2px solid #E8872A; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem;">
    <span style="font-size: 1.5rem;">⚡</span>
    <div>
      <strong style="color: #9a5010; font-size: 1rem;">New: Exercise Quickstart Guide</strong>
      <p style="margin: 0.3rem 0 0; font-size: 0.92rem; color: #5a3a10;">Everything you need to start — context files, data access, and setup — in under 5 minutes. <a href="week2_quickstart.html" style="color: #E8872A; font-weight: 600;">Open Quickstart →</a></p>
    </div>
  </div>
</div>
```

## CORS Verification

After deploying the `.htaccess`, verify CORS is working by running:

```bash
curl -sI -H "Origin: http://localhost:8000" "https://xrlab.ucsd.edu/ka/data/ka_payloads/evidence.json" | grep -i "access-control"
```

Expected output:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

If no CORS headers appear, the server may not have `mod_headers` enabled. In that case, run:
```bash
sudo a2enmod headers
sudo systemctl restart apache2
```

Then verify again.

## Verification Checklist

After deployment, verify all of these:

1. `https://xrlab.ucsd.edu/ka/160sp/week2_quickstart.html` loads and displays correctly
2. `https://xrlab.ucsd.edu/ka/160sp/week2_exercises.html` has the new "⚡ Quickstart" nav link and the amber callout box
3. All 5 context file download links on the quickstart page work:
   - `https://xrlab.ucsd.edu/ka/160sp/context/context_ex0_mechanism_pathway.md`
   - `https://xrlab.ucsd.edu/ka/160sp/context/context_exA_trust_panel.md`
   - `https://xrlab.ucsd.edu/ka/160sp/context/context_exB_debate_visualizer.md`
   - `https://xrlab.ucsd.edu/ka/160sp/context/context_exC_warrant_calculator.md`
   - `https://xrlab.ucsd.edu/ka/160sp/context/context_exD_search_filter.md`
4. Context files contain `https://xrlab.ucsd.edu/ka/` URLs (not relative paths)
5. CORS headers are present on data payloads (see curl test above)
6. The "Evidence Explorer" and "Argumentation Viewer" links on the quickstart page work

## What Changed in the Context Files

Each context file's "Technical Environment" section was updated from:
```
- Data loaded via `fetch('data/ka_payloads/evidence.json')`
```
to:
```
- **Data is loaded via fetch() using the full URL:**
  - `fetch('https://xrlab.ucsd.edu/ka/data/ka_payloads/evidence.json')`
- **IMPORTANT:** Always use the full `https://xrlab.ucsd.edu/ka/` URLs in fetch() calls so your code works from any location without needing to clone the repository
```

This ensures that when students paste the context file into their AI, the AI generates code with full URLs that work from any location.

## Do NOT Modify

- `week2_exercises.html` content beyond the nav link and quickstart callout — the exercise descriptions, grading rubric, etc. are final
- `data/ka_payloads/*.json` — the data files are correct as-is
- Any files outside the `160sp/` and `data/ka_payloads/` directories
