# AI Context: GUI Evaluation (Track 4)

## What is K-ATLAS?

K-ATLAS (Knowledge Architecture for Translating Life-science and Affective-environment Science) is a structured credibility reasoning system that stores scientific knowledge as *structured credences* — beliefs tagged with how well-supported they are, where the support comes from, and why the system holds each belief with particular confidence. Unlike a conventional database, K-ATLAS explicitly models the warrant structure: the chain of reasoning from evidence to claims, with formal discount factors controlling how much credence flows across different types of evidence.

The system's knowledge is organized as an Evidence Network (Web of Belief) where nodes are claims and edges are typed, weighted warrants. This network is visualized and navigated through a multi-page web interface consisting of topic overviews, evidence cards, gap analyses, and contribution workflows. The interface must make this complex epistemic structure transparent and navigable to users with different expertise levels and different goals.

## Current Site Structure

### K-ATLAS Root Pages
- **Home** (`ka_home.html`): Navigation hub
- **Explore/Topics** (`ka_topics.html`): Browse psychological constructs and environmental variables organized by domain (Lighting, Biophilia, Acoustics, Spatial Geometry, Color, Thermal Comfort, etc.)
- **Evidence** (`ka_evidence.html`): Evidence cards for specific constructs, showing warrant type, credence level, supporting and undercutting papers
- **Warrants** (`ka_warrants.html`): Formal warrant structure (backing, warrant, claim, rebuttal)
- **Argumentation** (`ka_argumentation.html`): Detailed reasoning for a specific claim
- **Gaps** (`ka_gaps.html`): Research gaps ranked by Value of Information
- **Articles** (`ka_article_search.html`): Searchable paper corpus with relevance to ATLAS claims
- **Demo** (`ka_demo.html`): Guided example
- **Contribute → Article Propose** (`ka_article_propose.html`): Submission form for new papers

### COGS 160 Pages (160sp/)
- **Schedule** (`ka_schedule.html`): Course timeline and week agenda
- **Week 1–3 Agendas** (`week1_agenda.html`, etc.): Task descriptions and workflows
- **Thursday Tasks** (`ka_thursday_tasks.html`): Seven exploratory tasks
- **Track Signup** (`ka_track_signup.html`): Self-assignment to tracks
- **Track Assignments** (`ka_tag_assignment.html`, `ka_article_finder_assignment.html`, `ka_vr_assignment.html`, `ka_gui_assignment.html`): Detailed task specifications
- **Dashboard** (`ka_dashboard.html`): Personal progress hub
- **Collect Articles** (`ka_collect_articles.html`): Workflow for article corpus building
- **Google Search Guide** (`ka_google_search_guide.html`): How to find papers

### Data Payloads (JSON, not visible but transmitted)
- Evidence records with claim text, credence, warrant type, supporting papers
- Article metadata and full-text indices
- Topic hierarchies and construct definitions
- Gap analyses with VOI scores

## The Six User Modes

K-ATLAS serves six distinct user personas with different goals and mental models:

| Mode | User Type | Primary Goal | Key Pages |
|------|-----------|--------------|-----------|
| **student_explorer** | Undergrad, no prior background | Understand one neuroarchitecture topic; find a research interest | Explore (Topics), Evidence, Gaps, Hypothesis Builder |
| **researcher** | PhD student, postdoc, faculty | Answer a specific research question; find gaps; assess generalizability | Evidence, Argumentation, Articles, Gaps, Hypothesis Builder |
| **contributor** | Anyone proposing new papers | Add papers to the corpus; understand relevance criteria | Articles, Article Propose, Gaps, Evidence |
| **instructor** | Course instructor (COGS 160) | Assign tasks, track student progress, surface gaps for assignments | Dashboard, Schedule, Track Assignments, Week Agendas |
| **practitioner** | Architect, designer, developer | Extract design recommendations; assess evidence strength | Explore, Evidence, Gaps, Hypothesis Builder |
| **theory_mechanism_explorer** | Epistemologist, methodologist | Understand warrant structure; assess credence calibration; critique methodology | Argumentation, Warrants, Evidence, Gaps |

Each mode has different information needs, different interaction patterns, and different tolerance for ambiguity.

## What Usability Evaluation Means in This Context

Usability evaluation is NOT about aesthetic judgment ("the site looks nice") or best practices compliance ("we follow WCAG 2.1"). It is about **task success**: Can a target user, given their mode and their goal, accomplish what they are trying to do using the interface?

### The Core Question
For a specific user mode and a specific task:
1. Does the interface present the information the user needs in the right order?
2. Are navigation paths clear and consistent?
3. Where do users get stuck, confused, or abandon the task?
4. What would reduce friction?

### Examples of Usability Problems (Not Aesthetic Issues)

**Problem 1: Mode Ambiguity**
- A student explorer visits Evidence page looking for "what's strong evidence for a claim?"
- Evidence cards show credence 0.68, warrant type "EMPIRICAL_ASSOCIATION", but do not explain what that means
- Student has to navigate away to Warrants page to understand, then come back
- **Friction point**: Definition is not inline; requires context-switching

**Problem 2: Navigation Consistency**
- User mode is set in the sidebar on Schedule page
- User mode is set in a dropdown on Dashboard page
- User mode is set in localStorage without any UI indicator on Home page
- Same user sees different information on the same page depending on which entry point they used
- **Friction point**: Three different identity mechanisms; no shared state; user gets lost

