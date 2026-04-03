# Theory Explorer Expert Panel Review: Document Index

**Date**: 2026-04-03
**Project**: Knowledge Atlas Theory/Mechanism Explorer Home Page Design
**Status**: COMPLETE — 4 Documents + Index

---

## Document Navigator

### 1. **EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03.md**
**Length**: ~8,000 words | **Reading time**: 30–40 minutes

**For whom**: Decision-makers, stakeholders, anyone wanting the full intellectual context

**What's in it**:
- Executive summary (2 pages)
- The proposed design (6-card system overview)
- **Individual panelist positions** (5 sections, ~1,200 words each):
  - Carl Craver (mechanistic explanation, multi-level mechanisms)
  - Peter Machamer (entity-activity semantics)
  - Lindley Darden (mechanism discovery, schema gaps)
  - Paul Thagard (explanatory coherence, ECHO scoring)
  - James Woodward (interventionist causation)
- Panel consensus and disagreements
- **Integrated recommendations** for revised 6-card design
- References (philosophy of science literature)

**Read this if you**: Want to understand the intellectual foundations; need to convince skeptics; are making budget/timeline decisions

**Skip if you**: Just want to know what to build (go to Quick Reference or Handoff doc instead)

---

### 2. **IMPLEMENTATION_GUIDE_THEORY_EXPLORER_2026-04-03.md**
**Length**: ~6,500 words | **Reading time**: 20–30 minutes

**For whom**: Development team, technical leads, product manager

**What's in it**:
- Quick-reference table (what changes per card, effort estimates)
- **Card-by-card implementation details** (5 cards):
  - Neural Frameworks (minor update)
  - Theory Comparison (major revision: data model, React components, effort)
  - Mechanism Chain (major revision: pyramid visualization, color-coded status)
  - Critical Test (major revision: discrimination index, coherence impact)
  - Warrant Structure (no changes)
  - Underdetermination Alert (medium revision)
- **Data models** in JSON for each card
- **React/TypeScript code templates** for key components
- Effort estimates per card (total: 10–12 weeks)
- Success metrics and QA checklist
- Risk mitigation strategies

**Read this if you**: Are implementing the design; need technical specifications; need to estimate capacity/timeline

**Skip if you**: Are making strategic decisions (read Handoff doc) or need high-level overview (read Quick Reference)

---

### 3. **PANEL_SUMMARY_QUICK_REFERENCE_2026-04-03.md**
**Length**: ~1,500 words | **Reading time**: 5–10 minutes

**For whom**: Team quick reference, content creators, anyone in a hurry

**What's in it**:
- One-paragraph summary of each panelist's core insight
- **Visual table**: What each card should contain (by panelist perspective)
- Implementation priority timeline
- **Content creator checklists**:
  - Mechanism description checklist (7 items)
  - Theory comparison checklist (5 items)
  - Critical test checklist (8 items)
- Key philosophy of science references
- Questions to ask during implementation
- Success criteria (user perspective)

**Read this if you**: Need a quick summary; are creating content; are in status meetings

**Always** keep this on your desk during implementation.

---

### 4. **PANEL_TO_DEVELOPMENT_HANDOFF_2026-04-03.md**
**Length**: ~3,500 words | **Reading time**: 15–20 minutes

**For whom**: Stakeholders, development manager, anyone moving from planning to execution

**What's in it**:
- What changed from original proposal (side-by-side)
- Key design decisions (5 major decisions with rationale)
- Effort & timeline breakdown (4 phases, 10–12 weeks)
- Resource requirements (team roles, hours)
- What stays the same vs. what's new
- **Decision points requiring sign-off** before development:
  1. Coherence formula sign-off
  2. Schema-gap color scheme
  3. Content population strategy
  4. Critical test sourcing
  5. Supporting pages priority
- Risk register (5 risks with probability/impact/mitigation)
- Success criteria for phase completion
- Open questions for panelists
- Next steps (Week 0 immediate actions)

**Read this if you**: Are responsible for greenlight decision; managing development; coordinating with experts

**Use this as**: The bridge between high-level strategy and implementation details

---

### 5. **INDEX_THEORY_EXPLORER_PANEL_2026-04-03.md** (This Document)
**Your starting point for understanding what exists and where to go.**

---

## Quick Start: What Should I Read?

