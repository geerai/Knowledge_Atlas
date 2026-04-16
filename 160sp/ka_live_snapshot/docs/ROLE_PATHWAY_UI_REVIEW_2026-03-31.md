# Role Pathway UI Review

## Recommended Role Pathways

The site already has the right underlying roles in `ka_workflows.js`: `student_explorer`, `contributor`, `theory_mechanism_explorer`, and `practitioner`. The UI should make each role feel like a distinct route, not just a filter on the same page.

- `Student Explorer`: lead with `First Questions`, then `Deep Dive`, then `Evidence Pipeline` if the student wants to move from orientation into collection. This role should feel exploratory first, with clear permission to stop after the first route if that is all the user needs.
- `Contributor`: lead with `Evidence Pipeline`, then `First Questions`, then `Deep Dive`. This role should feel operational first. The visual emphasis should be on submission, tagging, and getting work into the archive.
- `Theory Explorer`: lead with `Mechanism Trace`, then `Hypothesis Test`, then `Deep Dive`. This role should feel explanatory and adversarial in the scientific sense: what mechanism is claimed, what would count against it, and what alternative theory competes with it.
- `Practitioner`: lead with `Design Decision Support`, then `Client Evidence Brief`, then `Deep Dive`. This role should feel decision-oriented: the first question is not “what is true?” but “what is useful enough to act on with appropriate caution?”

The home page copy in `ka_home.html` already points in this direction. The pathway UI should make the ordering visible up front, and should not present all workflows as equally relevant to all users.

## Route-Aware Next / Back CTAs

The current workflow hub already has the right mechanical model: a sticky bottom bar, progress persistence, and a route state in the URL. The CTA design should make that state obvious.

- Use one primary CTA and one secondary CTA only. The primary button should always be the forward action, colored with the route accent. The secondary button should be a quiet outline button.
- Label the forward button by intent, not by generic motion. Early steps should say `Next: [next step title]`. The last step should say `Finish route` or `Complete route`, not `Next`.
- Label the back button by position, not by abstraction. Use `Back` or `Previous step`, and disable it on step 1.
- The CTA bar should remain sticky, but not dominant. It should read as guidance, not as a modal command.
- Step changes should preserve route state in the URL and local storage. If the user leaves the workflow, they should be able to return to the same step without reorientation.
- When a step opens another page, that page should inherit the route context and offer a return link back into the same workflow, not a reset to home.
- On mobile, the buttons should stack or compress cleanly, with the progress label still visible.

Visually, the current workflow hub is close to the right answer: use the route color for the primary action, keep the secondary action neutral, and let the progress indicator do the rest. The main improvement is semantic: the labels must tell the user where they are going.

## Two Mock Pathway Hub Pages

The two mock hub pages should be prototypes of route selection, not full workflow pages.

1. `Student Explorer` / `Contributor` hub
   - A role switcher between the two roles.
   - A short role statement that distinguishes exploration from contribution.
   - Two large pathway cards: `First Questions` and `Evidence Pipeline`.
   - A visible “resume where you left off” card.
   - A compact step preview for each workflow, showing only titles and page names.
   - A clear note that the user may browse freely, but the recommended order is the one shown.

2. `Theory Explorer` / `Practitioner` hub
   - A role switcher between mechanism-seeking and decision-making.
   - A shared route map showing where theory work connects to practical decision work.
   - Two primary pathway cards per role, with the theory route emphasising `Mechanism Trace` and `Hypothesis Test`, and the practitioner route emphasising `Design Decision Support` and `Client Evidence Brief`.
   - A small panel that explains the difference between “explain” and “apply” in plain language.
   - A route preview that shows which pages open next and which step concludes the route.
   - One example of a route-aware Next/Back control so the handoff into `ka_workflow_hub.html` is obvious.

The pages should be mock hubs, so they need to show selection, hierarchy, and return points, but not the full detail of the step-by-step workflow.
