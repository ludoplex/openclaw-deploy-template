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
          // Get all visible text content
          var bodyText = document.body.innerText;
          
          // Look for messages, alerts, notices
          var alerts = document.querySelectorAll('[role="alert"], .alert, .error, .success, .message, .notice');
          
          // Look for submit buttons (hidden or visible)
          var allButtons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.textContent.trim(),
            type: b.type,
            disabled: b.disabled,
            hidden: b.hidden || getComputedStyle(b).display === 'none',
            className: b.className.substring(0, 50)
          }));
          
          // Check for any stepper/progress indicator
          var stepper = document.querySelector('[class*="step"], [class*="progress"], [role="progressbar"]');
          
          // Get full page visible text (truncated)
          var visibleText = bodyText.substring(0, 1000);
          
          return JSON.stringify({
            alerts: alerts.length,
            buttons: allButtons,
            hasStepper: !!stepper,
            visibleText: visibleText
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
