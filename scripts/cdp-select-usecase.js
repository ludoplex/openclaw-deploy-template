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
          // Find the AI/ML option
          var options = document.querySelectorAll('[role="radio"], input[type="radio"], label');
          var aiOption = Array.from(document.querySelectorAll('*')).find(el => 
            el.textContent.includes('AI or machine learning') && el.querySelector('input, [role="radio"]')
          );
          
          if (!aiOption) {
            // Try finding the radio button directly
            var radios = document.querySelectorAll('input[type="radio"]');
            for (var r of radios) {
              var label = r.closest('label') || r.parentElement;
              if (label && label.textContent.includes('AI or machine learning')) {
                r.click();
                return 'CLICKED radio: AI/ML';
              }
            }
            
            // Try clicking the div containing the text
            var divs = Array.from(document.querySelectorAll('div')).filter(d => 
              d.textContent.includes('Build and run AI')
            );
            if (divs.length > 0) {
              divs[0].click();
              return 'CLICKED div: ' + divs[0].textContent.substring(0, 50);
            }
          } else {
            aiOption.click();
            return 'CLICKED: ' + aiOption.textContent.substring(0, 50);
          }
          
          return 'NOT_FOUND';
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
