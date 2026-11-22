document.addEventListener('DOMContentLoaded', () => {
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const messagesContainer = document.getElementById('messagesContainer');
  const heroSection = document.getElementById('heroSection');
  const clearBtn = document.getElementById('clearBtn');
  const exampleCards = document.querySelectorAll('.example-card');

  let hasMessages = false;

  // Click on example cards
  exampleCards.forEach(card => {
    card.addEventListener('click', () => {
      const query = card.getAttribute('data-query');
      if (query) {
        chatInput.value = query;
        sendMessage();
      }
    });
  });

  // Clear chat
  clearBtn.addEventListener('click', async () => {
    try {
      await fetch('/api/clear', { method: 'POST' });
      messagesContainer.innerHTML = '';
      heroSection.style.display = 'block';
      hasMessages = false;
    } catch (e) {
      console.error('Failed to clear conversation:', e);
    }
  });

  // Enter key press
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  sendBtn.addEventListener('click', sendMessage);

  async function sendMessage() {
    const query = chatInput.value.trim();
    if (!query) return;

    if (!hasMessages) {
      heroSection.style.display = 'none';
      hasMessages = true;
    }

    // Append user message
    appendUserMessage(query);
    chatInput.value = '';
    chatInput.focus();
    sendBtn.disabled = true;

    // Append loading bubble
    const loadingElem = appendLoadingBubble();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      const data = await response.json();
      loadingElem.remove();
      appendAssistantMessage(data);
    } catch (error) {
      loadingElem.remove();
      appendAssistantMessage({
        answer: 'Sorry, unable to retrieve official documentation right now. Please check server logs.',
        sources: [],
        retrieved_chunks: [],
        guardrail_triggered: true,
        guardrail_reason: 'NETWORK_ERROR'
      });
    } finally {
      sendBtn.disabled = false;
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
  }

  function appendUserMessage(text) {
    const wrap = document.createElement('div');
    wrap.className = 'message-wrapper user';
    wrap.innerHTML = `<div class="user-bubble">${escapeHtml(text)}</div>`;
    messagesContainer.appendChild(wrap);
  }

  function appendLoadingBubble() {
    const wrap = document.createElement('div');
    wrap.className = 'message-wrapper assistant';
    wrap.innerHTML = `
      <div class="assistant-card" style="padding: 14px 18px;">
        <span style="font-size: 13px; color: var(--text-muted); display: inline-flex; align-items: center; gap: 8px;">
          <span class="status-dot"></span> Searching verified scheme documents...
        </span>
      </div>
    `;
    messagesContainer.appendChild(wrap);
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    return wrap;
  }

  function appendAssistantMessage(data) {
    const wrap = document.createElement('div');
    wrap.className = 'message-wrapper assistant';

    const isAlert = data.guardrail_triggered;
    const alertHeader = isAlert ? `
      <div class="guardrail-header">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        ${data.guardrail_reason || 'Guardrail Triggered'}
      </div>
    ` : '';

    const rewrittenInfo = (data.rewritten_query && data.rewritten_query !== data.query) ? `
      <div class="context-tag">Context Disambiguation: "${escapeHtml(data.rewritten_query)}"</div>
    ` : '';

    const sourceLink = (data.sources && data.sources.length > 0) ? `
      <div class="source-container">
        <span style="font-size: 11.5px; color: var(--text-muted);">Verified Source:</span>
        <a href="${data.sources[0]}" target="_blank" rel="noopener noreferrer" class="source-pill">
          ${formatSourceHost(data.sources[0])}
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
        </a>
      </div>
    ` : '';

    // Evidence Chunks Drawer
    let evidenceDrawer = '';
    if (data.retrieved_chunks && data.retrieved_chunks.length > 0) {
      const drawerId = 'drawer-' + Math.random().toString(36).substring(2, 9);
      const chunkItems = data.retrieved_chunks.map((c, i) => `
        <div class="chunk-item">
          <div class="chunk-title">#${i + 1} ${escapeHtml(c.metadata.scheme_name || '')} &bull; ${escapeHtml(c.metadata.section || '')} (Score: ${c.distance ? c.distance.toFixed(3) : 'N/A'})</div>
          <div class="chunk-snippet">${escapeHtml(c.text.substring(0, 220))}...</div>
        </div>
      `).join('');

      evidenceDrawer = `
        <button class="evidence-toggle" onclick="toggleEvidence('${drawerId}')">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
          Inspect Retrieved Evidence Chunks (${data.retrieved_chunks.length})
        </button>
        <div class="evidence-drawer" id="${drawerId}">
          ${chunkItems}
        </div>
      `;
    }

    wrap.innerHTML = `
      <div class="assistant-card ${isAlert ? 'guardrail-alert' : ''}">
        ${alertHeader}
        ${rewrittenInfo}
        <div class="assistant-answer">${formatAnswerText(data.answer)}</div>
        ${sourceLink}
        ${evidenceDrawer}
      </div>
    `;

    messagesContainer.appendChild(wrap);
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  }

  window.toggleEvidence = function(id) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.toggle('open');
    }
  };

  function formatAnswerText(text) {
    if (!text) return '';
    // Strip trailing Source and Last updated duplicate if needed, or format
    return text.replace(/\n/g, '<br/>');
  }

  function formatSourceHost(url) {
    try {
      const parsed = new URL(url);
      const pathParts = parsed.pathname.split('/').filter(Boolean);
      return pathParts.length > 1 ? `${pathParts[pathParts.length - 1]}` : parsed.hostname;
    } catch (e) {
      return 'Official Document';
    }
  }

  function escapeHtml(string) {
    const div = document.createElement('div');
    div.innerText = string;
    return div.innerHTML;
  }
});