### "I have 5 minutes"
→ Read **PANEL_SUMMARY_QUICK_REFERENCE_2026-04-03.md** (first 2 pages)

### "I have 15 minutes"
→ Read **PANEL_TO_DEVELOPMENT_HANDOFF_2026-04-03.md** (sections: "What Changed" + "Key Design Decisions")

### "I have 30 minutes (strategic decision)"
→ Read:
1. EXPERT_PANEL_THEORY_EXPLORER_DESIGN: Executive Summary + Consensus section
2. PANEL_TO_DEVELOPMENT_HANDOFF: All sections except nitty-gritty technical

### "I have 1 hour (building the thing)"
→ Read:
1. PANEL_SUMMARY_QUICK_REFERENCE: All
2. IMPLEMENTATION_GUIDE: All except code templates

### "I have 2+ hours (deep understanding)"
→ Read all 4 documents in order:
1. EXPERT_PANEL_THEORY_EXPLORER_DESIGN (foundational)
2. PANEL_SUMMARY_QUICK_REFERENCE (orientation)
3. PANEL_TO_DEVELOPMENT_HANDOFF (decision/planning)
4. IMPLEMENTATION_GUIDE (technical execution)

---

## The Five Intellectual Traditions (One-Liner Summary)

1. **Carl Craver** — Mechanisms have multiple ontological levels; theories at different levels complement rather than compete
2. **Peter Machamer** — Always specify what entities *do* (activities), not just what they are
3. **Lindley Darden** — Mark knowledge gaps explicitly; mechanisms are typically incomplete schemas under construction
4. **Paul Thagard** — Use ECHO-style coherence scoring to rank underdetermined theories (breadth + depth + background fit + simplicity)
5. **James Woodward** — True causal discrimination comes from intervention-targeted tests that reveal what would happen if we manipulate the system

---

## How Panelists Shaped Each Card

### Card 1: Neural Frameworks
**Panelists involved**: None specifically (minor update)

### Card 2: Theory Comparison ★★★ (Major revision)
**Craver**: Add mechanistic level column
**Machamer**: Add entity-activity pairs
**Darden**: Add empirical support citations
**Thagard**: Add coherence score with breakdown
**Woodward**: Add interventionist prediction column

### Card 3: Mechanism Chain ★★★ (Major revision)
**Craver**: Multi-level pyramid (behavioral → circuit → synaptic → molecular)
**Machamer**: Specify activities connecting entities
**Darden**: Color-code by empirical support (green/yellow/red/gray); mark how-possibly vs. how-actually
**Thagard**: None directly (architecture is neutral to coherence scoring)
**Woodward**: Add interventionist properties (what breaks the mechanism?)

### Card 4: Critical Test ★★★ (Major revision)
**Craver**: Mark mechanistic level each test targets
**Machamer**: Specify what activities the test interrogates
**Darden**: Discrimination index (does outcome cleanly favor one theory?)
**Thagard**: Coherence impact (how much would test outcome change theory landscape?)
**Woodward**: Emphasize interventionist targeting; specify exact causal variable being tested

### Card 5: Warrant Structure
**Status**: ✓ No changes (epistemologically sound as-is)

### Card 6: Underdetermination Alert
**Craver**: Note when theories operate at different levels
**Machamer**: Distinguish between activity differences vs. entity differences
**Darden**: Show resolution pathway; give timeline
**Thagard**: Coherence comparison (which theory currently favored?)
**Woodward**: Mark interventionist divergence (do they make opposite predictions?)

---

## Success Checklist

After implementing all 4 documents:

- [ ] Design team has read Implementation Guide
- [ ] Development team understands 5 panelist perspectives (Quick Reference)
- [ ] Stakeholders approved 5 key design decisions (Handoff doc)
- [ ] Resources committed (dev team, content experts, domain specialists)
- [ ] Timeline realistic for available capacity (10–12 weeks)
- [ ] Content population strategy defined (which phenomena first?)
- [ ] Decision points scheduled (coherence formula sign-off, etc.)

---

## Key Files by Audience

