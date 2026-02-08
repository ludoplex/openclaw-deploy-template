// LLM Session Export Bookmarklet
// Drag this to your bookmarks bar, then click on any LLM chat page to extract content

javascript:(function(){
    const data = {
        url: window.location.href,
        title: document.title,
        timestamp: new Date().toISOString(),
        platform: detectPlatform(),
        messages: []
    };
    
    function detectPlatform() {
        const url = window.location.hostname;
        if (url.includes('arena.ai') || url.includes('lmarena.ai')) return 'arena';
        if (url.includes('perplexity.ai')) return 'perplexity';
        if (url.includes('chatgpt.com') || url.includes('chat.openai.com')) return 'chatgpt';
        if (url.includes('claude.ai')) return 'claude';
        return 'unknown';
    }
    
    // Platform-specific extraction
    if (data.platform === 'arena') {
        // Arena.ai format
        document.querySelectorAll('[class*="message"], [class*="chat"], [role="article"]').forEach(el => {
            data.messages.push({
                role: el.className.includes('user') ? 'user' : 'assistant',
                content: el.innerText.trim()
            });
        });
    } else if (data.platform === 'perplexity') {
        // Perplexity format
        document.querySelectorAll('[class*="prose"], [class*="answer"]').forEach(el => {
            data.messages.push({ role: 'assistant', content: el.innerText.trim() });
        });
    } else if (data.platform === 'chatgpt') {
        // ChatGPT format
        document.querySelectorAll('[data-message-author-role]').forEach(el => {
            data.messages.push({
                role: el.getAttribute('data-message-author-role'),
                content: el.innerText.trim()
            });
        });
    } else {
        // Fallback: just get all text
        data.messages.push({ role: 'unknown', content: document.body.innerText });
    }
    
    // Download as JSON
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${data.platform}-export-${Date.now()}.json`;
    a.click();
    
    console.log('Exported:', data);
    alert(`Exported ${data.messages.length} messages from ${data.platform}`);
})();
