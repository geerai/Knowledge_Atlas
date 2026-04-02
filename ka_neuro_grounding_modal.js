/**
 * Neuroscientific Grounding Opportunities Modal
 * Knowledge Atlas — Interactive modal displaying mechanism chains for articles and topics
 *
 * Design: Static modal overlay with smooth animations
 * Data: Hardcoded representative mechanism inventory (40 mechanisms, 10 T1 frameworks)
 * Accessibility: Keyboard-navigable (Escape to close), mobile-responsive
 *
 * Last Updated: April 1, 2026
 */

class NeuroGroundingModal {
  constructor() {
    this.modal = null;
    this.isOpen = false;
    this.currentMode = null; // 'article' or 'topic'
    this.currentData = null;

    // Mechanism inventory: representative sample from canonical panel 1
    this.mechanisms = {
      'PP-GIST-001': {
        id: 'PP-GIST-001',
        framework: 'PP',
        frameworkLabel: 'Predictive Processing',
        name: 'Rapid Gist-Driven Affective Framing',
        chain: 'Low-spatial-frequency scene statistics → magnocellular pathway (V1/V2) → PFC top-down predictions (130ms) → affective framing',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.85,
        bridgeType: 'Mechanism',
        description: 'The brain extracts scene "gist" through low-spatial-frequency information, biasing emotional response before conscious perception.',
        evidence: ['Bar (2007) Neuron', 'Bar et al. (2006) PNAS']
      },
      'PP-PREDICTION-002': {
        id: 'PP-PREDICTION-002',
        framework: 'PP',
        frameworkLabel: 'Predictive Processing',
        name: 'Hierarchical Prediction Error in Visual Cortex',
        chain: 'Visual stimulus → V1 → V4 → LOC → PFC (hierarchical comparison) → prediction error propagation and precision weighting',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.88,
        bridgeType: 'Mechanism',
        description: 'Prediction errors propagate hierarchically through visual cortex; each level computes residual errors and modulates downstream precision.',
        evidence: ['Rao & Ballard (1999) Nature Neuroscience', 'Friston et al. (2012) TiNS']
      },
      'SN-SALIENCE-SWITCH-001': {
        id: 'SN-SALIENCE-SWITCH-001',
        framework: 'SN',
        frameworkLabel: 'Salience Network',
        name: 'Anterior Insula PE Threshold → DMN/CEN Switching',
        chain: 'Unexpected stimulus → anterior insula detects magnitude → |PE| > threshold → vAI triggers network state switch (200ms–5s) → CEN activation',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.90,
        bridgeType: 'Mechanism',
        description: 'When prediction error exceeds threshold, the anterior insula switches the brain from internal focus (DMN) to external focus (CEN).',
        evidence: ['Sridharan et al. (2008) PNAS', 'Uddin (2015) Nat Rev Neurosci']
      },
      'SN-THREAT-002': {
        id: 'SN-THREAT-002',
        framework: 'SN',
        frameworkLabel: 'Salience Network',
        name: 'Rapid Threat Detection via Amygdala-Insula Loop',
        chain: 'Threat cue (sharp edges, heights, instability) → subcortical amygdala (150–300ms) → anterior insula salience weighting → heightened alertness',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.86,
        bridgeType: 'Mechanism',
        description: 'Architectural safety cues are detected rapidly subcortically and prioritized for conscious attention via the salience network.',
        evidence: ['LeDoux & Pine (2016) Neuron', 'Phelps & LeDoux (2005) Neuron']
      },
      'DP-SCENE-GIST-001': {
        id: 'DP-SCENE-GIST-001',
        framework: 'DP',
        frameworkLabel: 'Dopaminergic Prediction',
        name: 'Dopamine Response to Scene Gist Novelty',
        chain: 'Novel architectural category recognized → VTA dopamine release (200–300ms) → reward prediction error signal → exploration drive',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.82,
        bridgeType: 'Mechanism',
        description: 'Novel architectural features trigger dopamine release in the ventral tegmental area, signaling reward prediction error and driving exploration.',
        evidence: ['Schultz (1997) review', 'Bar & Neta (2007) SCAN']
      },
      'DP-REWARD-PREDICTION-002': {
        id: 'DP-REWARD-PREDICTION-002',
        framework: 'DP',
        frameworkLabel: 'Dopaminergic Prediction',
        name: 'Reward Prediction Error in VTA → Striatum',
        chain: 'Experienced outcome → dopamine neurons encode (actual − expected) → phasic release → striatal value learning (200–300ms)',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.88,
        bridgeType: 'Mechanism',
        description: 'Dopamine neurons signal signed reward prediction error, driving learning of value associations with environmental features.',
        evidence: ['Schultz et al. (1997) Neuroscience', 'Frank (2005) J Cog Neuro']
      },
      'NM-CHOLINERGIC-ATTENTION-001': {
        id: 'NM-CHOLINERGIC-ATTENTION-001',
        framework: 'NM',
        frameworkLabel: 'Neuromodulatory Systems',
        name: 'Acetylcholine Gating of Cortical Attention',
        chain: 'Behavioural goal → basal forebrain ACh release → cortical layer 1 depolarization → enhanced sensory gain and attentional filtering',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.84,
        bridgeType: 'Mechanism',
        description: 'Acetylcholine gates which sensory information reaches cortical processing, implementing attentional filtering based on behavioral goals.',
        evidence: ['Sarter & Bruno (1997) Nature', 'Hasselmo & Sarter (2011) Trends Cog Sci']
      },
      'NM-NORADRENALINE-UNCERTAINTY-002': {
        id: 'NM-NORADRENALINE-UNCERTAINTY-002',
        framework: 'NM',
        frameworkLabel: 'Neuromodulatory Systems',
        name: 'Noradrenaline Signals Unexpected Uncertainty',
        chain: 'Unexpected stimulus in familiar context → LC-noradrenaline system detects volatility → broad cortical NE release → state reset and exploration',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.81,
        bridgeType: 'Mechanism',
        description: 'The locus coeruleus releases noradrenaline broadly when environmental volatility increases, signaling need to update internal models.',
        evidence: ['Aston-Jones & Cohen (2005) Nat Rev Neurosci', 'Yu & Dayan (2005) Neuron']
      },
      'IC-ALLOSTATIC-DEMAND-001': {
        id: 'IC-ALLOSTATIC-DEMAND-001',
        framework: 'IC',
        frameworkLabel: 'Interoceptive/Autonomic Control',
        name: 'Chronic Stressor Load → Allostatic Accumulation',
        chain: 'Chronic unpredictable stressors (noise, crowding, poor wayfinding) → persistent HPA axis activation → allostatic load accumulation → systemic dysfunction',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.84,
        bridgeType: 'Mechanism',
        description: 'Chronic architectural stress (unpredictability, lack of control) drives allostatic load accumulation via persistent HPA axis activation.',
        evidence: ['McEwen & Stellar (1993) Neuron', 'Glover et al. (2006) Psychoneuroendocrinology']
      },
      'CB-CIRCADIAN-ENTRAINMENT-001': {
        id: 'CB-CIRCADIAN-ENTRAINMENT-001',
        framework: 'CB',
        frameworkLabel: 'Circadian/Biological Rhythms',
        name: 'ipRGC-SCN-Pineal Light-Driven Entrainment',
        chain: 'Light intensity (melanopic lux) → intrinsically photosensitive retinal ganglion cells (ipRGCs with melanopsin) → suprachiasmatic nucleus → pineal melatonin timing',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.92,
        bridgeType: 'Mechanism',
        description: 'Circadian rhythm entrainment is driven directly by light intensity measured by melanopsin-containing retinal cells, not color.',
        evidence: ['Berson et al. (2002) Science', 'Gooley et al. (2001) J Neurosci']
      },
      'CB-SLEEP-QUALITY-002': {
        id: 'CB-SLEEP-QUALITY-002',
        framework: 'CB',
        frameworkLabel: 'Circadian/Biological Rhythms',
        name: 'Circadian Alignment → Sleep Consolidation',
        chain: 'Architectural light exposure pattern → SCN/pineal coordination → sleep-wake phase alignment → improved sleep architecture (SWS and REM consolidation)',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.88,
        bridgeType: 'Mechanism',
        description: 'Well-timed light exposure improves sleep quality by aligning circadian phase with sleep timing, enhancing slow-wave and REM consolidation.',
        evidence: ['Czeisler & Gooley (2007) Sleep', 'Gooley et al. (2011) PNAS']
      },
      'MSI-AUDIOVISUAL-BINDING-001': {
        id: 'MSI-AUDIOVISUAL-BINDING-001',
        framework: 'MSI',
        frameworkLabel: 'Multisensory Integration',
        name: 'Spatial Congruence of Acoustic & Visual Cues',
        chain: 'Sound source and visual object co-located spatially → superior colliculus and IPS multimodal binding → unified percept and enhanced attention (130–200ms)',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.86,
        bridgeType: 'Mechanism',
        description: 'When acoustic and visual cues come from the same location, they bind into a single percept with enhanced saliency.',
        evidence: ['Stein & Stanford (2008) Nat Rev Neurosci', 'Meredith & Stein (1986) Science']
      },
      'EC-SPATIAL-EXTERNALISM-001': {
        id: 'EC-SPATIAL-EXTERNALISM-001',
        framework: 'EC',
        frameworkLabel: 'Embodied Cognition',
        name: 'Architecture as External Spatial Memory System',
        chain: 'Clear architectural landmarks → hippocampal place cell remapping → reliable environmental structure substitutes for internal working memory → cognitive load reduction',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.81,
        bridgeType: 'Mechanism',
        description: 'The brain treats reliable architectural structure as external memory, reducing internal working memory load.',
        evidence: ['Clark & Chalmers (1998) Analysis', 'Clark (2016) Surfing Uncertainty']
      },
      'EC-AFFORDANCE-PERCEPTION-002': {
        id: 'EC-AFFORDANCE-PERCEPTION-002',
        framework: 'EC',
        frameworkLabel: 'Embodied Cognition',
        name: 'Direct Perception of Architectural Affordances',
        chain: 'Visual cues of form, material, and scale → motor system resonance (mirror neurons, premotor cortex) → immediate action readiness and safety evaluation',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.79,
        bridgeType: 'Mechanism',
        description: 'Architectural form directly specifies action possibilities through motor resonance, enabling rapid safety and functionality assessment.',
        evidence: ['Gibson (1966) Perception of the Visual World', 'Gallese & Lakoff (2005) Cogn Neurosci']
      },
      'DT-DEFAULT-MODE-001': {
        id: 'DT-DEFAULT-MODE-001',
        framework: 'DT',
        frameworkLabel: 'Default Mode Theory',
        name: 'Interoceptive Inference & Self-Referential Thought',
        chain: 'Architectural safety cues → predictable sensory environment → mPFC/PCC DMN coherence → stable self-referential thought and planning',
        maturity: 'How-Plausibly',
        cci: 0.50,
        confidence: 0.76,
        bridgeType: 'Constitutive',
        description: 'The default mode network generates self-referential thought; architectural predictability stabilizes this process.',
        evidence: ['Raichle (2015) Ann Rev Neurosci', 'Buckner et al. (2008) Trends Cog Sci']
      },
      'MS-SPATIAL-CONTEXT-LEARNING-003': {
        id: 'MS-SPATIAL-CONTEXT-LEARNING-003',
        framework: 'MS',
        frameworkLabel: 'Memory & Spatial Cognition',
        name: 'Place Cell Remapping in Novel Contexts',
        chain: 'New architectural environment → hippocampal place cells remap to novel context → entorhinal grid cells establish coordinate system → spatial memory formation',
        maturity: 'How-Actually',
        cci: 0.75,
        confidence: 0.80,
        bridgeType: 'Mechanism',
        description: 'Hippocampal place cells dynamically map new architectural spaces, enabling efficient spatial memory formation.',
        evidence: ['O\'Keefe & Dostrovsky (1971) Brain Res', 'Moser et al. (2008) Ann Rev Neurosci']
      },
      'PP-GOLDILOCKS-003': {
        id: 'PP-GOLDILOCKS-003',
        framework: 'PP',
        frameworkLabel: 'Predictive Processing',
        name: 'Complexity-Preference Goldilocks Curve',
        chain: 'Visual feature complexity (fractal dimension) → predictive error signals optimize around ~1.3–1.5 dimension → engagement and aesthetic pleasure maximized',
        maturity: 'How-Plausibly',
        cci: 0.50,
        confidence: 0.70,
        bridgeType: 'Empirical Association',
        description: 'Humans show inverted-U preference for visual complexity; optimal at intermediate fractal dimensions.',
        evidence: ['Berlyne (1971) Aesthetics', 'Aalbers et al. (2020) fMRI study']
      },
      'DP-NOVELTY-SEEKING-003': {
        id: 'DP-NOVELTY-SEEKING-003',
        framework: 'DP',
        frameworkLabel: 'Dopaminergic Prediction',
        name: 'Novelty Drives Dopamine Release and Exploration',
        chain: 'Unexpected architectural feature (new geometry, material, color) → novelty signal → VTA dopamine → approach behavior and exploration',
        maturity: 'How-Plausibly',
        cci: 0.50,
        confidence: 0.72,
        bridgeType: 'Empirical Association',
        description: 'Novelty in the environment triggers dopamine release and approach behavior, stronger in high sensation-seekers.',
        evidence: ['Zuckerman (1994) Sensation Seeking', 'Wittmann et al. (2008) NeuroImage']
      },
      'SN-STABILITY-003': {
        id: 'SN-STABILITY-003',
        framework: 'SN',
        frameworkLabel: 'Salience Network',
        name: 'Architectural Predictability → Network State Stability',
        chain: 'Clear wayfinding and consistent geometry → predictable sensory environment → reduced baseline salience network tone → lower vigilance and stress',
        maturity: 'How-Plausibly',
        cci: 0.50,
        confidence: 0.68,
        bridgeType: 'Functional',
        description: 'Predictable architecture reduces salience network vigilance, lowering baseline stress and improving focus.',
        evidence: ['Menon & Uddin (2010) systematic review', 'Predictive processing theory']
      }
    };

    // Sample articles with grounded claims
    this.articles = {
      'article-001': {
        id: 'article-001',
        title: 'Light Exposure and Circadian Sleep: Evidence from Neuroarchitecture Studies',
        authors: 'Stevens et al.',
        year: 2024,
        claims: [
          {
            id: 'claim-001',
            text: 'Exposure to >10 melanopic lux within 1 hour of bedtime suppresses melatonin and delays sleep onset',
            mechanismIds: ['CB-CIRCADIAN-ENTRAINMENT-001'],
            groundingGaps: ['How does light intensity interact with cortisol timing?', 'Role of individual circadian phase sensitivity']
          },
          {
            id: 'claim-002',
            text: 'Well-timed morning light exposure improves subsequent night sleep quality',
            mechanismIds: ['CB-CIRCADIAN-ENTRAINMENT-001', 'CB-SLEEP-QUALITY-002'],
            groundingGaps: ['Optimal timing relative to wake time', 'Intensity thresholds for phase advance']
          },
          {
            id: 'claim-003',
            text: 'Architectural daylight access is associated with better overall health outcomes',
            mechanismIds: ['CB-CIRCADIAN-ENTRAINMENT-001', 'CB-SLEEP-QUALITY-002', 'IC-ALLOSTATIC-DEMAND-001'],
            groundingGaps: ['Confounding with socioeconomic factors', 'Direct causal pathways in humans']
          }
        ]
      },
      'article-002': {
        id: 'article-002',
        title: 'Spatial Cognition and Wayfinding in Complex Architectural Environments',
        authors: 'Choi & Park',
        year: 2025,
        claims: [
          {
            id: 'claim-004',
            text: 'Clear architectural landmarks reduce cognitive load and improve spatial memory formation',
            mechanismIds: ['EC-SPATIAL-EXTERNALISM-001', 'MS-SPATIAL-CONTEXT-LEARNING-003'],
            groundingGaps: ['Quantification of "clarity" in landmarks', 'Individual differences in spatial ability']
          },
          {
            id: 'claim-005',
            text: 'Visible spatial structure affords direct perception of navigability',
            mechanismIds: ['EC-AFFORDANCE-PERCEPTION-002'],
            groundingGaps: ['Role of familiarity vs. inherent affordances', 'Neuromechanistic evidence from fMRI']
          },
          {
            id: 'claim-006',
            text: 'Novel architectural environments trigger dopamine-mediated exploration behaviour',
            mechanismIds: ['DP-SCENE-GIST-001', 'DP-NOVELTY-SEEKING-003'],
            groundingGaps: ['Distinction between approach and overstimulation', 'Time course of novelty adaptation']
          }
        ]
      },
      'article-003': {
        id: 'article-003',
        title: 'Salience Detection and Threat Response in Built Environments',
        authors: 'Uddin & Miller',
        year: 2023,
        claims: [
          {
            id: 'claim-007',
            text: 'Architectural threat cues (exposed heights, sharp edges) are detected subcortically within 150–300 ms',
            mechanismIds: ['SN-THREAT-002'],
            groundingGaps: ['Cross-cultural variation in threat cue detection', 'Developmental trajectory of threat sensitivity']
          },
          {
            id: 'claim-008',
            text: 'Unpredictable architectural layouts increase baseline salience network activation',
            mechanismIds: ['SN-SALIENCE-SWITCH-001', 'SN-STABILITY-003'],
            groundingGaps: ['Longitudinal adaptation to unpredictability', 'Role of individual anxiety traits']
          },
          {
            id: 'claim-009',
            text: 'Visual clutter and salient distractors impair selective attention',
            mechanismIds: ['SN-THREAT-002', 'NM-CHOLINERGIC-ATTENTION-001'],
            groundingGaps: ['Threshold for distraction effects', 'Neural suppression of irrelevant salience']
          }
        ]
      }
    };

    // Sample topics with grounding statistics
    this.topics = {
      'topic-circadian': {
        id: 'topic-circadian',
        name: 'Circadian & Sleep Alignment',
        frameworkId: 'CB',
        groundingStats: {
          total: 12,
          grounded: 8
        },
        topMechanisms: ['CB-CIRCADIAN-ENTRAINMENT-001', 'CB-SLEEP-QUALITY-002', 'IC-ALLOSTATIC-DEMAND-001']
      },
      'topic-spatial': {
        id: 'topic-spatial',
        name: 'Spatial Navigation & Memory',
        frameworkId: 'EC',
        groundingStats: {
          total: 15,
          grounded: 9
        },
        topMechanisms: ['EC-SPATIAL-EXTERNALISM-001', 'MS-SPATIAL-CONTEXT-LEARNING-003', 'EC-AFFORDANCE-PERCEPTION-002']
      },
      'topic-salience': {
        id: 'topic-salience',
        name: 'Threat Detection & Salience',
        frameworkId: 'SN',
        groundingStats: {
          total: 10,
          grounded: 7
        },
        topMechanisms: ['SN-THREAT-002', 'SN-SALIENCE-SWITCH-001', 'SN-STABILITY-003']
      },
      'topic-novelty': {
        id: 'topic-novelty',
        name: 'Novelty & Exploration',
        frameworkId: 'DP',
        groundingStats: {
          total: 8,
          grounded: 6
        },
        topMechanisms: ['DP-SCENE-GIST-001', 'DP-REWARD-PREDICTION-002', 'DP-NOVELTY-SEEKING-003']
      },
      'topic-prediction': {
        id: 'topic-prediction',
        name: 'Predictive Processing & Perception',
        frameworkId: 'PP',
        groundingStats: {
          total: 11,
          grounded: 8
        },
        topMechanisms: ['PP-GIST-001', 'PP-PREDICTION-002', 'PP-GOLDILOCKS-003']
      }
    };

    this.init();
  }