| Audience | Primary Doc | Secondary Docs |
|----------|-------------|-----------------|
| **Executive/Stakeholder** | Handoff | Executive Summary of Panel Report |
| **Development Lead** | Implementation Guide | Quick Reference + Handoff |
| **Frontend Engineer** | Implementation Guide (code sections) | Quick Reference (checklists) |
| **Content Creator** | Quick Reference (checklists) | Panel Report (context on why) |
| **Domain Expert (scientist)** | Panel Report | Implementation Guide (data model) |
| **Product Manager** | Handoff | Implementation Guide (timeline) |
| **Philosophy/Epistemology Reviewer** | Panel Report | All others (validation) |

---

## Navigation Within Each Document

### EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03.md
```
Executive Summary
├─ Key Findings (3 critical gaps)
├─ Consensus Recommendations
└─ Priority

The Proposed Design
├─ 6-card system overview
├─ Governing question
└─ Risk assessment per card

Individual Panelist Positions (5 sections)
├─ Carl Craver
│  ├─ Position on mechanism representation
│  ├─ Position on theory comparison
│  ├─ Position on critical tests
│  ├─ Critique of proposal
│  └─ Constructive recommendations
├─ Peter Machamer
├─ Lindley Darden
├─ Paul Thagard
└─ James Woodward

Panel Consensus
├─ Strong Agreements (5 items)
├─ Productive Disagreements (tension table)
└─ Specific Tensions (3 with panel resolutions)

Recommended Integrated Design
├─ Card 1: Neural Frameworks (Updated)
├─ Card 2: Theory Comparison (REVISED) ← Most detailed
├─ Card 3: Mechanism Chain (REVISED) ← Most detailed
├─ Card 4: Critical Test (REVISED) ← Most detailed
├─ Card 5: Warrant Structure (Retained)
├─ Card 6: Underdetermination Alert (REVISED)
└─ New Supporting Pages

Operational Guidelines
├─ Coherence Scoring (formula + explanation)
├─ Mechanistic Level Specification (definitions)
├─ Interventionist Targeting (what makes a test "critical"?)
├─ Schema-Gap Notation (color-coding scheme)
└─ Discrimination Index Calculation (formula)

References
```

### IMPLEMENTATION_GUIDE_THEORY_EXPLORER_2026-04-03.md
```
Quick Reference Table
├─ Changes per card
├─ Effort estimates
└─ Timeline

Card 0: Neural Frameworks (Minor Update)
├─ Current state
├─ Proposed changes
├─ New data model
├─ UI template
└─ Effort: Low

Card 1: Theory Comparison (Major Revision)
├─ Current state (problematic)
├─ Proposed design (detailed layout)
├─ Data model (JSON schema)
├─ Frontend components (React templates)
└─ Effort: High

Card 2: Mechanism Chain (Major Revision)
├─ Current state (problematic)
├─ Proposed design (pyramid visualization)
├─ Data model
├─ Frontend components
└─ Effort: High

Card 3: Critical Test (Major Revision)
├─ Current state (underspecified)
├─ Proposed design (theory-targeted tests)
├─ Data model
├─ Frontend components
└─ Effort: Very High

Cards 4 & 5 (Minor/No Changes)

Overall Timeline
├─ Phase 1: Foundation (weeks 1–2)
├─ Phase 2: Core Cards (weeks 3–8)
├─ Phase 3: Advanced Cards (weeks 9–12)
└─ Phase 4: Content and Launch (weeks 12+)

Success Metrics
├─ Usability
├─ Epistemic Quality
└─ Content Completeness

Risk Mitigation (4 risks)

Next Steps
└─ Design Review, Data Infrastructure, Component Dev, Content Population, User Testing
```

### PANEL_SUMMARY_QUICK_REFERENCE_2026-04-03.md
```
The Five Panelists and Their Core Insights (1-paragraph each)
├─ Carl Craver
├─ Peter Machamer
├─ Lindley Darden
├─ Paul Thagard
└─ James Woodward

What Each Card Should Show (visual table)

Three Key Principles (All Panelists Agree)
├─ Principle 1: Mechanisms Have Multiple Levels
├─ Principle 2: Underdetermination is Temporary
└─ Principle 3: Transparency About Gaps

What the Panel Accomplished (tensions resolved)

Implementation Priority (phase table)

For Content Creators: The Checklist
├─ Mechanism description checklist
├─ Theory comparison checklist
└─ Critical test checklist

Key References (5 books + articles)

Questions to Ask During Implementation (Craver → Woodward)

Success Looks Like (6 user quotes)
```

