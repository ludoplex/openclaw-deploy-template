const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

ws.on('open', () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: `
        (function() {
          // Find and click "Add billing information" link
          var link = Array.from(document.querySelectorAll('a, button')).find(el => 
            el.textContent.toLowerCase().includes('add billing') ||
            el.textContent.toLowerCase().includes('payment method')
          );
          if (link) {
            link.click();
            return 'CLICKED: ' + link.textContent.trim().substring(0, 50);
          }
          return 'NOT_FOUND';
        })()
      `
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  console.log('Result:', result.result?.result?.value || JSON.stringify(result));
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => { console.error('Error:', err.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 10000);
