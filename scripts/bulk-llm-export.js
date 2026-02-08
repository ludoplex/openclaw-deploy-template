#!/usr/bin/env node
/**
 * Bulk LLM Session Exporter using Puppeteer
 * 
 * Usage:
 * 1. Close all Chrome/Brave windows
 * 2. Launch Chrome with: chrome --remote-debugging-port=9222
 * 3. Log into your LLM platforms
 * 4. Run: node bulk-llm-export.js
 */

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.join(__dirname, '..', 'llm-exports');
const CDP_PORT = 9222;

async function main() {
    console.log(`
===========================================
  Bulk LLM Session Exporter
===========================================

Before running:
1. Close all Chrome/Brave windows
2. Run one of these commands:

   Chrome:
   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222

   Brave:
   "C:\\Users\\user\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe" --remote-debugging-port=9222

3. Log into arena.ai, perplexity.ai, chatgpt.com
4. Then run this script again

===========================================
`);

    // Ensure output directory
    if (!fs.existsSync(OUTPUT_DIR)) {
        fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    let browser;
    try {
        // Connect to existing browser
        browser = await puppeteer.connect({
            browserURL: `http://127.0.0.1:${CDP_PORT}`,
            defaultViewport: null
        });
        
        console.log('✅ Connected to browser\n');
        
        const pages = await browser.pages();
        console.log(`Found ${pages.length} tabs\n`);
        
        for (const page of pages) {
            const url = page.url();
            const title = await page.title();
            
            // Check if it's an LLM platform
            const isLLM = ['arena.ai', 'lmarena.ai', 'perplexity.ai', 'chatgpt.com', 'chat.openai.com', 'claude.ai']
                .some(domain => url.includes(domain));
            
            if (!isLLM) continue;
            
            console.log(`Processing: ${title}`);
            console.log(`  URL: ${url}`);
            
            try {
                // Extract content
                const content = await page.evaluate(() => {
                    const data = {
                        url: window.location.href,
                        title: document.title,
                        timestamp: new Date().toISOString(),
                        fullText: document.body.innerText,
                        messages: []
                    };
                    
                    // Try to extract structured messages
                    // ChatGPT
                    document.querySelectorAll('[data-message-author-role]').forEach(el => {
                        data.messages.push({
                            role: el.getAttribute('data-message-author-role'),
                            content: el.innerText.trim()
                        });
                    });
                    
                    // Arena.ai / generic
                    if (data.messages.length === 0) {
                        document.querySelectorAll('[class*="message"], [class*="turn"], article').forEach(el => {
                            const text = el.innerText.trim();
                            if (text.length > 20) {
                                data.messages.push({
                                    role: 'unknown',
                                    content: text
                                });
                            }
                        });
                    }
                    
                    return data;
                });
                
                // Save to file
                const safeName = (content.title || 'untitled')
                    .replace(/[<>:"/\\|?*]/g, '-')
                    .substring(0, 80);
                const filename = `${safeName}-${Date.now()}.json`;
                const filepath = path.join(OUTPUT_DIR, filename);
                
                fs.writeFileSync(filepath, JSON.stringify(content, null, 2));
                console.log(`  ✅ Saved: ${filename}`);
                console.log(`  Messages: ${content.messages.length}`);
                console.log('');
                
            } catch (err) {
                console.log(`  ❌ Error: ${err.message}\n`);
            }
        }
        
        console.log(`\nExports saved to: ${OUTPUT_DIR}`);
        
    } catch (err) {
        if (err.message.includes('ECONNREFUSED')) {
            console.log('❌ Could not connect to browser.');
            console.log('   Make sure Chrome/Brave is running with --remote-debugging-port=9222');
        } else {
            console.error('Error:', err.message);
        }
    } finally {
        if (browser) {
            browser.disconnect();
        }
    }
}

main();