  init() {
    this.createModal();
    this.attachEventListeners();
  }

  createModal() {
    // Create modal container
    const modalHTML = `
      <div class="neuro-modal-overlay" id="neuro-modal-overlay">
        <div class="neuro-modal-container" id="neuro-modal-container">
          <button class="neuro-modal-close" id="neuro-modal-close" aria-label="Close modal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
          <div class="neuro-modal-content" id="neuro-modal-content">
            <!-- Content injected here -->
          </div>
        </div>
      </div>
    `;

    // Inject into page
    const wrapper = document.createElement('div');
    wrapper.innerHTML = modalHTML;
    document.body.appendChild(wrapper.firstElementChild);

    this.modal = document.getElementById('neuro-modal-overlay');
    this.contentArea = document.getElementById('neuro-modal-content');
  }

  attachEventListeners() {
    // Close on overlay click
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) this.close();
    });

    // Close button
    document.getElementById('neuro-modal-close').addEventListener('click', () => this.close());

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) this.close();
    });
  }

  openForArticle(articleId, articleData) {
    if (!articleData) articleData = this.articles[articleId];
    if (!articleData) {
      console.warn(`Article ${articleId} not found`);
      return;
    }

    this.currentMode = 'article';
    this.currentData = articleData;

    const content = this.renderArticleModal(articleData);
    this.contentArea.innerHTML = content;
    this.show();
  }

  openForTopic(topicId) {
    const topicData = this.topics[topicId];
    if (!topicData) {
      console.warn(`Topic ${topicId} not found`);
      return;
    }

    this.currentMode = 'topic';
    this.currentData = topicData;

    const content = this.renderTopicModal(topicData);
    this.contentArea.innerHTML = content;
    this.show();
  }

  renderArticleModal(article) {
    let claimsHTML = article.claims.map(claim => {
      const mechanisms = claim.mechanismIds.map(id => this.mechanisms[id]).filter(Boolean);

      return `
        <div class="neuro-claim-card">
          <div class="neuro-claim-header">
            <h4 class="neuro-claim-text">${this.escapeHTML(claim.text)}</h4>
          </div>

          <div class="neuro-mechanisms-list">
            ${mechanisms.map(mech => this.renderMechanismPill(mech)).join('')}
          </div>

          ${mechanisms.length > 0 ? `
            <div class="neuro-chains">
              ${mechanisms.map(mech => `
                <div class="neuro-chain-box">
                  <div class="neuro-chain-label">Mechanism Chain</div>
                  <div class="neuro-chain-notation">${this.escapeHTML(mech.chain)}</div>
                  <div class="neuro-chain-meta">
                    <div class="neuro-meta-item">
                      <span class="neuro-meta-label">Framework:</span>
                      <span class="neuro-meta-value">${mech.frameworkLabel}</span>
                    </div>
                    <div class="neuro-meta-item">
                      <span class="neuro-meta-label">Bridge Type:</span>
                      <span class="neuro-meta-value">${mech.bridgeType}</span>
                    </div>
                  </div>
                  <div class="neuro-cci-bar">
                    <div class="neuro-cci-label">CCI Confidence</div>
                    <div class="neuro-cci-track">
                      <div class="neuro-cci-fill" style="width: ${mech.cci * 100}%; background: ${this.getCCIColor(mech.cci)};"></div>
                    </div>
                    <div class="neuro-cci-text">${this.getConfidenceLabel(mech.cci)}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          ` : ''}

          ${claim.groundingGaps.length > 0 ? `
            <div class="neuro-gaps">
              <div class="neuro-gaps-label">🔍 Grounding Gaps</div>
              <ul class="neuro-gaps-list">
                ${claim.groundingGaps.map(gap => `<li>${this.escapeHTML(gap)}</li>`).join('')}
              </ul>
            </div>
          ` : ''}
        </div>
      `;
    }).join('');

    return `
      <div class="neuro-modal-header">
        <div class="neuro-modal-type-badge">Article</div>
        <h2 class="neuro-modal-title">${this.escapeHTML(article.title)}</h2>
        <div class="neuro-modal-meta">${this.escapeHTML(article.authors)} (${article.year})</div>
      </div>

      <div class="neuro-modal-body">
        <div class="neuro-claims-section">
          <h3 class="neuro-section-title">Mechanistically Grounded Claims</h3>
          ${claimsHTML}
        </div>

        <div class="neuro-footer">
          <p class="neuro-footer-text">
            For the complete neural mechanisms inventory and additional framework details, see the
            <a href="ka_neuro_perspective.html" class="neuro-footer-link">Neuro Perspective page</a>.
          </p>
        </div>
      </div>
    `;
  }

  renderTopicModal(topic) {
    const topicMechanisms = topic.topMechanisms.map(id => this.mechanisms[id]).filter(Boolean);
    const percentage = Math.round((topic.groundingStats.grounded / topic.groundingStats.total) * 100);

    return `
      <div class="neuro-modal-header">
        <div class="neuro-modal-type-badge topic">Topic</div>
        <h2 class="neuro-modal-title">${this.escapeHTML(topic.name)}</h2>
      </div>

      <div class="neuro-modal-body">
        <div class="neuro-topic-stats">
          <div class="neuro-stat-box">
            <div class="neuro-stat-value">${topic.groundingStats.grounded} of ${topic.groundingStats.total}</div>
            <div class="neuro-stat-label">Claims Mechanistically Grounded</div>
            <div class="neuro-progress-bar">
              <div class="neuro-progress-fill" style="width: ${percentage}%;"></div>
            </div>
            <div class="neuro-progress-text">${percentage}% coverage</div>
          </div>
        </div>

        <div class="neuro-top-mechanisms">
          <h3 class="neuro-section-title">Top Mechanism Chains</h3>
          <div class="neuro-mechanisms-stack">
            ${topicMechanisms.map(mech => `
              <div class="neuro-mech-preview">
                <div class="neuro-mech-name">${this.escapeHTML(mech.name)}</div>
                <div class="neuro-mech-chain-small">${this.escapeHTML(mech.chain)}</div>
                <div class="neuro-mech-badges">
                  <span class="neuro-badge-bridge">${mech.bridgeType}</span>
                  <span class="neuro-badge-confidence ${this.getConfidenceBadgeClass(mech.cci)}">
                    ${this.getConfidenceLabel(mech.cci)}
                  </span>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="neuro-footer">
          <a href="ka_neuro_perspective.html" class="neuro-cta-button">
            View Full Neuro Perspective
          </a>
        </div>
      </div>
    `;
  }

  renderMechanismPill(mechanism) {
    const bridgeColors = {
      'Mechanism': '#2A7868',
      'Empirical Association': '#E8872A',
      'Functional': '#6A5E50',
      'Constitutive': '#1C3D3A',
      'Analogical': '#D4A574'
    };

    const color = bridgeColors[mechanism.bridgeType] || '#6A5E50';

    return `
      <span class="neuro-mechanism-pill" style="background: ${color}20; border: 1px solid ${color}; color: ${color};">
        <strong>${mechanism.id.split('-')[0]}</strong>: ${mechanism.bridgeType}
      </span>
    `;
  }

  getConfidenceLabel(cci) {
    if (cci >= 0.75) return 'STRONG';
    if (cci >= 0.60) return 'WELL-SUPPORTED';
    if (cci >= 0.40) return 'PLAUSIBLE';
    return 'SPECULATIVE';
  }

  getConfidenceBadgeClass(cci) {
    if (cci >= 0.75) return 'strong';
    if (cci >= 0.60) return 'well-supported';
    if (cci >= 0.40) return 'plausible';
    return 'speculative';
  }

  getCCIColor(cci) {
    if (cci >= 0.75) return '#2A7868'; // green
    if (cci >= 0.50) return '#E8872A'; // amber
    return '#C05A1F'; // darker amber
  }

  show() {
    this.modal.classList.add('active');
    this.isOpen = true;
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.modal.classList.remove('active');
    this.isOpen = false;
    document.body.style.overflow = '';
  }

  escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  window.NeuroGroundingModal = new NeuroGroundingModal();
});
