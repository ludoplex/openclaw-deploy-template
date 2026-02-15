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
          var results = {};
          
          // Check for error messages
          var errors = document.querySelectorAll('[class*="error"], [role="alert"], [aria-invalid="true"]');
          results.errors = Array.from(errors).map(e => e.textContent.trim().substring(0, 100));
          
          // Check form validity
          var form = document.querySelector('form');
          if (form) {
            results.formValid = form.checkValidity();
          }
          
          // Check input values
          var inputs = document.querySelectorAll('input');
          results.inputs = Array.from(inputs).map(i => ({
            name: i.name || i.id || i.placeholder,
            value: i.value,
            valid: i.validity?.valid
          }));
          
          // Check button state
          var addBtn = Array.from(document.querySelectorAll('button')).find(b => 
            b.textContent.includes('Add billing')
          );
          if (addBtn) {
            results.buttonDisabled = addBtn.disabled;
            results.buttonText = addBtn.textContent.trim();
          }
          
          // Check current URL
          results.url = window.location.href;
          
          return JSON.stringify(results, null, 2);
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
