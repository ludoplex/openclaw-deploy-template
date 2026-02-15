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
        (async function() {
          var results = [];
          
          // Fill street address
          var inputs = Array.from(document.querySelectorAll('input'));
          var streetInput = inputs.find(i => i.placeholder && i.placeholder.includes('Baker'));
          if (streetInput) {
            streetInput.focus();
            streetInput.value = '977 Gilchrist St';
            streetInput.dispatchEvent(new Event('input', {bubbles: true}));
            streetInput.dispatchEvent(new Event('change', {bubbles: true}));
            results.push('street: OK');
          }
          
          // Fill postal code
          var postalInput = inputs.find(i => i.placeholder && i.placeholder.includes('93100'));
          if (postalInput) {
            postalInput.focus();
            postalInput.value = '82201';
            postalInput.dispatchEvent(new Event('input', {bubbles: true}));
            postalInput.dispatchEvent(new Event('change', {bubbles: true}));
            results.push('postal: OK');
          }
          
          // Fill city
          var cityInput = inputs.find(i => i.placeholder && i.placeholder.includes('Paris'));
          if (cityInput) {
            cityInput.focus();
            cityInput.value = 'Wheatland';
            cityInput.dispatchEvent(new Event('input', {bubbles: true}));
            cityInput.dispatchEvent(new Event('change', {bubbles: true}));
            results.push('city: OK');
          }
          
          // Now select Region (Wyoming)
          await new Promise(r => setTimeout(r, 200));
          
          var regionCombobox = document.querySelector('[aria-label*="region" i] [role="combobox"], [data-testid*="region" i] [role="combobox"]');
          if (!regionCombobox) {
            var allComboboxes = Array.from(document.querySelectorAll('[role="combobox"]'));
            regionCombobox = allComboboxes.find(c => c.textContent.includes('Region'));
          }
          
          if (regionCombobox) {
            regionCombobox.focus();
            regionCombobox.click();
            results.push('region dropdown clicked');
            
            await new Promise(r => setTimeout(r, 300));
            
            var listbox = document.querySelector('[role="listbox"]');
            if (listbox) {
              var options = listbox.querySelectorAll('[role="option"]');
              var wyOption = Array.from(options).find(o => 
                o.textContent.toLowerCase().includes('wyoming')
              );
              
              if (wyOption) {
                wyOption.click();
                results.push('region: Wyoming selected');
              } else {
                results.push('region: Wyoming not found in ' + options.length + ' options');
              }
            }
          } else {
            results.push('region combobox not found');
          }
          
          return results.join(', ');
        })()
      `,
      awaitPromise: true
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
}, 20000);
