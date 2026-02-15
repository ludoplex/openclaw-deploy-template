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
          // Find and click "Add billing address" button
          var buttons = document.querySelectorAll('button');
          var addBtn = Array.from(buttons).find(b => 
            b.textContent.toLowerCase().includes('add billing') ||
            b.textContent.toLowerCase().includes('billing address')
          );
          
          if (addBtn) {
            addBtn.click();
            return 'CLICKED: ' + addBtn.textContent.trim();
          }
          
          // List all buttons for debugging
          var allBtns = Array.from(buttons).map(b => b.textContent.trim().substring(0, 30));
          return 'NOT_FOUND: ' + allBtns.join(', ');
        })()
      `
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  console.log('Result:', result.result?.result?.value || JSON.stringify(result, null, 2));
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => {
  console.error('WS Error:', err.message);
  process.exit(1);
});

setTimeout(() => {
  console.error('Timeout');
  ws.close();
  process.exit(0);
}, 10000);
