const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

ws.on('open', () => {
  console.log('Connected to CDP');
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: `
        (function() {
          // Find the Google SSO button
          var googleBtn = Array.from(document.querySelectorAll('button, a, div[role="button"]')).find(el => {
            var html = el.innerHTML.toLowerCase();
            var text = el.textContent.toLowerCase();
            return html.includes('google') || text.includes('google') || el.querySelector('svg[class*="google"]');
          });
          
          if (!googleBtn) {
            // Try finding by image/icon
            googleBtn = document.querySelector('button img[alt*="google" i], button svg, a img[alt*="google" i]')?.closest('button, a');
          }
          
          if (!googleBtn) {
            // Last resort: find buttons with only an SVG (icon buttons)
            var iconBtns = Array.from(document.querySelectorAll('button')).filter(b => 
              b.querySelector('svg') && b.textContent.trim().length < 5
            );
            if (iconBtns.length > 0) {
              googleBtn = iconBtns[0]; // First icon button is usually Google
            }
          }
          
          if (googleBtn) {
            googleBtn.click();
            return 'CLICKED: ' + googleBtn.outerHTML.substring(0, 200);
          }
          
          // List all buttons for debugging
          var allBtns = Array.from(document.querySelectorAll('button, a[class], div[role="button"]')).map(b => 
            b.tagName + ': ' + b.textContent.trim().substring(0, 30)
          );
          return 'NOT_FOUND: ' + allBtns.join(' | ');
        })()
      `
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  if (result.result && result.result.result) {
    console.log('Result:', result.result.result.value);
  } else {
    console.log('Result:', JSON.stringify(result, null, 2));
  }
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => {
  console.error('WS Error:', err.message);
  process.exit(1);
});

setTimeout(() => {
  console.error('Timeout');
  process.exit(1);
}, 10000);
