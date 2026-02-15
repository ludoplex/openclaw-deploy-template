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
    await sendAndWait('Input.dispatchKeyEvent', {
      type: 'keyDown',
      key: char,
      text: char
    });
    await sendAndWait('Input.dispatchKeyEvent', {
      type: 'keyUp',
      key: char
    });
    await new Promise(r => setTimeout(r, 20));
  }
}

ws.on('open', async () => {
  console.log('Connected to CDP');
  
  try {
    // First clear and focus the street input
    await sendAndWait('Runtime.evaluate', {
      expression: `
        (function() {
          var inputs = Array.from(document.querySelectorAll('input'));
          var streetInput = inputs.find(i => i.name === 'streetName1');
          if (streetInput) {
            streetInput.focus();
            streetInput.select();
            return 'FOCUSED: street';
          }
          return 'NOT_FOUND';
        })()
      `
    });
    
    console.log('Typing street address...');
    await typeText('977 Gilchrist St');
    
    // Tab to postal code
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
    await new Promise(r => setTimeout(r, 100));
    
    console.log('Typing postal code...');
    await typeText('82201');
    
    // Tab to city
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
    await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
    await new Promise(r => setTimeout(r, 100));
    
    console.log('Typing city...');
    await typeText('Wheatland');
    
    console.log('Done typing!');
    
    // Check button state
    const result = await sendAndWait('Runtime.evaluate', {
      expression: `
        (function() {
          var btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Add billing'));
          return btn ? 'Button disabled: ' + btn.disabled : 'Button not found';
        })()
      `
    });
    console.log('Button state:', result.result?.result?.value);
    
  } catch (e) {
    console.error('Error:', e);
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
  ws.close();
  process.exit(0);
}, 60000);
