const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

ws.on('open', () => {
  console.log('Connected to CDP');
  
  // Click the combobox and find options
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: `
        (async function() {
          // Find the country combobox by its aria-label
          var combobox = document.querySelector('[role="combobox"][aria-label="countryCode" i]');
          if (!combobox) {
            combobox = document.querySelector('[data-testid*="country" i] [role="combobox"]');
          }
          if (!combobox) {
            // Try finding by text
            var allComboboxes = document.querySelectorAll('[role="combobox"]');
            combobox = Array.from(allComboboxes).find(c => c.textContent.includes('Select your country'));
          }
          
          if (!combobox) {
            return 'COMBOBOX_NOT_FOUND';
          }
          
          // Click to open
          combobox.focus();
          combobox.click();
          
          // Wait for dropdown to open
          await new Promise(r => setTimeout(r, 300));
          
          // Now look for the listbox
          var listbox = document.querySelector('[role="listbox"]');
          if (!listbox) {
            return 'LISTBOX_NOT_FOUND after click';
          }
          
          // Find United States option
          var options = listbox.querySelectorAll('[role="option"]');
          var usOption = Array.from(options).find(o => 
            o.textContent.trim().toLowerCase().includes('united states')
          );
          
          if (usOption) {
            usOption.click();
            return 'SELECTED: United States';
          }
          
          // If not found, try scrolling through options
          var optionTexts = Array.from(options).slice(0, 10).map(o => o.textContent.trim());
          return 'OPTIONS: ' + optionTexts.join(', ');
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
}, 15000);
