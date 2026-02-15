const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

let msgId = 1;

async function sendAndWait(method, params) {
  return new Promise(resolve => {
    const id = msgId++;
    const handler = (data) => {
      const result = JSON.parse(data);
      if (result.id === id) {
        ws.off('message', handler);
        resolve(result);
      }
    };
    ws.on('message', handler);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function typeText(text) {
  for (const char of text) {
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: char, text: char });
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: char });
    await new Promise(r => setTimeout(r, 30));
  }
}

ws.on('open', async () => {
  try {
    // Click search box or press Ctrl+K
    let result = await sendAndWait('Runtime.evaluate', {
      expression: `
        var searchBox = document.querySelector('input[placeholder*="Resources"], input[type="search"], [data-testid*="search"]');
        if (searchBox) {
          searchBox.focus();
          searchBox.click();
          return 'CLICKED search';
        }
        return 'Search not found';
      `
    });
    console.log('Search:', result.result?.result?.value);
    
    await new Promise(r => setTimeout(r, 300));
    
    console.log('Typing search...');
    await typeText('Mac mini M4');
    
    await new Promise(r => setTimeout(r, 500));
    
    // Check results
    result = await sendAndWait('Runtime.evaluate', {
      expression: `
        var results = document.querySelectorAll('[class*="result"], [class*="suggestion"], li');
        Array.from(results).slice(0, 5).map(r => r.textContent.substring(0, 50)).join(' | ');
      `
    });
    console.log('Results:', result.result?.result?.value);
    
  } catch (e) {
    console.error('Error:', e);
  }
  
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => { console.error('Error:', err.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 30000);
