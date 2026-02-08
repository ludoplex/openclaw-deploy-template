#!/usr/bin/env node
/**
 * LLM Session Scraper
 * Connects directly to Chrome CDP to extract session data from:
 * - Arena.ai / lmarena.ai
 * - Perplexity.ai
 * - ChatGPT (if accessible)
 */

const CDP = require('chrome-remote-interface');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, '..', 'llm-exports');

async function main() {
    // Ensure output directory exists
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    console.log('Connecting to Chrome CDP on port 18793...');
    
    let client;
    try {
        // List all targets (tabs)
        const targets = await CDP.List({ port: 18793 });
        console.log(`Found ${targets.length} tabs:\n`);
        
        const relevantTabs = targets.filter(t => 
            t.url.includes('arena.ai') || 
            t.url.includes('lmarena.ai') || 
            t.url.includes('perplexity.ai') ||
            t.url.includes('chatgpt.com') ||
            t.url.includes('chat.openai.com')
        );
        
        console.log(`Relevant tabs: ${relevantTabs.length}`);
        
        for (const tab of relevantTabs) {
            console.log(`\n--- Processing: ${tab.title || tab.url} ---`);
            
            try {
                client = await CDP({ target: tab.id, port: 18793 });
                const { Page, Runtime } = client;
                
                // Get page content
                const result = await Runtime.evaluate({
                    expression: `(() => {
                        // Try to get the main content
                        const content = {
                            url: window.location.href,
                            title: document.title,
                            text: document.body.innerText,
                            html: document.body.innerHTML
                        };
                        return JSON.stringify(content);
                    })()`,
                    returnByValue: true
                });
                
                if (result.result.value) {
                    const content = JSON.parse(result.result.value);
                    const filename = sanitizeFilename(content.title || 'untitled') + '.json';
                    const filepath = path.join(OUTPUT_DIR, filename);
                    
                    fs.writeFileSync(filepath, JSON.stringify(content, null, 2));
                    console.log(`Saved: ${filepath}`);
                }
                
                await client.close();
            } catch (tabError) {
                console.error(`Error processing tab: ${tabError.message}`);
                if (client) await client.close().catch(() => {});
            }
        }
        
        console.log('\n✅ Done!');
        console.log(`Exports saved to: ${OUTPUT_DIR}`);
        
    } catch (err) {
        console.error('CDP Connection failed:', err.message);
        console.log('\nTroubleshooting:');
        console.log('1. Make sure Chrome/Brave has the OpenClaw extension active');
        console.log('2. Check that a tab is attached to the relay');
        console.log('3. Try: curl http://127.0.0.1:18793/json');
    }
}

function sanitizeFilename(name) {
    return name
        .replace(/[<>:"/\\|?*]/g, '-')
        .replace(/\s+/g, '_')
        .substring(0, 100);
}

main().catch(console.error);
