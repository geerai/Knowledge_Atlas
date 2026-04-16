/**
 * ka_workflows.js  —  ATLAS Guided Workflow Definitions
 * -------------------------------------------------------
 * Central data store for all role-specific workflows shown on
 * ka_user_home.html (workflow cards) and ka_workflow_hub.html
 * (step-by-step detail page).
 *
 * Each workflow has:
 *   id           — kebab-case identifier
 *   title        — short display name
 *   subtitle     — one-line framing
 *   objective    — what the user will accomplish (displayed prominently)
 *   forRoles     — which user types see this workflow
 *   estimatedTime — rough effort estimate
 *   badge        — category label
 *   badgeColor   — hex colour for badge chip
 *   icon         — emoji icon
 *   steps[]      — ordered step objects (see schema below)
 *
 * Step schema:
 *   id           — string (s1, s2, …)
 *   title        — step name
 *   pageLink     — ATLAS page to navigate to for this step
 *   pageName     — display name for the page link
 *   description  — 2-4 sentence description of what to do
 *   lookFor[]    — 3-4 bullet points of what to notice
 *   imageType    — key into KA_WORKFLOW_IMAGES for illustration
 *   collectArticles — boolean: show article-collector affordance on this step
 */

window.KA_WORKFLOWS = {

  // ─── WORKFLOW DEFINITIONS ───────────────────────────────────────────────────

  workflows: {

    // ── Student / Contributor ──────────────────────────────────────────────

    'first-questions': {
      id: 'first-questions',
      title: 'First Questions',
      subtitle: 'Learn how to explore Atlas before you try to contribute to it',
      objective: 'Use the Did You Know findings, the topic hierarchy, and the question tools to understand what Atlas covers well, what it only tentatively classifies, and which questions are worth pursuing next.',
      forRoles: ['student_explorer', 'contributor'],
      estimatedTime: '35–50 min',
      badge: 'Onboarding',
      badgeColor: '#2A7868',
      icon: '🔍',
      steps: [
        {
          id: 's1',
          title: 'Start with Did You Know',
          pageLink: 'ka_home.html',
          pageName: 'Home',
          description: 'Begin on the Atlas home page and read several Did You Know cards. The point is not to memorise them but to learn the style of claim Atlas can surface: a concrete environmental factor, a human consequence, and a degree of epistemic caution.',
          lookFor: [
            'Which findings feel genuinely surprising rather than merely familiar?',
            'Which cards state a mechanism, and which merely state an effect?',
            'Which cards make you want to ask “why?” or “for whom?”'
          ],
          imageType: 'qa-interface',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Probe One Finding More Deeply',
          pageLink: 'ka_demo_v04.html',
          pageName: 'Ask ATLAS',
          description: 'Pick one finding from Step 1 and push on it in the Ask ATLAS interface. Ask what evidence supports it, what the likely mechanism is, and where the uncertainty still lies.',
          lookFor: [
            'Does Atlas distinguish between evidence, interpretation, and projection?',
            'What follow-up question would sharpen the original claim?',
            'Where does the system hedge, and does the hedging seem reasonable?'
          ],
          imageType: 'qa-interface',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'Open the Topic Hierarchy',
          pageLink: 'ka_topic_hierarchy.html',
          pageName: 'Topic Map',
          description: 'Move from single findings to the larger map. Use the defended and working views to see which parts of the corpus Atlas can classify confidently and which parts remain provisional.',
          lookFor: [
            'Which top-level environmental families recur across multiple human outcomes?',
            'Which topic neighborhoods have many nearby topics, and which stand alone?',
            'What changes when you expand from the defended map to the working map?'
          ],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Compare Topic Areas',
          pageLink: 'ka_topics.html',
          pageName: 'Topics',
          description: 'Use the Topics page to compare broad areas, research fronts, and open questions. This is where curiosity becomes a more disciplined sense of which domains are mature, emerging, or thinly evidenced.',
          lookFor: [
            'Which topics are mature enough to teach from immediately?',
            'Which topics are active but contested?',
            'Which topics would make a good first research question for a student?'
          ],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's5',
          title: 'Turn Curiosity into Searchable Questions',
          pageLink: 'ka_question_maker.html',
          pageName: 'Question Maker',
          description: 'Finish by turning one promising topic into a small set of sharper questions. This step prepares you either to stop, satisfied that you understand the territory better, or to move on into article finding and contribution work.',
          lookFor: [
            'Can you produce one broad question, one mechanism question, and one gap question?',
            'Do the questions sound like things a real researcher could investigate?',
            'Would you now know where to go next in Atlas if you wanted to contribute?'
          ],
          imageType: 'query-builder',
          collectArticles: false
        }
      ]
    },

    'evidence-pipeline': {
      id: 'evidence-pipeline',
      title: 'Evidence Pipeline',
      subtitle: 'From raw article to ATLAS-ready evidence claim',
      objective: 'Take one paper all the way from discovery to a tagged, quality-assessed evidence submission that another researcher can rely on.',
      forRoles: ['contributor', 'researcher'],
      estimatedTime: '60–90 min',
      badge: 'Contribution',
      badgeColor: '#1a56a4',
      icon: '🔬',
      steps: [
        {
          id: 's1',
          title: 'Find a High-Value Paper',
          pageLink: 'ka_article_search.html',
          pageName: 'Article Search',
          description: 'Identify an article that makes an explicit, testable empirical claim about how a physical environment affects human cognition, emotion, or behavior. High-value papers: (1) report effect sizes, (2) describe sample clearly, (3) use controlled or quasi-experimental designs, (4) are peer-reviewed.',
          lookFor: [
            'Does the abstract state a hypothesis and report whether it was supported?',
            'Is there a methods section with enough detail to assess internal validity?',
            'Does the paper measure a construct ATLAS already tracks (check Topics page)?',
            'Is it cited enough to suggest the field considers it credible?'
          ],
          imageType: 'article-search',
          collectArticles: true
        },
        {
          id: 's2',
          title: 'Evaluate Evidence Quality',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Apply the ATLAS quality rubric to your chosen paper. Assess study design, sample, measurement validity, effect size reporting, and replication status. A paper that fails multiple criteria should be noted but not submitted as strong evidence — it can be submitted with appropriate quality flags.',
          lookFor: [
            'What study design does the paper use? (RCT > quasi-experiment > correlation)',
            'How large is the sample? How representative of the target population?',
            'Are effect sizes reported with confidence intervals?',
            'Has the finding been replicated, or is this the only study?'
          ],
          imageType: 'evidence-card',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'Tag the Evidence Claim',
          pageLink: 'ka_tagger.html',
          pageName: 'Tagger',
          description: 'Identify the specific CNFA construct(s) measured in the paper and tag them. A well-tagged evidence claim links: the environmental IV (e.g., luminance_mean), the psychological DV (e.g., attention_capture), the direction of effect, and the population. Be precise — "office workers in open plans" is more useful than "people".',
          lookFor: [
            'Does the paper\'s IV map cleanly to a CNFA tag, or is it ambiguous?',
            'Is the DV a construct ATLAS currently tracks? If not, flag it as a gap.',
            'What moderators does the paper report? (Size, demographics, context?)',
            'How confident are you in your tag choices? Note any uncertainty.'
          ],
          imageType: 'tagger-ui',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Submit with Annotation',
          pageLink: 'ka_article_propose.html',
          pageName: 'Submit Articles',
          description: 'Submit the paper with your quality assessment and tag annotations. The submission annotation should be a single sentence of the form: "[Study] found that [IV manipulation] [increased/decreased] [DV] by [effect size] in [population] (p = [value])." This precision makes your submission immediately useful.',
          lookFor: [
            'Does your annotation capture the key causal claim?',
            'Is the effect size and direction included?',
            'Would a researcher reading only your annotation know what to look for in the full paper?'
          ],
          imageType: 'submit-form',
          collectArticles: true
        }
      ]
    },

    'deep-dive': {
      id: 'deep-dive',
      title: 'Evidence Deep Dive',
      subtitle: 'Trace one claim from assertion to literature support',
      objective: 'Take a single ATLAS answer and follow its evidence chain back to the literature — assessing confidence, gaps, and alternative interpretations.',
      forRoles: ['student_explorer', 'researcher', 'theory_mechanism_explorer'],
      estimatedTime: '30–45 min',
      badge: 'Analysis',
      badgeColor: '#5c3d8f',
      icon: '🕵️',
      steps: [
        {
          id: 's1',
          title: 'Get an ATLAS Answer',
          pageLink: 'ka_demo_v04.html',
          pageName: 'Ask ATLAS',
          description: 'Ask ATLAS a specific question about how a physical environment affects people. Choose something you have a genuine view on — it is easier to evaluate an answer when you have prior expectations. Note the answer and the confidence level ATLAS reports.',
          lookFor: [
            'Does ATLAS commit to a direction of effect, or hedge?',
            'What evidence does it cite?',
            'Does the answer match your prior expectation? If not, why not?'
          ],
          imageType: 'qa-interface',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Inspect the Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Navigate to the evidence cards supporting the answer you received. For each card, read the full citation and assess: How strong is this evidence on its own? Is the study design appropriate to the claim? Are there any red flags (very small n, no replication, industry-funded, etc.)?',
          lookFor: [
            'How many independent studies support the claim?',
            'Are they all from the same lab, or distributed across research groups?',
            'Do the effect sizes converge, or vary wildly across studies?',
            'Are there any studies with contradictory findings?'
          ],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Map the Argument',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'In the Argumentation view, examine how the evidence is assembled into an argument. Identify the warrant that connects evidence to claim. Ask: is this warrant explicit or implicit? Is it domain-specific or a general epistemic principle?',
          lookFor: [
            'Is the warrant clearly stated, or inferred?',
            'Could a plausible alternative warrant lead to a different conclusion?',
            'Are there defeaters (evidence that weakens the claim) visible in the view?'
          ],
          imageType: 'argument-graph',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Identify Gaps and Note Them',
          pageLink: 'ka_gaps.html',
          pageName: 'Gaps',
          description: 'Navigate to the Gaps page and check whether the gap you identified is already documented. If not, note it in your reflection document. A well-specified gap includes: what the claim is, what evidence is missing, what study design would fill it, and why it matters for architectural practice.',
          lookFor: [
            'Is the gap already in ATLAS, or genuinely new?',
            'Is it a sampling gap (right construct, wrong population) or a construct gap (construct not yet studied)?',
            'What would a study look like that filled this gap?'
          ],
          imageType: 'gap-view',
          collectArticles: true
        }
      ]
    },

    // ── Researcher ──────────────────────────────────────────────────────────

    'hypothesis-test': {
      id: 'hypothesis-test',
      title: 'Hypothesis Test',
      subtitle: 'Assess whether ATLAS supports or challenges a theoretical prediction',
      objective: 'State a testable prediction from a theory of your choice, then systematically evaluate what the ATLAS evidence base says about it — including contrary evidence.',
      forRoles: ['researcher', 'theory_mechanism_explorer'],
      estimatedTime: '60–90 min',
      badge: 'Research',
      badgeColor: '#8b1a2e',
      icon: '⚗️',
      steps: [
        {
          id: 's1',
          title: 'State the Hypothesis',
          pageLink: 'ka_hypothesis_builder.html',
          pageName: 'Hypothesis Builder',
          description: 'Before searching, commit to a specific, falsifiable prediction. Use the Hypothesis Builder to formalise it: IV, DV, direction, moderators, and the theoretical mechanism you expect. A good hypothesis is not "I think nature is good" but "exposure to a window view of vegetation will reduce physiological stress indicators (measured by cortisol or heart rate) more than a matched interior view, in white-collar workers under time pressure."',
          lookFor: [
            'Is your hypothesis specific enough to be falsified?',
            'Have you identified the mechanism, not just the correlation?',
            'What would count as disconfirming evidence?'
          ],
          imageType: 'hypothesis-form',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Search for Supporting Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Search the evidence base for studies that bear on your hypothesis. Collect studies that support it AND studies that challenge it. The quality of your analysis depends on including both.',
          lookFor: [
            'Are the supporting studies from high-quality designs (RCT, quasi-experimental)?',
            'Do they measure your specific DV, or a proxy?',
            'What moderators are reported? Are they consistent with your theoretical mechanism?'
          ],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Assess Contrary Evidence',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Equally important: actively search for studies that fail to support your hypothesis or point in the opposite direction. A hypothesis that ignores contrary evidence is confirmation-biased. Note: partial support (effect in one subgroup but not another) is evidence about moderators, not failure.',
          lookFor: [
            'Are the null results from adequately powered studies, or small and underpowered?',
            'Do the disconfirming studies measure the same construct, or a related but different one?',
            'Can the contrary evidence be explained by your theoretical mechanism (as a boundary condition)?'
          ],
          imageType: 'argument-graph',
          collectArticles: true
        },
        {
          id: 's4',
          title: 'Render a Verdict',
          pageLink: 'ka_interpretation.html',
          pageName: 'Interpretation',
          description: 'Using the Interpretation page, render a verdict: Does the evidence support, partially support, fail to support, or challenge your hypothesis? Express your confidence level and explain what additional evidence would change your assessment. This is the deliverable: a calibrated belief, not a binary yes/no.',
          lookFor: [
            'What is your all-things-considered credence in the hypothesis?',
            'What is the single piece of evidence that most changes your prior?',
            'What study would you design to resolve the remaining uncertainty?'
          ],
          imageType: 'interpretation-panel',
          collectArticles: false
        }
      ]
    },

    'lit-synthesis': {
      id: 'lit-synthesis',
      title: 'Literature Synthesis',
      subtitle: 'Map what is known, contested, and open in a domain',
      objective: 'Produce a calibrated map of the evidence landscape in one domain — distinguishing robust findings, contested claims, and genuine gaps — suitable for informing a design brief or research proposal.',
      forRoles: ['researcher'],
      estimatedTime: '90–120 min',
      badge: 'Synthesis',
      badgeColor: '#4a7c59',
      icon: '🗺️',
      steps: [
        {
          id: 's1',
          title: 'Define the Domain Boundaries',
          pageLink: 'ka_topics.html',
          pageName: 'Topics',
          description: 'Select the topic area and define its scope. Be explicit about what is inside and outside your review. A scoped synthesis ("effects of indoor plant exposure on office workers\' self-reported stress, 2000–2024") is more useful than an unscopable one ("nature and wellbeing").',
          lookFor: ['Which sub-topics are densely covered?', 'Which are sparse?', 'Are there adjacent topics that clearly bear on your domain?'],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Collect the Evidence Base',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Systematically collect all relevant evidence cards in your domain. Use the workspace basket to build your corpus. Aim for completeness over selectivity in this step — you will filter and assess in Step 3.',
          lookFor: ['Are there papers you expected to find but cannot locate in ATLAS?', 'Are all the study designs represented?', 'What is the temporal spread — are there recent replications?'],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Assess and Categorise',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Group your collected evidence into: (a) robust findings — consistent across multiple high-quality studies; (b) promising but thin — supported by 1-2 studies, awaiting replication; (c) contested — studies point in different directions; (d) gaps — expected findings that are absent. Quality of design matters as much as quantity.',
          lookFor: ['Which claims have the most consistent evidence?', 'Where do studies contradict each other — and why?', 'What would a meta-analyst conclude?'],
          imageType: 'argument-graph',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Annotate and Export',
          pageLink: 'ka_annotations.html',
          pageName: 'Annotations',
          description: 'Write a synthesis annotation for each category: a 2-3 sentence summary of what the evidence shows in this domain, with appropriate epistemic hedging. Robust findings get confident statements; contested claims get explicit uncertainty. These annotations are your deliverable.',
          lookFor: ['Is your language calibrated to the evidence strength?', 'Can a non-specialist read your annotations and understand the state of knowledge?'],
          imageType: 'annotation-view',
          collectArticles: false
        }
      ]
    },

    // ── Practitioner ────────────────────────────────────────────────────────

    'design-decision': {
      id: 'design-decision',
      title: 'Design Decision Support',
      subtitle: 'Move from an image or design idea to its likely human consequences',
      objective: 'Start from a concrete environmental example, inspect how Atlas would tag it, trace the likely cognitive, affective, and social consequences, and leave with a concise practice-facing note rather than a vague design intuition.',
      forRoles: ['practitioner'],
      estimatedTime: '30–45 min',
      badge: 'Practice',
      badgeColor: '#b05e1a',
      icon: '📐',
      steps: [
        {
          id: 's1',
          title: 'Inspect How an Image Is Tagged',
          pageLink: 'ka_tagger.html',
          pageName: 'Image Tagger',
          description: 'Begin with the image-tagging surface so you can see how a built environment is decomposed into meaningful features and likely constructs. This is the quickest way for a practitioner to understand what Atlas thinks it is seeing before it makes any broader claim.',
          lookFor: ['Which environmental features drive the proposed tags?', 'Which tags look plausible, and which feel over-extended?', 'What information is missing from the image alone?'],
          imageType: 'tagger-ui',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'See Likely Consequences',
          pageLink: 'ka_topics.html',
          pageName: 'Topics',
          description: 'Move from the tagged environmental features to the likely consequence families. Use the topic and front cards to see which cognitive, affective, and social outcomes Atlas most strongly associates with the kind of environment you are considering.',
          lookFor: ['Which consequence families recur: stress, comfort, navigation, preference, social response?', 'Which consequences are well established, and which are still frontier questions?', 'Do the topic cards suggest caution rather than confidence anywhere?'],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'Review the Evidence Behind the Consequences',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'Open the evidence layer to check what actually supports the consequence claims. A practitioner needs to know not only what Atlas suggests, but what sort of studies, populations, and measurements sit behind the suggestion.',
          lookFor: ['Are the claims supported by strong studies or only by thin evidence?', 'Do the populations resemble the setting you care about?', 'Which practical caveats would you need to mention to a client?'],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's4',
          title: 'Write the Practice Note',
          pageLink: 'ka_annotations.html',
          pageName: 'Annotations',
          description: 'Finish with one short practice note: what this environmental feature is likely to do, what the evidence behind that claim looks like, and what uncertainty remains. The aim is not to sound certain; it is to be action-guiding without becoming careless.',
          lookFor: ['Can a client read the note without specialist vocabulary?', 'Does the note separate what is likely from what is speculative?', 'Would this note help a real design decision rather than merely decorate it?'],
          imageType: 'annotation-view',
          collectArticles: false
        }
      ]
    },

    'client-brief': {
      id: 'client-brief',
      title: 'Client Evidence Brief',
      subtitle: 'Curate a compelling, evidence-backed design rationale',
      objective: 'Assemble a concise set of 5-8 evidence cards that justify specific design choices to a client — showing the scientific basis for decisions without overwhelming non-specialist readers.',
      forRoles: ['practitioner'],
      estimatedTime: '45–60 min',
      badge: 'Practice',
      badgeColor: '#b05e1a',
      icon: '📋',
      steps: [
        {
          id: 's1',
          title: 'Identify the Key Design Claims',
          pageLink: 'ka_topics.html',
          pageName: 'Topics',
          description: 'List the three to five most important design claims you want to substantiate for this client or project. These should be the claims most likely to be questioned ("why biophilic elements?", "why this ceiling height?", "why this acoustic treatment?"). Start from your design rationale, not from ATLAS.',
          lookFor: ['Which of your design choices is most novel or counterintuitive to the client?', 'Which choices are most expensive — those need the strongest justification?'],
          imageType: 'topic-browser',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Find the Evidence',
          pageLink: 'ka_evidence.html',
          pageName: 'Evidence',
          description: 'For each design claim, find the one or two best-supported pieces of evidence in the ATLAS archive. "Best-supported" means: clear methodology, appropriate population, replicated if possible, and effect size large enough to be practically significant. Save these into the workspace basket.',
          lookFor: ['Is there a single landmark study that the field widely cites?', 'Are there recent meta-analyses or systematic reviews — those are most authoritative?', 'Are any of the key authors prominent enough that naming them strengthens the brief?'],
          imageType: 'evidence-card',
          collectArticles: true
        },
        {
          id: 's3',
          title: 'Write Plain-Language Summaries',
          pageLink: 'ka_annotations.html',
          pageName: 'Annotations',
          description: 'For each evidence piece, write a plain-language summary (2-3 sentences, no jargon) that a client can read without a research background. Then add a brief note on what the evidence does NOT tell you — every honest brief acknowledges limits. This honesty builds trust.',
          lookFor: ['Can someone without a research background understand your summary?', 'Have you translated the effect size into practical terms ("roughly a 15% improvement in task focus")?', 'Have you been explicit about what the evidence cannot prove?'],
          imageType: 'annotation-view',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Review for Overreach',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Before finalising: read your brief as a sceptical client would. Identify any claim that overstates the evidence. Overreach damages credibility more than honest hedging does. The strongest brief is the one that accurately represents both what is known and what is uncertain.',
          lookFor: ['Does any claim say "proves" when it should say "suggests"?', 'Are there alternative interpretations of the evidence that you have not acknowledged?', 'Have you cited the evidence, not just asserted the claim?'],
          imageType: 'argument-graph',
          collectArticles: false
        }
      ]
    },

    // ── Instructor ──────────────────────────────────────────────────────────

    'student-onboarding': {
      id: 'student-onboarding',
      title: 'Student Onboarding',
      subtitle: 'Approve registrations and assign tracks + research questions',
      objective: 'Move all pending student registrations through to fully approved status — with track assignments, research question assignments, and confirmation that students know their next steps.',
      forRoles: ['instructor'],
      estimatedTime: '20–40 min',
      badge: 'Admin',
      badgeColor: '#2A5FA0',
      icon: '🎓',
      steps: [
        {
          id: 's1',
          title: 'Review Pending Registrations',
          pageLink: '160sp/ka_approve.html',
          pageName: 'Approve Students',
          description: 'Open the approval queue. For each pending student, review their track preference and skills statement. A student who has chosen a track that does not match their stated skills is a mismatch to flag — they should be redirected before, not after, they have spent a week on the wrong track.',
          lookFor: ['Which tracks are oversubscribed? Which need more students?', 'Are skills statements specific (good) or generic ("I know programming")?', 'Any students who have not submitted a skills statement at all?'],
          imageType: 'admin-queue',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Balance Track Assignments',
          pageLink: '160sp/ka_approve.html',
          pageName: 'Approve Students',
          description: 'Assign each student to a track, balancing across the four tracks where possible. If a student\'s preference is reasonable, honour it. If the track is full, redirect to their second choice and note the reason. The target is 4-6 students per track for a class of 20.',
          lookFor: ['Are any tracks empty? That creates a problem for Phase 3 cross-audits.', 'Have you documented the rationale for any overrides?'],
          imageType: 'admin-queue',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'Assign Research Questions',
          pageLink: '160sp/ka_approve.html',
          pageName: 'Approve Students',
          description: 'Assign each student one of the eight research questions (Q01–Q08). Avoid giving students on the same track the same question — their track work will be more valuable if they are covering different evidence domains. If possible, match the research question to the student\'s stated topic interests.',
          lookFor: ['Are all 8 questions represented across your cohort?', 'Do any questions map particularly well to specific track work?'],
          imageType: 'admin-assign',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Confirm and Monitor',
          pageLink: '160sp/ka_dashboard.html',
          pageName: 'Dashboard',
          description: 'After approving all students, check the main dashboard to confirm the assignments are reflected in the system. Note any students who have not yet logged in after receiving their approval — they may need a follow-up email.',
          lookFor: ['Have all approved students logged in?', 'Are any students stuck on setup (no articles submitted after one week)?', 'Is the article submission rate roughly on track for the class?'],
          imageType: 'dashboard-view',
          collectArticles: false
        }
      ]
    },

    // ── Theory / Mechanism Explorer ──────────────────────────────────────────

    'mechanism-trace': {
      id: 'mechanism-trace',
      title: 'Mechanism Trace',
      subtitle: 'Trace a theory, its mechanism claims, and the experiment that would test them',
      objective: 'Move from rival theories to mechanism claims, then inspect how Atlas itself reasons about them and what critical experiment would genuinely distinguish the options.',
      forRoles: ['theory_mechanism_explorer', 'researcher'],
      estimatedTime: '60–90 min',
      badge: 'Theory',
      badgeColor: '#5c3d8f',
      icon: '🧠',
      steps: [
        {
          id: 's1',
          title: 'Compare Rival Theories',
          pageLink: 'Designing_Experiments/theory_and_experiment_design.html',
          pageName: 'Theory & Experiment Design',
          description: 'Begin with the theory page, not with an isolated result. The task is to understand which theoretical programmes are in play, what each predicts, and what would count as a meaningful discrimination between them.',
          lookFor: ['Which theories genuinely compete, and which merely use different language for the same idea?', 'What mechanism does each theory rely on?', 'What would each theory predict in the same built-environment case?'],
          imageType: 'hypothesis-form',
          collectArticles: false
        },
        {
          id: 's2',
          title: 'Trace Mechanism Claims',
          pageLink: 'ka_argumentation.html',
          pageName: 'Argumentation',
          description: 'Use the argumentation layer to inspect how mechanism-level claims are supported, attacked, or undercut. This is where Theory Explorer should feel different from ordinary browsing: you are not merely asking what happens, but why Atlas thinks it happens and what counts against that view.',
          lookFor: ['Which claims are explicitly mechanistic rather than merely associative?', 'What attack schemes or defeaters appear around the mechanism claims?', 'Where is the mechanism chain strongest, and where does it become speculative?'],
          imageType: 'argument-graph',
          collectArticles: false
        },
        {
          id: 's3',
          title: 'See How Atlas Itself Reasons',
          pageLink: 'ka_explain_system.html',
          pageName: 'How Atlas Works',
          description: 'Open the system explanation page to see how Atlas moves from extracted claims to warrants, argumentation, and proposed experiments. This matters because a theory explorer needs to know not only the content of the claim but the machinery that assembled it.',
          lookFor: ['How does Atlas distinguish warrant, interpretation, and projection?', 'Where in the system would a new mechanism be discovered, challenged, or promoted?', 'Which parts of the architecture remain more aspirational than complete?'],
          imageType: 'annotation-view',
          collectArticles: false
        },
        {
          id: 's4',
          title: 'Propose the Critical Experiment',
          pageLink: 'ka_hypothesis_builder.html',
          pageName: 'Hypothesis Builder',
          description: 'End by proposing the experiment that would best discriminate between the rival theories or mechanisms. A theory explorer should not stop at description; the real question is what study would force the field to learn something definite next.',
          lookFor: ['Which outcome and mediator would the experiment measure directly?', 'What result would support one theory and count against another?', 'Could this experiment be done in VR, in the field, or only in the lab?'],
          imageType: 'hypothesis-form',
          collectArticles: false
        }
      ]
    }

  }, // end workflows

  // ─── ROLE CONFIGURATION ──────────────────────────────────────────────────

  byRole: {
    student_explorer:         ['first-questions', 'deep-dive'],
    contributor:              ['evidence-pipeline', 'deep-dive', 'first-questions'],
    researcher:               ['hypothesis-test', 'lit-synthesis', 'evidence-pipeline', 'deep-dive'],
    practitioner:             ['design-decision', 'client-brief', 'deep-dive'],
    instructor:               ['student-onboarding'],
    theory_mechanism_explorer:['mechanism-trace', 'hypothesis-test', 'deep-dive']
  },

  // ─── ROLE META ────────────────────────────────────────────────────────────

  roleMeta: {
    student_explorer: {
      label: 'Student Explorer',
      icon: '🎒',
      color: '#2A7868',
      bgLight: '#f0fff4',
      description: 'You are learning how Atlas is meant to be explored. Start with the Did You Know findings, then move into the topic map and question tools before you try to collect or tag anything yourself.',
      tagline: 'Explore the evidence landscape before you build in it.'
    },
    contributor: {
      label: 'Contributor',
      icon: '🔧',
      color: '#1a56a4',
      bgLight: '#eff6ff',
      description: 'You are actively contributing to the ATLAS evidence base — finding articles, tagging claims, and building the pipeline. Your work directly determines what future researchers and practitioners can rely on.',
      tagline: 'Build the evidence base one verified claim at a time.'
    },
    researcher: {
      label: 'Researcher',
      icon: '🔬',
      color: '#8b1a2e',
      bgLight: '#fff1f2',
      description: 'You are using ATLAS to support your own research — testing hypotheses, synthesising literature, and identifying gaps worth filling. You bring methodological scepticism that the system needs.',
      tagline: 'Test your hypotheses against the evidence the field has actually produced.'
    },
    practitioner: {
      label: 'Practitioner',
      icon: '📐',
      color: '#b05e1a',
      bgLight: '#fff7ed',
      description: 'You are an architect, designer, or consultant using Atlas to turn an environment, image, or design option into likely human consequences and then into a concise practice-facing note.',
      tagline: 'Evidence-grounded design requires knowing what the science actually shows.'
    },
    instructor: {
      label: 'Instructor',
      icon: '🎓',
      color: '#2A5FA0',
      bgLight: '#eff6ff',
      description: 'You manage the course workflow — registrations, track assignments, research question allocation, and student progress monitoring. Your workflows are administrative but their downstream effects are academic.',
      tagline: 'The quality of student work begins with the clarity of your setup.'
    },
    theory_mechanism_explorer: {
      label: 'Theory Explorer',
      icon: '🧠',
      color: '#5c3d8f',
      bgLight: '#faf5ff',
      description: 'You are tracing theories, mechanisms, and critical tests. This mode foregrounds theory comparison, mechanism-level argumentation, and the parts of Atlas that explain how the system itself reasons.',
      tagline: 'Understand mechanism, not only outcome.'
    }
  },

  // ─── IMAGE TYPE DESCRIPTIONS (SVG / CSS art descriptions) ────────────────

  imageTypes: {
    'topic-browser':       { label: 'Topics Browser', symbol: '🗂️', color: '#2A7868' },
    'query-builder':       { label: 'Query Builder',  symbol: '🔍', color: '#1a56a4' },
    'article-search':      { label: 'Article Search', symbol: '📰', color: '#5c3d8f' },
    'submit-form':         { label: 'Submit Articles', symbol: '📤', color: '#b05e1a' },
    'evidence-card':       { label: 'Evidence Card',  symbol: '📊', color: '#8b1a2e' },
    'argument-graph':      { label: 'Argument Map',   symbol: '🔗', color: '#2A5FA0' },
    'qa-interface':        { label: 'ATLAS QA',       symbol: '💬', color: '#4a7c59' },
    'hypothesis-form':     { label: 'Hypothesis',     symbol: '⚗️', color: '#8b1a2e' },
    'tagger-ui':           { label: 'Tagger',         symbol: '🏷️', color: '#1a56a4' },
    'gap-view':            { label: 'Gap Map',        symbol: '🕳️', color: '#6b7280' },
    'interpretation-panel':{ label: 'Interpretation', symbol: '⚖️', color: '#5c3d8f' },
    'annotation-view':     { label: 'Annotations',   symbol: '📝', color: '#2A7868' },
    'admin-queue':         { label: 'Approval Queue', symbol: '📋', color: '#2A5FA0' },
    'admin-assign':        { label: 'Assignment',     symbol: '📌', color: '#2A5FA0' },
    'dashboard-view':      { label: 'Dashboard',      symbol: '📈', color: '#4a7c59' }
  }

}; // end KA_WORKFLOWS
