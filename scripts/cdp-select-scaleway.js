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
          // Find and click the Scaleway option (not Dedibox)
          var cards = document.querySelectorAll('[class*="card"], div[role="button"], button');
          
          // Look for element containing "Scaleway" text but not "Dedibox"
          var scalewayCard = Array.from(document.querySelectorAll('*')).find(el => {
            var text = el.textContent;
            var childCount = el.children.length;
            return text.includes('Scaleway') && 
                   text.includes('cloud computing') && 
                   !text.includes('Dedibox') &&
                   childCount > 2 && childCount < 20;
          });
          
          if (!scalewayCard) {
            // Try finding the card container on the right side
            var allDivs = Array.from(document.querySelectorAll('div'));
            scalewayCard = allDivs.find(d => {
              var t = d.textContent.trim();
              return t.startsWith('Scaleway') && t.includes('cloud computing');
            });
          }
          
          if (scalewayCard) {
            // Find the closest clickable element
            var clickable = scalewayCard.closest('a, button, [role="button"], [tabindex]') || scalewayCard;
            clickable.click();
            return 'CLICKED Scaleway: ' + scalewayCard.textContent.substring(0, 100);
          }
          
          // Debug: list all cards
          var cardTexts = Array.from(document.querySelectorAll('div')).filter(d => 
            d.textContent.includes('Scaleway') || d.textContent.includes('Dedibox')
          ).slice(0, 5).map(d => d.tagName + ':' + d.textContent.substring(0, 50));
          
          return 'NOT_FOUND: ' + cardTexts.join(' | ');
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
