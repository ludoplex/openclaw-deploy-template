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
          var results = [];
          
          // Fill street address
          var streetInput = document.querySelector('input[name*="street" i], input[placeholder*="street" i], input[id*="street" i]');
          if (!streetInput) {
            var inputs = Array.from(document.querySelectorAll('input'));
            streetInput = inputs.find(i => i.placeholder && i.placeholder.toLowerCase().includes('baker'));
          }
          if (streetInput) {
            streetInput.focus();
            streetInput.value = '977 Gilchrist St';
            streetInput.dispatchEvent(new Event('input', {bubbles: true}));
            streetInput.dispatchEvent(new Event('change', {bubbles: true}));
            results.push('street: OK');
          } else {
            results.push('street: NOT_FOUND');
          }
          
          // Fill postal code
          var postalInput = document.querySelector('input[name*="postal" i], input[name*="zip" i], input[placeholder*="postal" i], input[placeholder*="93100" i]');
          if (postalInput) {
            postalInput.focus();
            postalInput.value = '82201';
            postalInput.dispatchEvent(new Event('input', {bubbles: true}));
            postalInput.dispatchEvent(new Event('change', {bubbles: true}));
            results.push('postal: OK');
          } else {
            results.push('postal: NOT_FOUND');
          }
          
          // Fill city
          var cityInput = document.querySelector('input[name*="city" i], input[placeholder*="city" i], input[placeholder*="Paris" i]');
          if (cityInput) {
            cityInput.focus();
            cityInput.value = 'Wheatland';
            cityInput.dispatchEvent(new Event('input', {bubbles: true}));
            cityInput.dispatchEvent(new Event('change', {bubbles: true}));
            results.push('city: OK');
          } else {
            results.push('city: NOT_FOUND');
          }
          
          return results.join(', ');
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