**Problem 3: Search-to-Answer Gap**
- Practitioner wants to know: "What colors improve well-being?"
- Articles search page has keyword box
- Practitioner types "color well-being"
- Returns 47 results, many on color blindness, color processing disorders, not design color
- No way to filter by evidence relevance or credence
- **Friction point**: Search returns many false positives; no ranking by K-ATLAS relevance

**Problem 4: Boundary Condition Invisibility**
- Researcher looks at evidence for "nature contact reduces cortisol"
- Credence is high (0.78)
- Interface does not surface that evidence is 80% WEIRD populations
- Researcher recommends design for non-Western urban setting
- **Friction point**: Generalization limits are not prominent; evidence appears universal

## Current Known UI Problems

1. **Mode-switching inconsistency**: Three different identity storage mechanisms (localStorage, URL parameter, sidebar state) with no synchronization. User sees different personalization depending on entry point.

2. **Warrant type opacity**: Warrant types (CONSTITUTIVE, MECHANISM, EMPIRICAL_ASSOCIATION, FUNCTIONAL, CAPACITY, ANALOGICAL, THEORY-DERIVED) are shown on evidence cards but not explained inline. Users must navigate to a reference page to understand what "FUNCTIONAL" means.

3. **Population generalization invisibility**: BOUNDARY gaps that flag population limitations are on a separate "Gaps" page, not integrated into evidence cards themselves. A high-credence claim appears universal without explicit caveat.

4. **Slow search-to-evidence workflow**: Finding relevant papers via Articles search and then navigating to their evidence is cumbersome. No direct link from "this paper supports this evidence item" within the articles view.

5. **Shallow construct hierarchy**: Topics page shows top-level constructs (Lighting, Biophilia) but not the fine-grained decomposition needed for design specification. Practitioners need to jump to Evidence to see sub-constructs.

6. **No hypothesis-to-experiment bridge**: Hypothesis Builder suggests research questions but does not link them back to ATLAS claims. User cannot trace "I want to test this" back to "here is the gap in ATLAS that matters."

## Data Model for Evaluation Records

Each usability evaluation must capture:

- **page_url**: Full URL of the page being tested (e.g., `ka_evidence.html?claim_id=cortisol_biophilia_01`)
- **user_mode**: The user mode operating under (student_explorer, researcher, contributor, instructor, practitioner, theory_mechanism_explorer)
- **task_attempted**: Free-text description of what the user tried to do (e.g., "Find the effect size for biophilic density on cortisol")
- **success**: Boolean or 3-valued (Success, Partial, Failure)
- **time_to_complete**: Seconds to complete task (or seconds until abandonment)
- **friction_points**: List of specific points where the user slowed down, got confused, or went off-path
  - Example: `["warrant type 'FUNCTIONAL' undefined", "navigation back from Articles page requires page reload", "no clear link from paper to supporting evidence"]`
- **suggested_fix**: Concrete, specific redesign or added UI element that would reduce friction
  - Example: `"Add inline tooltip to warrant types on evidence card (appears on hover, explains d value and interpretation)"`
- **tester_id**: Who conducted the evaluation
- **timestamp**: When evaluation was performed
- **notes**: Additional context (e.g., "tester is design student, not computer scientist; struggled with epistemological language")

## Acceptance Criteria for Evaluation Submissions

1. **Cover all primary user flows for the assigned mode**: Do not evaluate one page in isolation. For practitioner mode, the flow is typically: Home → Explore → Evidence → Gaps → Hypothesis Builder. Evaluation should cover friction across this flow.

2. **Friction points must be reproducible**: "The interface feels confusing" is not a friction point. "When a user clicks the 'Warrant' link from an evidence card, they are taken to a new page with no breadcrumb navigation back, requiring manual URL editing or use of browser back button" is reproducible.

3. **Suggested fixes must be specific, not vague**:
   - ✗ "Make the interface more intuitive"
   - ✓ "Add a dropdown menu to the Evidence card header that filters by warrant type; show the d value and interpretation next to each type"

4. **Evaluation must test with actual target users or detailed task simulation**: Do not guess about what a practitioner needs. Either test with an architect/designer, or document your assumptions about their mental model clearly.

5. **Success criteria must be explicit**: Before testing, state what "success" means for the task. Example: "User can, without extraneous clicking, find the top three evidence items supporting 'biophilic exposure improves focus', note their credence scores, and identify one paper that supports each evidence item."

6. **All evaluations must cover at least one friction point from the known UI problems list** (mode inconsistency, warrant opacity, population invisibility, search slowness, shallow hierarchy, or hypothesis-to-gap bridging) or identify a new, specific problem.

## Key References

- **UI Layout and Navigation**: Examine all pages at `ka_*.html` in the root and `/160sp/` directory
- **Evidence Structure**: `ka_evidence.html` (current implementation of evidence cards)
- **Mode Definition**: Check localStorage and URL parameters in each page's `<script>` section
- **Warrant Definitions**: `ka_warrants.html` (reference page; should be accessible from evidence cards)
- **Task Specifications**: `ka_thursday_tasks.html` and individual track assignments for user persona details
