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
          var emailInput = document.querySelector('input[type="email"], input[name*="email"], input[placeholder*="email" i]');
          if (emailInput) {
            emailInput.focus();
            emailInput.value = 'theander.project@gmail.com';
            emailInput.dispatchEvent(new Event('input', {bubbles: true}));
            emailInput.dispatchEvent(new Event('change', {bubbles: true}));
            return 'FILLED: ' + emailInput.outerHTML.substring(0, 100);
          }
          var allInputs = Array.from(document.querySelectorAll('input')).map(i => i.type + ':' + i.name + ':' + i.placeholder);
          return 'NOT_FOUND: ' + allInputs.join(', ');
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