### PANEL_TO_DEVELOPMENT_HANDOFF_2026-04-03.md
```
What Was Done (3 documents + 1 summary)

What Changed From Original Proposal
├─ Original design (6 cards)
├─ Issues identified
├─ Panel additions to each card
└─ Summary of enhancements

Key Design Decisions From Panel (5 decisions)
├─ Decision 1: Multi-Level Mechanism Representation
├─ Decision 2: Coherence-Based Theory Ranking
├─ Decision 3: Interventionist Testing for Discrimination
├─ Decision 4: Explicit Schema Gaps
└─ Decision 5: Activities, Not Just Entities

Effort & Timeline Breakdown (4 phases)
├─ Phase 1: Foundation (weeks 1–2)
├─ Phase 2: Core Cards (weeks 3–8)
├─ Phase 3: Advanced Cards (weeks 9–12)
└─ Phase 4: Content & Launch (weeks 12+)

Resource Requirements
├─ Development team (4 roles)
├─ Content & domain experts (3 roles)
└─ Timeline

What Stays the Same

What's New
├─ Data Models
├─ UI Components
└─ Backend Calculations

Decision Points Before Development (5 decisions)
├─ 1. Coherence Formula Sign-Off
├─ 2. Schema-Gap Color Scheme
├─ 3. Content Population Strategy
├─ 4. Critical Test Sourcing
└─ 5. Supporting Pages Priority

Risk Register (5 risks with P/I/M)

Success Criteria (Phase 1–3 Completion)
├─ Code Quality
├─ Content Quality
└─ User Research

Documentation Deliverables

Next Steps (Immediate, Week 0)
├─ Decision Checkpoint
├─ Design Kickoff
├─ Governance Setup
└─ Content Preparation

Open Questions For Panel (5 questions)

Status & Timeline
```

---

## Critical Dates & Milestones

| Date | Event |
|------|-------|
| 2026-04-03 | Panel report + 3 companion docs delivered; committed to repo |
| 2026-04-04 | **GO/NO-GO DECISION** on design direction + resource commitment |
| 2026-04-07–11 (Week 1) | Phase 1 begins (foundation, component design) |
| 2026-04-21–05-02 (Weeks 3–8) | Phase 2 (theory comparison + mechanism chain cards) |
| 2026-05-05–23 (Weeks 9–12) | Phase 3 (critical test card, underdetermination alert) |
| 2026-05-26+ (Week 12+) | Phase 4 (content population, QA, soft launch) |

---

## Contact & Escalation

**For questions about:**
- **Panel positions & philosophy**: See EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03.md
- **Implementation specs & code**: See IMPLEMENTATION_GUIDE_THEORY_EXPLORER_2026-04-03.md
- **Quick overview & checklists**: See PANEL_SUMMARY_QUICK_REFERENCE_2026-04-03.md
- **Go/no-go decisions & timeline**: See PANEL_TO_DEVELOPMENT_HANDOFF_2026-04-03.md
- **This index**: You're reading it

**Escalation path**: David Kirsh → (depends on question type) → Relevant panelist or development lead

---

## Document Metadata

| Document | Lines | Words | Created | Status |
|----------|-------|-------|---------|--------|
| EXPERT_PANEL_THEORY_EXPLORER_DESIGN_2026-04-03 | ~820 | ~8,000 | 2026-04-03 11:00 | FINAL |
| IMPLEMENTATION_GUIDE_THEORY_EXPLORER_2026-04-03 | ~650 | ~6,500 | 2026-04-03 11:02 | FINAL |
| PANEL_SUMMARY_QUICK_REFERENCE_2026-04-03 | ~310 | ~1,500 | 2026-04-03 11:03 | FINAL |
| PANEL_TO_DEVELOPMENT_HANDOFF_2026-04-03 | ~520 | ~3,500 | 2026-04-03 11:04 | FINAL |
| **TOTAL** | **~2,300** | **~19,500** | **2026-04-03** | **COMPLETE** |

All documents are committed to `/sessions/keen-busy-turing/mnt/REPOS/Knowledge_Atlas/docs/` and accessible via git.

---

**Navigation**: Use this index to find what you need. Start with the "Quick Start" section above and work from there.

**Status**: READY FOR REVIEW — All documents in place, committed, and linked.
