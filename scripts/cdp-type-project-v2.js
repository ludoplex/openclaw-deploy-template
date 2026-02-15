const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

let msgId = 1;

async function sendAndWait(method, params) {
  return new Promise(resolve => {
    const id = msgId++;
    const handler = (data) => {
      const result = JSON.parse(data);
      if (result.id === id) {
        ws.off('message', handler);
        resolve(result);
      }
    };
    ws.on('message', handler);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function typeText(text) {
  for (const char of text) {
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: char, text: char });
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: char });
    await new Promise(r => setTimeout(r, 30));
  }
}

ws.on('open', async () => {
  try {
    // Click on the project name input to focus it
    await sendAndWait('Runtime.evaluate', {
      expression: `
        var input = document.querySelector('input');
        if (input) {
          input.focus();
          input.click();
          // Clear the value
          input.value = '';
          input.dispatchEvent(new Event('input', {bubbles: true}));
        }
        input ? 'cleared and focused' : 'not found';
      `
    });
    
    console.log('Typing project name...');
    await typeText('OpenClaw');
    
    await new Promise(r => setTimeout(r, 300));
    
    // Check button state
    const result = await sendAndWait('Runtime.evaluate', {
      expression: `
        var btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Continue'));
        var input = document.querySelector('input');
        'Input value: ' + (input?.value || 'none') + ', Button disabled: ' + (btn?.disabled || 'not found');
      `
    });
    console.log('State:', result.result?.result?.value);
    
  } catch (e) {
    console.error('Error:', e);
  }
  
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => { console.error('Error:', err.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 30000);
