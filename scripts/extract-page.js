// Paste this into browser console (F12 → Console) on any LLM chat page
// It will download the full conversation as a text file

(function() {
    const url = window.location.href;
    const title = document.title.replace(/[^a-z0-9]/gi, '_').substring(0, 50);
    const timestamp = new Date().toISOString().split('T')[0];
    
    // Get all text content
    let content = `URL: ${url}\nTitle: ${document.title}\nExtracted: ${new Date().toISOString()}\n\n`;
    content += '='.repeat(80) + '\n\n';
    
    // Platform-specific extraction
    if (url.includes('arena.ai') || url.includes('lmarena.ai')) {
        // Arena/LMSYS - get chat messages
        const messages = document.querySelectorAll('.message, .chat-message, [class*="message"], .prose, .markdown');
        messages.forEach((m, i) => {
            content += `[Message ${i+1}]\n${m.innerText}\n\n---\n\n`;
        });
    } else if (url.includes('perplexity.ai')) {
        // Perplexity - get answer sections
        const answers = document.querySelectorAll('[class*="prose"], [class*="answer"], .markdown-body, main');
        answers.forEach((a, i) => {
            content += `[Section ${i+1}]\n${a.innerText}\n\n---\n\n`;
        });
    } else if (url.includes('chat.openai.com') || url.includes('chatgpt.com')) {
        // ChatGPT
        const turns = document.querySelectorAll('[data-message-author-role]');
        turns.forEach(t => {
            const role = t.getAttribute('data-message-author-role');
            content += `[${role}]\n${t.innerText}\n\n---\n\n`;
        });
    } else if (url.includes('claude.ai')) {
        // Claude
        const msgs = document.querySelectorAll('[class*="message"], .prose');
        msgs.forEach((m, i) => {
            content += `[Message ${i+1}]\n${m.innerText}\n\n---\n\n`;
        });
    } else if (url.includes('x.com') && url.includes('grok')) {
        // Grok
        const msgs = document.querySelectorAll('[class*="message"], [class*="response"]');
        msgs.forEach((m, i) => {
            content += `[Message ${i+1}]\n${m.innerText}\n\n---\n\n`;
        });
    }
    
    // Fallback - just get body text
    if (content.length < 500) {
        content += document.body.innerText;
    }
    
    // Download as file
    const blob = new Blob([content], {type: 'text/plain'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${title}_${timestamp}.txt`;
    a.click();
    
    console.log('✅ Downloaded:', a.download);
})();
