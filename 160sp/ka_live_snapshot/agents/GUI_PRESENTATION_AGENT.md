# K-ATLAS GUI Presentation Agent

**Date**: 2026-03-29
**Status**: New — not yet run. Requires template designs before first full run (see § Template Status below).
**Purpose**: Takes the GUI Agent v3 26-item page spec + Science-Writing Agent copy pack and produces a runnable Streamlit mockup for each K-ATLAS page.
**Framework**: Streamlit (Python 3.11+)

---

## Why this agent exists

The GUI Agent v3 and Science-Writing Agent together produce high-quality behavioral specs and copy. But specifications are not interfaces. A designer, a student doing a usability critique, or an expert panel reviewer cannot meaningfully evaluate a text spec — they need to see and interact with something. This agent closes that gap by producing **runnable Streamlit mockups**: single-file Python scripts that render each K-ATLAS page with real copy in place, realistic component structure, and correct interaction patterns, even before any backend data is wired up.

The mockups serve three purposes:
1. **Expert panel review** — Track 4 students in D3 give the panel a working mockup, not a text spec
2. **Usability testing** — COGS 160 students and recruited participants can interact with a real UI
3. **Developer handoff** — The mockup is the starting template for production implementation

---

## What this agent produces

For each page: a single self-contained Python file `pages/[page_name]_mockup.py` that:

- Renders the correct Streamlit layout (sidebar, columns, tabs, expanders)
- Shows real copy from the science copy pack (not Lorem ipsum)
- Populates data with realistic synthetic examples (not empty placeholders)
- Wires up the primary interactions using `st.session_state`
- Applies the K-ATLAS visual template (see § Visual Template below)
- Includes a clearly labeled `# MOCK DATA` section showing what real data would replace
- Can be run standalone: `streamlit run pages/ask_mockup.py`

---

## Visual template

### Color palette

| Role | Hex | Usage |
|------|-----|-------|
| Primary blue | `#2E6E9E` | Headers, primary buttons, active tabs |
| Light blue background | `#EAF3FB` | Info callouts, persona cards |
| Deep navy | `#1F497D` | Page titles, strong emphasis |
| Amber | `#FFF3CD` | Warnings, uncertain evidence |
| Light green | `#D4EDDA` | Strong evidence, success states |
| Light red | `#F8D7DA` | Error states, contested claims |
| Cyan light | `#E0FFFF` | Info strips, tooltips |
| Mid gray | `#888888` | Footer text, secondary labels |
| Near-white | `#F9F9F9` | Page background |
| White | `#FFFFFF` | Card backgrounds |

### Typography

Applied via `st.markdown` with custom CSS injected once per page:

```python
st.markdown("""
<style>
    .main { background-color: #F9F9F9; }
    h1 { color: #1F497D; font-family: Arial, sans-serif; }
    h2 { color: #2E6E9E; font-family: Arial, sans-serif; }
    h3 { color: #2E6E9E; font-family: Arial, sans-serif; }
    .stTabs [data-baseweb="tab"] { color: #2E6E9E; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #2E6E9E; }
    .evidence-row { border-left: 3px solid #2E6E9E; padding-left: 10px; margin-bottom: 8px; }
    .uncertainty-strong { background: #D4EDDA; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; }
    .uncertainty-mixed { background: #FFF3CD; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; }
    .uncertainty-weak { background: #F8D7DA; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; }
    .provenance-strip { background: #EAF3FB; border-left: 3px solid #2E6E9E; padding: 8px 12px; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)
```

### Standard page scaffold

Every page mockup starts with this scaffold:

```python
import streamlit as st

# ── Page config ────────────────────────────────────────
st.set_page_config(
    page_title="K-ATLAS | [Page Name]",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS injection ──────────────────────────────────────
# [Insert palette CSS above]

# ── Session state defaults ─────────────────────────────
if "persona" not in st.session_state:
    st.session_state.persona = "researcher"
if "compare_tray" not in st.session_state:
    st.session_state.compare_tray = []
# [Add any page-specific session state]

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.image("assets/ka_logo.png", width=120)  # or st.title("K-ATLAS") if no logo
    st.divider()
    st.session_state.persona = st.radio(
        "Viewing as:",
        ["researcher", "student", "practitioner", "developer"],
        format_func=lambda x: {
            "researcher": "🔬 Researcher / PI",
            "student": "📚 Student Researcher",
            "practitioner": "🏗️ Practitioner",
            "developer": "⚙️ KA Developer"
        }[x]
    )
    st.divider()
    # [Navigation links]

# ── Main content ───────────────────────────────────────
st.title("[Page Title]")
st.caption("[One-sentence purpose line from science copy pack]")
# [Page-specific content]
```

### Uncertainty strip component

