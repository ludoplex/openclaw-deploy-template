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
          // Find all elements that look like dropdowns or selects
          var selects = document.querySelectorAll('select, [role="listbox"], [role="combobox"], [aria-haspopup="listbox"]');
          
          // Find elements with "Account type" or "Personal project" text
          var accountType = Array.from(document.querySelectorAll('*')).find(e => 
            e.textContent.includes('Personal project') && e.children.length < 5
          );
          
          // Find any divs that look clickable (role="button" or tabindex)
          var clickableDivs = Array.from(document.querySelectorAll('div[role="button"], div[tabindex], div[aria-haspopup]')).map(d => ({
            text: d.textContent.trim().substring(0, 50),
            role: d.getAttribute('role'),
            ariaExpanded: d.getAttribute('aria-expanded'),
            className: d.className.substring(0, 50)
          }));
          
          // Get the form's full HTML for inspection
          var formHtml = document.querySelector('form') ? document.querySelector('form').innerHTML.substring(0, 3000) : 'no form';
          
          return JSON.stringify({
            selects: selects.length,
            accountTypeText: accountType ? accountType.outerHTML.substring(0, 200) : 'not found',
            clickableDivs: clickableDivs,
            formPreview: formHtml.substring(0, 1500)
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
