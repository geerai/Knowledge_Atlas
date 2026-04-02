(function () {
  'use strict';

  const STORAGE_KEY = 'ka_workspace_state_v1';
  const DEFAULT_FOLDER_ID = 'default';
  const DEFAULT_FOLDER_NAME = 'General';

  let widgetEl = null;
  let panelOpen = false;
  let flashTimeout = null;

  function nowIso() {
    return new Date().toISOString();
  }

  function loadState() {
    try {
      const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (parsed && typeof parsed === 'object') {
        return normalizeState(parsed);
      }
    } catch (_error) {}
    return normalizeState({});
  }

  function normalizeState(raw) {
    const folders = Array.isArray(raw.folders) ? raw.folders.filter(Boolean) : [];
    if (!folders.some((folder) => folder.id === DEFAULT_FOLDER_ID)) {
      folders.unshift({ id: DEFAULT_FOLDER_ID, name: DEFAULT_FOLDER_NAME, createdAt: nowIso() });
    }
    const items = Array.isArray(raw.items) ? raw.items.filter(Boolean).map(normalizeItem) : [];
    const currentFolderId = folders.some((folder) => folder.id === raw.currentFolderId)
      ? raw.currentFolderId
      : DEFAULT_FOLDER_ID;
    return { folders, currentFolderId, items };
  }

  function normalizeItem(item) {
    return {
      id: item.id || makeId('item'),
      kind: String(item.kind || 'note'),
      sourceId: String(item.sourceId || item.id || ''),
      title: String(item.title || 'Untitled item'),
      subtitle: String(item.subtitle || ''),
      url: String(item.url || ''),
      notes: String(item.notes || ''),
      folderId: String(item.folderId || DEFAULT_FOLDER_ID),
      addedAt: item.addedAt || nowIso(),
      sourcePage: String(item.sourcePage || window.location.pathname.split('/').pop() || ''),
      meta: item.meta && typeof item.meta === 'object' ? item.meta : {},
    };
  }

  function saveState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(normalizeState(state)));
    } catch (_error) {}
  }

  function getState() {
    return loadState();
  }

  function updateState(mutator) {
    const state = loadState();
    const next = mutator(normalizeState(state)) || state;
    saveState(next);
    render();
    return next;
  }

  function makeId(prefix) {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  }

  function dedupeKey(item) {
    return [
      String(item.kind || ''),
      String(item.sourceId || ''),
      String(item.url || ''),
      String(item.title || '').toLowerCase(),
      String(item.folderId || DEFAULT_FOLDER_ID),
    ].join('::');
  }

  function currentFolder(state) {
    const snapshot = state || loadState();
    return snapshot.folders.find((folder) => folder.id === snapshot.currentFolderId) || snapshot.folders[0];
  }

  function getItems(folderId) {
    const state = loadState();
    if (!folderId) return state.items.slice();
    return state.items.filter((item) => item.folderId === folderId);
  }

  function getFolders() {
    return loadState().folders.slice();
  }

  function count(folderId) {
    return getItems(folderId).length;
  }

  function add(item) {
    const state = loadState();
    const folderId = item.folderId || state.currentFolderId || DEFAULT_FOLDER_ID;
    const normalized = normalizeItem({ ...item, folderId });
    const key = dedupeKey(normalized);
    const exists = state.items.some((row) => dedupeKey(row) === key);
    if (exists) {
      flash('Already saved');
      openPanel();
      return null;
    }
    state.items.unshift(normalized);
    saveState(state);
    render();
    flash('Saved to workspace');
    openPanel();
    pulse();
    return normalized;
  }

  function remove(itemId) {
    updateState((state) => {
      state.items = state.items.filter((item) => item.id !== itemId);
      return state;
    });
  }

  function clearCurrentFolder() {
    const state = loadState();
    const folderId = state.currentFolderId;
    updateState((next) => {
      next.items = next.items.filter((item) => item.folderId !== folderId);
      return next;
    });
  }

  function clearKind(kind) {
    updateState((state) => {
      state.items = state.items.filter((item) => item.kind !== kind);
      return state;
    });
  }

  function createFolder(name) {
    const clean = String(name || '').trim();
    if (!clean) return null;
    const state = loadState();
    const existing = state.folders.find((folder) => folder.name.toLowerCase() === clean.toLowerCase());
    if (existing) {
      state.currentFolderId = existing.id;
      saveState(state);
      render();
      return existing;
    }
    const folder = { id: makeId('folder'), name: clean, createdAt: nowIso() };
    state.folders.push(folder);
    state.currentFolderId = folder.id;
    saveState(state);
    render();
    flash(`Folder created: ${clean}`);
    openPanel();
    return folder;
  }

  function setCurrentFolder(folderId) {
    updateState((state) => {
      if (state.folders.some((folder) => folder.id === folderId)) {
        state.currentFolderId = folderId;
      }
      return state;
    });
  }

  function buildMarkdown(folderId) {
    const state = loadState();
    const folder = folderId
      ? state.folders.find((row) => row.id === folderId)
      : currentFolder(state);
    const items = state.items.filter((item) => item.folderId === folder.id);
    const lines = [
      `# ${folder.name}`,
      '',
      `Generated: ${new Date().toLocaleString()}`,
      '',
    ];
    if (!items.length) {
      lines.push('_No saved items yet._');
      return lines.join('\n');
    }
    items.forEach((item, index) => {
      lines.push(`## ${index + 1}. ${item.title}`);
      lines.push(`- Kind: ${item.kind}`);
      if (item.subtitle) lines.push(`- Summary: ${item.subtitle}`);
      if (item.url) lines.push(`- Link: ${item.url}`);
      if (item.sourcePage) lines.push(`- Source page: ${item.sourcePage}`);
      if (item.notes) lines.push(`- Notes: ${item.notes}`);
      if (item.meta && Object.keys(item.meta).length) {
        Object.entries(item.meta).forEach(([key, value]) => {
          if (value === '' || value === null || value === undefined) return;
          lines.push(`- ${humanizeKey(key)}: ${Array.isArray(value) ? value.join(', ') : value}`);
        });
      }
      lines.push('');
    });
    return lines.join('\n');
  }

  function humanizeKey(key) {
    return String(key || '')
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (match) => match.toUpperCase());
  }

  function copyMarkdown(folderId) {
    const text = buildMarkdown(folderId);
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      flash('Clipboard unavailable');
      return Promise.resolve(false);
    }
    return navigator.clipboard.writeText(text)
      .then(() => {
        flash('Workspace copied as Markdown');
        return true;
      })
      .catch(() => {
        flash('Could not copy Markdown');
        return false;
      });
  }

  function exportMarkdownFile(folderId) {
    const state = loadState();
    const folder = folderId
      ? state.folders.find((row) => row.id === folderId)
      : currentFolder(state);
    const text = buildMarkdown(folder.id);
    const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${folder.name.toLowerCase().replace(/[^a-z0-9]+/g, '-') || 'workspace'}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    flash('Markdown export ready');
  }

  function wireButtons(root) {
    const scope = root || document;
    scope.querySelectorAll('[data-workspace-title]').forEach((node) => {
      if (node.dataset.workspaceBound === 'true') return;
      node.dataset.workspaceBound = 'true';
      node.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        let meta = {};
        const rawMeta = node.dataset.workspaceMeta || '';
        if (rawMeta) {
          try { meta = JSON.parse(rawMeta); } catch (_error) {}
        }
        add({
          kind: node.dataset.workspaceKind || 'note',
          sourceId: node.dataset.workspaceId || '',
          title: node.dataset.workspaceTitle || node.textContent || 'Saved item',
          subtitle: node.dataset.workspaceSubtitle || '',
          url: node.dataset.workspaceUrl || '',
          notes: node.dataset.workspaceNotes || '',
          meta,
        });
      });
    });
  }

  function injectStyles() {
    if (document.getElementById('ka-workspace-style')) return;
    const style = document.createElement('style');
    style.id = 'ka-workspace-style';
    style.textContent = `
      #ka-workspace-widget {
        position: fixed;
        right: 24px;
        bottom: 24px;
        z-index: 9100;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }
      #ka-workspace-toggle {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: #2A7868;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(28,61,58,0.28);
        position: relative;
        font-size: 1.35rem;
        user-select: none;
      }
      #ka-workspace-toggle.pulse { animation: ka-workspace-pulse .34s ease-out; }
      @keyframes ka-workspace-pulse {
        0% { transform: scale(1); }
        45% { transform: scale(1.14); }
        100% { transform: scale(1); }
      }
      #ka-workspace-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        min-width: 22px;
        height: 22px;
        border-radius: 999px;
        background: #f59e0b;
        color: #1f2937;
        font-size: 0.72rem;
        font-weight: 800;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 0 6px;
      }
      #ka-workspace-panel {
        position: absolute;
        right: 0;
        bottom: 66px;
        width: 360px;
        max-height: 560px;
        background: #fff;
        border: 1.5px solid #d7e6df;
        border-radius: 14px;
        box-shadow: 0 14px 40px rgba(0,0,0,0.16);
        display: none;
        flex-direction: column;
        overflow: hidden;
      }
      #ka-workspace-header {
        padding: 14px 16px;
        background: #1C3D3A;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }
      #ka-workspace-title {
        font-size: 0.96rem;
        font-weight: 800;
      }
      #ka-workspace-actions {
        display: flex;
        gap: 6px;
      }
      #ka-workspace-actions button {
        background: rgba(255,255,255,0.12);
        border: none;
        color: #fff;
        border-radius: 6px;
        padding: 4px 8px;
        font-size: 0.75rem;
        cursor: pointer;
      }
      #ka-workspace-folderbar {
        padding: 10px 12px;
        border-bottom: 1px solid #edf2ef;
        display: flex;
        gap: 8px;
        align-items: center;
      }
      #ka-workspace-folder-select {
        flex: 1;
        padding: 7px 10px;
        border: 1.5px solid #d7e6df;
        border-radius: 8px;
        font-size: 0.84rem;
      }
      #ka-workspace-new-folder {
        border: 1px solid #b9d3ca;
        background: #f7fbf9;
        color: #1C3D3A;
        border-radius: 8px;
        padding: 7px 10px;
        font-size: 0.8rem;
        font-weight: 700;
        cursor: pointer;
      }
      #ka-workspace-copy {
        border: 1px solid #b9d3ca;
        background: #f7fbf9;
        color: #1C3D3A;
        border-radius: 8px;
        padding: 7px 10px;
        font-size: 0.8rem;
        font-weight: 700;
        cursor: pointer;
      }
      #ka-workspace-flash {
        display: none;
        padding: 8px 12px;
        background: #eefaf5;
        color: #1C3D3A;
        font-size: 0.8rem;
        border-bottom: 1px solid #d7e6df;
      }
      #ka-workspace-list-wrap {
        flex: 1;
        overflow-y: auto;
        padding: 8px 10px;
        background: #fafcfa;
      }
      .ka-workspace-empty {
        padding: 26px 18px;
        text-align: center;
        color: #6b7280;
        font-size: 0.86rem;
        line-height: 1.55;
      }
      .ka-workspace-item {
        background: #fff;
        border: 1px solid #ebf0ed;
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 8px;
        display: flex;
        gap: 10px;
        align-items: flex-start;
      }
      .ka-workspace-item-main {
        flex: 1;
        min-width: 0;
      }
      .ka-workspace-kind {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #2A7868;
        margin-bottom: 6px;
      }
      .ka-workspace-item-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #1f2937;
        line-height: 1.4;
      }
      .ka-workspace-item-subtitle,
      .ka-workspace-item-meta {
        font-size: 0.77rem;
        color: #6b7280;
        line-height: 1.45;
        margin-top: 4px;
      }
      .ka-workspace-item-remove {
        background: none;
        border: none;
        color: #9ca3af;
        cursor: pointer;
        font-size: 1rem;
      }
      #ka-workspace-footer {
        padding: 10px 12px;
        border-top: 1px solid #edf2ef;
        background: #f7fbf9;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }
      #ka-workspace-footer-copy {
        font-size: 0.8rem;
        color: #6b7280;
      }
      #ka-workspace-open-page {
        font-size: 0.82rem;
        font-weight: 700;
        color: #1a56a4;
        text-decoration: none;
      }
      .ka-workspace-save-btn {
        border: 1px solid #b9d3ca;
        background: #f7fbf9;
        color: #1C3D3A;
        border-radius: 999px;
        padding: 5px 10px;
        font-size: 0.75rem;
        font-weight: 700;
        cursor: pointer;
      }
      .ka-workspace-save-btn:hover,
      #ka-workspace-new-folder:hover,
      #ka-workspace-copy:hover {
        background: #edf7f3;
      }
      @media (max-width: 520px) {
        #ka-workspace-panel { width: calc(100vw - 32px); }
      }
    `;
    document.head.appendChild(style);
  }

  function buildWidget() {
    if (widgetEl) return;
    injectStyles();
    const widget = document.createElement('div');
    widget.id = 'ka-workspace-widget';
    widget.innerHTML = `
      <div id="ka-workspace-toggle" title="Open workspace" aria-label="Open workspace">
        <span>🗂️</span>
        <span id="ka-workspace-badge">0</span>
      </div>
      <div id="ka-workspace-panel" aria-live="polite">
        <div id="ka-workspace-header">
          <div id="ka-workspace-title">Workspace</div>
          <div id="ka-workspace-actions">
            <button id="ka-workspace-export-btn" title="Download Markdown">⬇︎</button>
            <button id="ka-workspace-close-btn" title="Close">✕</button>
          </div>
        </div>
        <div id="ka-workspace-folderbar">
          <select id="ka-workspace-folder-select" aria-label="Choose folder"></select>
          <button id="ka-workspace-new-folder" type="button">New folder</button>
          <button id="ka-workspace-copy" type="button">Copy MD</button>
        </div>
        <div id="ka-workspace-flash"></div>
        <div id="ka-workspace-list-wrap">
          <div id="ka-workspace-empty" class="ka-workspace-empty">Save articles, topics, evidence, or questions as you move through Atlas. Your current folder becomes the basket for this route.</div>
          <div id="ka-workspace-list"></div>
        </div>
        <div id="ka-workspace-footer">
          <div id="ka-workspace-footer-copy">0 items in this folder</div>
          <a id="ka-workspace-open-page" href="ka_my_work.html">Open My Work →</a>
        </div>
      </div>
    `;
    document.body.appendChild(widget);
    widget.querySelector('#ka-workspace-toggle').addEventListener('click', togglePanel);
    widget.querySelector('#ka-workspace-close-btn').addEventListener('click', closePanel);
    widget.querySelector('#ka-workspace-new-folder').addEventListener('click', () => {
      const name = window.prompt('New folder name');
      if (name) createFolder(name);
    });
    widget.querySelector('#ka-workspace-copy').addEventListener('click', () => copyMarkdown());
    widget.querySelector('#ka-workspace-export-btn').addEventListener('click', () => exportMarkdownFile());
    widget.querySelector('#ka-workspace-folder-select').addEventListener('change', (event) => {
      setCurrentFolder(event.target.value);
    });
    widgetEl = widget;
    render();
  }

  function togglePanel() {
    panelOpen ? closePanel() : openPanel();
  }

  function openPanel() {
    buildWidget();
    panelOpen = true;
    widgetEl.querySelector('#ka-workspace-panel').style.display = 'flex';
  }

  function closePanel() {
    if (!widgetEl) return;
    panelOpen = false;
    widgetEl.querySelector('#ka-workspace-panel').style.display = 'none';
  }

  function flash(message) {
    if (!widgetEl) return;
    const flashEl = widgetEl.querySelector('#ka-workspace-flash');
    flashEl.textContent = message;
    flashEl.style.display = 'block';
    clearTimeout(flashTimeout);
    flashTimeout = setTimeout(() => {
      flashEl.style.display = 'none';
    }, 2200);
  }

  function pulse() {
    if (!widgetEl) return;
    const toggle = widgetEl.querySelector('#ka-workspace-toggle');
    toggle.classList.remove('pulse');
    void toggle.offsetWidth;
    toggle.classList.add('pulse');
  }

  function itemKindLabel(kind) {
    const labels = {
      article: 'Article',
      evidence: 'Evidence',
      topic: 'Topic',
      question: 'Question',
      front: 'Front',
      note: 'Note',
    };
    return labels[kind] || humanizeKey(kind);
  }

  function render() {
    if (!widgetEl) return;
    const state = loadState();
    const folder = currentFolder(state);
    const folderItems = state.items.filter((item) => item.folderId === folder.id);
    const select = widgetEl.querySelector('#ka-workspace-folder-select');
    select.innerHTML = state.folders.map((entry) => {
      const selected = entry.id === folder.id ? ' selected' : '';
      return `<option value="${entry.id}"${selected}>${entry.name}</option>`;
    }).join('');

    const badge = widgetEl.querySelector('#ka-workspace-badge');
    badge.textContent = folderItems.length;
    badge.style.display = folderItems.length ? 'flex' : 'none';
    widgetEl.querySelector('#ka-workspace-footer-copy').textContent =
      `${folderItems.length} item${folderItems.length === 1 ? '' : 's'} in ${folder.name}`;

    const empty = widgetEl.querySelector('#ka-workspace-empty');
    const list = widgetEl.querySelector('#ka-workspace-list');
    if (!folderItems.length) {
      empty.style.display = 'block';
      list.innerHTML = '';
      return;
    }
    empty.style.display = 'none';
    list.innerHTML = folderItems.map((item) => {
      const metaBits = [];
      if (item.meta && item.meta.paperId) metaBits.push(item.meta.paperId);
      if (item.meta && item.meta.year) metaBits.push(item.meta.year);
      if (item.sourcePage) metaBits.push(item.sourcePage);
      return `
        <div class="ka-workspace-item">
          <div class="ka-workspace-item-main">
            <div class="ka-workspace-kind">${itemKindLabel(item.kind)}</div>
            <div class="ka-workspace-item-title">${escapeHtml(item.title)}</div>
            ${item.subtitle ? `<div class="ka-workspace-item-subtitle">${escapeHtml(item.subtitle)}</div>` : ''}
            ${metaBits.length ? `<div class="ka-workspace-item-meta">${escapeHtml(metaBits.join(' · '))}</div>` : ''}
          </div>
          <button class="ka-workspace-item-remove" data-id="${item.id}" title="Remove">✕</button>
        </div>
      `;
    }).join('');
    list.querySelectorAll('.ka-workspace-item-remove').forEach((button) => {
      button.addEventListener('click', () => remove(button.dataset.id));
    });
  }

  function escapeHtml(text) {
    return String(text || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        buildWidget();
        wireButtons();
      }, { once: true });
    } else {
      buildWidget();
      wireButtons();
    }
  }

  window.KA_WORKSPACE = {
    init,
    add,
    remove,
    count,
    getAll: getItems,
    getFolders,
    getState,
    currentFolderId: () => loadState().currentFolderId,
    setCurrentFolder,
    createFolder,
    clearCurrentFolder,
    clearKind,
    buildMarkdown,
    copyMarkdown,
    exportMarkdownFile,
    wireButtons,
    openPanel,
    closePanel,
  };

  init();
})();
