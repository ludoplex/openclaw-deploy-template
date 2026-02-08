// ==UserScript==
// @name         LLM Session Exporter
// @namespace    http://mightyhouseinc.com/
// @version      1.0
// @description  Export chat sessions from Arena.ai, Perplexity, ChatGPT, Claude
// @author       MHI
// @match        https://arena.ai/*
// @match        https://lmarena.ai/*
// @match        https://www.perplexity.ai/*
// @match        https://perplexity.ai/*
// @match        https://chat.openai.com/*
// @match        https://chatgpt.com/*
// @match        https://claude.ai/*
// @grant        GM_download
// @grant        GM_setClipboard
// ==/UserScript==

(function() {
    'use strict';

    // Add export button to page
    function addExportButton() {
        if (document.getElementById('llm-export-btn')) return;
        
        const btn = document.createElement('button');
        btn.id = 'llm-export-btn';
        btn.innerHTML = '📥 Export';
        btn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99999;
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        `;
        btn.onclick = exportSession;
        document.body.appendChild(btn);
        
        // Also add "Export All" for library pages
        if (window.location.pathname.includes('library') || 
            window.location.pathname.includes('history')) {
            const btnAll = document.createElement('button');
            btnAll.id = 'llm-export-all-btn';
            btnAll.innerHTML = '📦 Export All';
            btnAll.style.cssText = btn.style.cssText.replace('bottom: 20px', 'bottom: 60px');
            btnAll.style.background = '#2196F3';
            btnAll.onclick = exportAllSessions;
            document.body.appendChild(btnAll);
        }
    }

    function detectPlatform() {
        const url = window.location.hostname;
        if (url.includes('arena.ai') || url.includes('lmarena.ai')) return 'arena';
        if (url.includes('perplexity.ai')) return 'perplexity';
        if (url.includes('chatgpt.com') || url.includes('chat.openai.com')) return 'chatgpt';
        if (url.includes('claude.ai')) return 'claude';
        return 'unknown';
    }

    function extractMessages() {
        const platform = detectPlatform();
        const messages = [];
        
        if (platform === 'arena') {
            // Arena.ai - look for message containers
            document.querySelectorAll('[class*="message"], [class*="turn"], article').forEach(el => {
                const text = el.innerText.trim();
                if (text.length > 10) {
                    messages.push({
                        role: el.className.toLowerCase().includes('user') ? 'user' : 'assistant',
                        content: text
                    });
                }
            });
        } else if (platform === 'perplexity') {
            // Perplexity - query and answer pairs
            const queries = document.querySelectorAll('[class*="query"], h1, h2');
            const answers = document.querySelectorAll('[class*="prose"], [class*="answer"], [class*="markdown"]');
            
            queries.forEach((q, i) => {
                messages.push({ role: 'user', content: q.innerText.trim() });
                if (answers[i]) {
                    messages.push({ role: 'assistant', content: answers[i].innerText.trim() });
                }
            });
        } else if (platform === 'chatgpt') {
            // ChatGPT - data attributes
            document.querySelectorAll('[data-message-author-role]').forEach(el => {
                messages.push({
                    role: el.getAttribute('data-message-author-role'),
                    content: el.innerText.trim()
                });
            });
        } else if (platform === 'claude') {
            // Claude.ai
            document.querySelectorAll('[class*="human"], [class*="assistant"]').forEach(el => {
                messages.push({
                    role: el.className.includes('human') ? 'user' : 'assistant',
                    content: el.innerText.trim()
                });
            });
        }
        
        // Fallback: if nothing found, get full page text
        if (messages.length === 0) {
            messages.push({
                role: 'full_page',
                content: document.body.innerText
            });
        }
        
        return messages;
    }

    function exportSession() {
        const data = {
            url: window.location.href,
            title: document.title,
            timestamp: new Date().toISOString(),
            platform: detectPlatform(),
            messages: extractMessages()
        };
        
        const filename = `${data.platform}-${Date.now()}.json`;
        const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        
        URL.revokeObjectURL(url);
        
        console.log(`Exported ${data.messages.length} messages to ${filename}`);
        showToast(`Exported ${data.messages.length} messages`);
    }

    async function exportAllSessions() {
        const platform = detectPlatform();
        const allExports = [];
        
        // Get all session links
        let sessionLinks = [];
        
        if (platform === 'perplexity') {
            sessionLinks = Array.from(document.querySelectorAll('a[href*="/search/"]'))
                .map(a => a.href);
        } else if (platform === 'arena') {
            sessionLinks = Array.from(document.querySelectorAll('a[href*="/c/"]'))
                .map(a => a.href);
        } else if (platform === 'chatgpt') {
            sessionLinks = Array.from(document.querySelectorAll('a[href*="/c/"]'))
                .map(a => a.href);
        }
        
        showToast(`Found ${sessionLinks.length} sessions. Check console for URLs.`);
        console.log('Session URLs to export:', sessionLinks);
        
        // Create a manifest file with all URLs
        const manifest = {
            platform: platform,
            timestamp: new Date().toISOString(),
            totalSessions: sessionLinks.length,
            urls: sessionLinks
        };
        
        const blob = new Blob([JSON.stringify(manifest, null, 2)], {type: 'application/json'});
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `${platform}-manifest-${Date.now()}.json`;
        a.click();
    }

    function showToast(message) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: #333;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 99999;
            font-size: 14px;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    // Initialize
    setTimeout(addExportButton, 1000);
    
    // Re-add button on navigation (SPA support)
    const observer = new MutationObserver(() => {
        setTimeout(addExportButton, 500);
    });
    observer.observe(document.body, { childList: true, subtree: true });

})();
