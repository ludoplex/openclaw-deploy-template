const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

let messageId = 1;

ws.on('open', () => {
  console.log('Connected to CDP');
  
  // First, click the country dropdown to open it
  ws.send(JSON.stringify({
    id: messageId++,
    method: 'Runtime.evaluate',
    params: {
      expression: `
        (function() {
          // Find the country dropdown/combobox
          var countryDropdown = document.querySelector('[aria-label*="country" i], [data-testid*="country" i], select[name*="country" i]');
          
          if (!countryDropdown) {
            // Try finding by text content
            var elements = Array.from(document.querySelectorAll('[role="combobox"], .select, select'));
            countryDropdown = elements.find(e => e.textContent.includes('Select your country') || e.textContent.includes('country'));
          }
          
          if (!countryDropdown) {
            // Try the div with "Select your country" text
            countryDropdown = Array.from(document.querySelectorAll('div')).find(d => 
              d.textContent.trim() === 'Select your country'
            );
            if (countryDropdown) {
              countryDropdown = countryDropdown.closest('[role="combobox"], [tabindex]') || countryDropdown;
            }
          }
          
          if (countryDropdown) {
            countryDropdown.click();
            return 'CLICKED: ' + countryDropdown.outerHTML.substring(0, 150);
          }
          
          // Debug: list all comboboxes and selects
          var combos = Array.from(document.querySelectorAll('[role="combobox"], select, [aria-haspopup="listbox"]')).map(c => 
            c.tagName + ':' + c.textContent.trim().substring(0, 30)
          );
          return 'NOT_FOUND: ' + combos.join(' | ');
        })()
      `
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  console.log('Result:', result.result?.result?.value || JSON.stringify(result));
  
  if (result.id === 1 && result.result?.result?.value?.startsWith('CLICKED')) {
    // Dropdown opened, wait and then select United States
    setTimeout(() => {
      ws.send(JSON.stringify({
        id: messageId++,
        method: 'Runtime.evaluate',
        params: {
          expression: `
            (function() {
              // Wait a moment for dropdown to render
              var options = document.querySelectorAll('[role="option"], li, option');
              var usOption = Array.from(options).find(o => 
                o.textContent.includes('United States') || o.textContent.includes('USA')
              );
              
              if (usOption) {
                usOption.click();
                return 'SELECTED: United States';
              }
              
              // Try typing in search
              var searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
              if (searchInput) {
                searchInput.value = 'United States';
                searchInput.dispatchEvent(new Event('input', {bubbles: true}));
                return 'TYPED_SEARCH: United States';
              }
              
              return 'OPTION_NOT_FOUND: ' + Array.from(options).slice(0, 5).map(o => o.textContent.trim().substring(0, 20)).join(', ');
            })()
          `
        }
      }));
    }, 500);
  } else if (result.id === 2) {
    ws.close();
    process.exit(0);
  }
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
