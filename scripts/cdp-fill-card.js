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
    // Check for iframes (Stripe uses iframes)
    let result = await sendAndWait('Runtime.evaluate', {
      expression: `
        var iframes = document.querySelectorAll('iframe');
        var inputs = document.querySelectorAll('input');
        'Iframes: ' + iframes.length + ', Inputs: ' + inputs.length + 
        ', Input names: ' + Array.from(inputs).map(i => i.name || i.placeholder || i.id).join(', ');
      `
    });
    console.log('Page structure:', result.result?.result?.value);

    // Focus card number input (might be in iframe or direct)
    result = await sendAndWait('Runtime.evaluate', {
      expression: `
        var cardInput = document.querySelector('input[name*="card"], input[placeholder*="1234"], input[autocomplete="cc-number"]');
        if (!cardInput) {
          cardInput = Array.from(document.querySelectorAll('input')).find(i => 
            i.placeholder && i.placeholder.includes('1234')
          );
        }
        if (cardInput) {
          cardInput.focus();
          cardInput.click();
          return 'FOCUSED card input';
        }
        return 'Card input not found';
      `
    });
    console.log('Card focus:', result.result?.result?.value);

    if (result.result?.result?.value === 'FOCUSED card input') {
      console.log('Typing card number...');
      await typeText('4232233106941908');
      
      // Tab to expiry
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
      await new Promise(r => setTimeout(r, 100));
      
      console.log('Typing expiry...');
      await typeText('0229');
      
      // Tab to CVV
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
      await new Promise(r => setTimeout(r, 100));
      
      console.log('Typing CVV...');
      await typeText('125');
      
      // Tab to name
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
      await new Promise(r => setTimeout(r, 100));
      
      console.log('Typing name...');
      await typeText('Vincent Anderson');
      
      console.log('Card details entered!');
    }
    
  } catch (e) {
    console.error('Error:', e);
  }
  
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => { console.error('Error:', err.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 60000);