```python
def uncertainty_strip(level: str, text: str):
    """level: 'strong' | 'mixed' | 'weak' | 'theoretical'"""
    colors = {
        "strong": ("#D4EDDA", "✅ Strong support"),
        "mixed": ("#FFF3CD", "⚠️ Mixed evidence"),
        "weak": ("#F8D7DA", "⚡ Limited evidence"),
        "theoretical": ("#E0FFFF", "🔵 Theory-linked inference")
    }
    bg, label = colors.get(level, ("#F9F9F9", "Unknown"))
    st.markdown(
        f'<div style="background:{bg}; padding:6px 12px; border-radius:4px; '
        f'font-size:0.85em; margin:4px 0"><strong>{label}</strong> — {text}</div>',
        unsafe_allow_html=True
    )
```

### Provenance expander component

```python
def provenance_expander(study_ref: str, quote: str, method: str, caveats: str = ""):
    with st.expander(f"📎 Source: {study_ref}", expanded=False):
        st.markdown(f'<div class="provenance-strip">"{quote}"</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"**Method**: {method}")
        with col2:
            if caveats:
                st.caption(f"**Caveats**: {caveats}")
```

---

## Template status

**Not yet finalized.** The color palette above is a first proposal based on the document color system used throughout the project. Before the first production run of this agent, David should confirm or revise:

1. Color palette — are these the right colors for KA's public-facing interface?
2. Logo / brand mark — is there a KA logo file? Where is it?
3. Typography — Arial acceptable, or a different font preferred?
4. Navigation structure — sidebar nav vs. top nav vs. page menu?
5. Density default — is `layout="wide"` the right default, or should some pages use centered?

Once confirmed, update the § Visual Template section and mark status as **Finalized**.

---

## Inputs required

1. **GUI Agent v3 output** for the target page (`docs/GUI_AGENT_V2_OUTPUT_[PAGENAME]_[DATE].md`)
2. **Science copy pack** for the target page (`docs/ATLAS_SCIENCE_COPY_PACK_[PAGENAME]_[DATE].md`)
3. **Visual template** (this document, confirmed)
4. **Mock data spec** — realistic synthetic data for this page (see below)

---

## Mock data approach

Every mockup uses synthetic data that is realistic in structure, content, and variability — not placeholder text. For example:

- Evidence page: a `pd.DataFrame` of 15–20 synthetic evidence rows with real-looking study refs, effect sizes, populations, and confidence levels
- Ask page: a realistic answer to a sample question ("Does natural light improve cognitive performance?") with 3 supporting evidence nodes, 1 conflicting finding, and an uncertainty strip
- Research Gaps page: 5–8 specific gap cards with VOI scores, gap types, and suggested study designs

The agent should generate mock data that teaches the reader what real data looks like, not just proves the layout renders.

---

## Prompt to run this agent

```
You are the K-ATLAS GUI Presentation Agent.

Your job is to produce a runnable Streamlit mockup for a K-ATLAS page.

Read these files first:
- /Users/davidusa/REPOS/Knowledge_Atlas/agents/GUI_PRESENTATION_AGENT.md  (this spec)
- /Users/davidusa/REPOS/Knowledge_Atlas/agents/GUI_AGENT_V3.md  (behavioral rules)
- [GUI Agent v3 output for this page]
- [Science copy pack for this page]

Your task is to produce a single-file Streamlit mockup for: [SPECIFY PAGE]

Requirements:
1. Apply the visual template CSS from this spec exactly
2. Use the standard page scaffold from this spec
3. Use the standard uncertainty_strip() and provenance_expander() components from this spec
4. Populate with realistic synthetic mock data — not Lorem ipsum, not empty placeholders
5. Wire primary interactions with st.session_state
6. Include a clearly labeled # MOCK DATA section
7. The file must be runnable standalone: streamlit run [filename]
8. Note any features that require custom Streamlit components explicitly as # CUSTOM COMPONENT NEEDED comments

Output to: /Users/davidusa/REPOS/Knowledge_Atlas/pages/[pagename]_mockup.py

After writing the file, verify it parses without errors:
    python3 -c "import ast; ast.parse(open('pages/[pagename]_mockup.py').read()); print('OK')"
```

---

## Run sequence

This agent runs third in the GUI pipeline:

1. Science-Writing Agent → copy pack
2. GUI Agent v3 → 26-item interaction spec
3. **This agent** → runnable Streamlit mockup
4. Expert panel or usability test → critique
5. GUI Agent v3 → revised spec based on critique
6. This agent → revised mockup
7. Developer → production implementation

---

## Pages to build (priority order)

| Priority | Page | Why |
|----------|------|-----|
| 1 | Ask | Core user entry point; most personas start here |
| 2 | Research Gaps + Experiment Maker | Fall course critical path; Track 4 needs it for D5 |
| 3 | Evidence | Dense analytic page; hardest to get right |
| 4 | Home | Orientation and routing; sets first impression |
| 5 | Neuroscience Perspective | Epistemic-transparency challenge; Norman critique applies |
| 6 | Author Mode | Expert-dense workspace; Munzner Task→Data→View applies |
| 7 | Practitioner Workspace | Actionability surface; Dill primary-action rule applies |
| 8 | COGS 160 Student Mode | Scaffolded learning mode; Zhuo progressive-disclosure rule |
