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
          // Scroll down to see more content
          window.scrollTo(0, document.body.scrollHeight);
          
          // Find all buttons
          var buttons = Array.from(document.querySelectorAll('button, input[type="submit"], [role="button"]'));
          var buttonInfo = buttons.map(b => ({
            text: b.textContent.trim().substring(0, 50),
            type: b.type || 'button',
            disabled: b.disabled
          }));
          
          // Find a submit/next/continue button
          var submitBtn = buttons.find(b => 
            /submit|next|continue|create|register|sign up/i.test(b.textContent)
          );
          
          if (submitBtn && !submitBtn.disabled) {
            submitBtn.click();
            return 'CLICKED: ' + submitBtn.textContent.trim();
          }
          
          return 'BUTTONS: ' + JSON.stringify(buttonInfo);
        })()
      `
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  console.log('Result:', JSON.stringify(result, null, 2));
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
