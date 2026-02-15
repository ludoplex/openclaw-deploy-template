const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

ws.on('open', () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: `
        (function() {
          // Get all rows that look like radio options
          var rows = Array.from(document.querySelectorAll('div, label, li')).filter(el => {
            var text = el.textContent.trim();
            return text === 'Build and run AI or machine learning models';
          });
          
          if (rows.length > 0) {
            rows[0].click();
            return 'CLICKED exact match: ' + rows[0].tagName;
          }
          
          // Try finding radio inputs
          var radios = document.querySelectorAll('[type="radio"], [role="radio"]');
          console.log('Found radios:', radios.length);
          
          // Click the 5th option (AI/ML is the 5th in the list)
          if (radios.length >= 5) {
            radios[4].click();
            return 'CLICKED 5th radio';
          }
          
          // Click the label containing AI
          var labels = Array.from(document.querySelectorAll('label, [class*="radio"], [class*="option"]'));
          for (var l of labels) {
            if (l.textContent.includes('AI or machine learning')) {
              l.click();
              return 'CLICKED label: ' + l.textContent.substring(0, 40);
            }
          }
          
          return 'NOT_FOUND, radios: ' + radios.length;
        })()
      `
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  console.log('Result:', result.result?.result?.value || JSON.stringify(result));
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => { console.error('Error:', err.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 10000);
