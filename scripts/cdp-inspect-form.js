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
          // Get all form-like containers
          var forms = document.querySelectorAll('form, [role="form"], .form');
          
          // Get all inputs
          var inputs = Array.from(document.querySelectorAll('input, select, textarea')).map(i => ({
            tag: i.tagName,
            type: i.type,
            name: i.name,
            id: i.id,
            placeholder: i.placeholder,
            value: i.value ? i.value.substring(0, 30) : '',
            disabled: i.disabled
          }));
          
          // Get all clickable elements
          var clickables = Array.from(document.querySelectorAll('button, a, [role="button"], input[type="submit"]')).map(e => ({
            tag: e.tagName,
            text: e.textContent.trim().substring(0, 50),
            href: e.href ? e.href.substring(0, 50) : '',
            disabled: e.disabled
          }));
          
          // Get body innerHTML length
          var bodyLength = document.body.innerHTML.length;
          
          // Check for loading indicators
          var loading = document.querySelector('[class*="loading"], [class*="spinner"], [aria-busy="true"]');
          
          return JSON.stringify({
            forms: forms.length,
            inputs: inputs,
            clickables: clickables,
            bodyLength: bodyLength,
            isLoading: !!loading,
            url: window.location.href
          }, null, 2);
        })()
      `
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  if (result.result && result.result.result) {
    console.log('Page state:', result.result.result.value);
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
