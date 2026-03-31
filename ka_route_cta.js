(function () {
  function getScriptBase() {
    const current = document.currentScript;
    if (current && current.src) {
      return current.src.slice(0, current.src.lastIndexOf('/') + 1);
    }
    const match = Array.from(document.querySelectorAll('script[src]')).find((script) =>
      /ka_route_cta\.js(?:\?|$)/.test(script.getAttribute('src') || '')
    );
    if (match && match.src) {
      return match.src.slice(0, match.src.lastIndexOf('/') + 1);
    }
    return window.location.origin + '/';
  }

  const SCRIPT_BASE = getScriptBase();

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  async function ensureWorkflowStore() {
    if (window.KA_WORKFLOWS) return;
    await loadScript(new URL('ka_workflows.js', SCRIPT_BASE).toString());
  }

  function buildRoutedLink(workflowId, stepIdx, pageLink) {
    const url = new URL(pageLink, SCRIPT_BASE);
    url.searchParams.set('wf', workflowId);
    url.searchParams.set('step', String(stepIdx));
    url.searchParams.set('from', 'workflow');
    return url.pathname + url.search;
  }

  function injectStyles() {
    if (document.getElementById('ka-route-cta-style')) return;
    const style = document.createElement('style');
    style.id = 'ka-route-cta-style';
    style.textContent = `
      .ka-route-cta {
        max-width: 1180px;
        margin: 14px auto 0;
        padding: 0 24px;
      }
      .ka-route-cta-card {
        background: #FFF6E8;
        border: 1px solid #E8C98E;
        border-radius: 12px;
        padding: 14px 16px;
        color: #6B4C12;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
      }
      .ka-route-cta-kicker {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #9A6B13;
        margin-bottom: 8px;
      }
      .ka-route-cta-title {
        font-family: Georgia, serif;
        font-size: 1rem;
        color: #4E3411;
        margin-bottom: 6px;
      }
      .ka-route-cta-copy {
        font-size: 0.84rem;
        line-height: 1.6;
        margin-bottom: 12px;
      }
      .ka-route-cta-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }
      .ka-route-cta-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 14px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 0.82rem;
        font-weight: 700;
        transition: background 0.15s, color 0.15s, border-color 0.15s;
      }
      .ka-route-cta-btn.primary {
        background: #7A4B00;
        color: #FFF9F0;
      }
      .ka-route-cta-btn.primary:hover {
        background: #5F3900;
      }
      .ka-route-cta-btn.secondary {
        background: #FFFFFF;
        color: #6B4C12;
        border: 1px solid #DAB36D;
      }
      .ka-route-cta-btn.secondary:hover {
        border-color: #B98526;
        color: #4E3411;
      }
      @media (max-width: 720px) {
        .ka-route-cta {
          padding: 0 16px;
        }
        .ka-route-cta-actions {
          flex-direction: column;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function renderRouteBanner() {
    const params = new URLSearchParams(window.location.search);
    const workflowId = params.get('wf') || '';
    const from = params.get('from') || '';
    if (!workflowId || from !== 'workflow' || !window.KA_WORKFLOWS || !window.KA_WORKFLOWS.workflows[workflowId]) {
      return;
    }
    if (document.querySelector('.ka-route-cta')) return;

    const workflow = window.KA_WORKFLOWS.workflows[workflowId];
    const stepIdxRaw = parseInt(params.get('step') || '0', 10);
    const currentStepIdx = Math.max(0, Math.min(isNaN(stepIdxRaw) ? 0 : stepIdxRaw, workflow.steps.length - 1));
    const currentStep = workflow.steps[currentStepIdx];
    const previousStep = currentStepIdx > 0 ? workflow.steps[currentStepIdx - 1] : null;
    const nextStep = currentStepIdx < workflow.steps.length - 1 ? workflow.steps[currentStepIdx + 1] : null;

    const banner = document.createElement('section');
    banner.className = 'ka-route-cta';
    banner.innerHTML =
      '<div class="ka-route-cta-card">' +
        '<div class="ka-route-cta-kicker">Recommended path</div>' +
        '<div class="ka-route-cta-title">' + workflow.title + ' · Step ' + (currentStepIdx + 1) + ' of ' + workflow.steps.length + ': ' + currentStep.title + '</div>' +
        '<div class="ka-route-cta-copy">This page is part of the guided path <strong>' + workflow.title + '</strong>. You may browse freely, but if you want the intended sequence, use the buttons below.</div>' +
        '<div class="ka-route-cta-actions">' +
          '<a class="ka-route-cta-btn secondary" href="ka_workflow_hub.html?wf=' + encodeURIComponent(workflowId) + '&step=' + currentStepIdx + '">Path overview</a>' +
          (previousStep
            ? '<a class="ka-route-cta-btn secondary" href="' + buildRoutedLink(workflowId, currentStepIdx - 1, previousStep.pageLink) + '">Back: ' + previousStep.title + '</a>'
            : '') +
          (nextStep
            ? '<a class="ka-route-cta-btn primary" href="' + buildRoutedLink(workflowId, currentStepIdx + 1, nextStep.pageLink) + '">Next: ' + nextStep.title + ' →</a>'
            : '<a class="ka-route-cta-btn primary" href="ka_workflow_hub.html?wf=' + encodeURIComponent(workflowId) + '&step=' + currentStepIdx + '">Finish path</a>') +
        '</div>' +
      '</div>';

    const anchor = document.querySelector('nav, .top-nav, .topnav, header');
    if (anchor && anchor.parentNode) {
      if (anchor.nextSibling) {
        anchor.parentNode.insertBefore(banner, anchor.nextSibling);
      } else {
        anchor.parentNode.appendChild(banner);
      }
    } else if (document.body.firstChild) {
      document.body.insertBefore(banner, document.body.firstChild);
    } else {
      document.body.appendChild(banner);
    }
  }

  async function init() {
    injectStyles();
    try {
      await ensureWorkflowStore();
      renderRouteBanner();
    } catch (error) {
      console.warn('KA route CTA disabled:', error);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
