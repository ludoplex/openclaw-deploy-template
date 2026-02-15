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
    await new Promise(r => setTimeout(r, 40));
  }
}

async function clickAt(x, y) {
  await sendAndWait('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
  await sendAndWait('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left' });
}

ws.on('open', async () => {
  try {
    // Get positions of card input areas
    let result = await sendAndWait('Runtime.evaluate', {
      expression: `
        var cardLabel = Array.from(document.querySelectorAll('*')).find(e => e.textContent.trim() === 'Card number');
        var expiryLabel = Array.from(document.querySelectorAll('*')).find(e => e.textContent.trim() === 'Expiration date');
        var cvvLabel = Array.from(document.querySelectorAll('*')).find(e => e.textContent.includes('CVV'));
        var nameInput = document.querySelector('input[name="cardHolder"], input[placeholder="John Doe"]');
        
        var iframes = document.querySelectorAll('iframe');
        var positions = [];
        
        for (var iframe of iframes) {
          var rect = iframe.getBoundingClientRect();
          positions.push({
            src: iframe.src?.substring(0, 50) || 'no src',
            x: rect.x + rect.width/2,
            y: rect.y + rect.height/2,
            width: rect.width,
            height: rect.height
          });
        }
        
        JSON.stringify({
          iframeCount: iframes.length,
          positions: positions.slice(0, 5),
          nameInput: nameInput ? { x: nameInput.getBoundingClientRect().x, y: nameInput.getBoundingClientRect().y } : null
        });
      `
    });
    console.log('Layout:', result.result?.result?.value);
    
    const layout = JSON.parse(result.result?.result?.value);
    
    // Find the card number iframe (usually first Stripe iframe)
    const stripeIframes = layout.positions.filter(p => p.src.includes('stripe') || p.width > 100);
    console.log('Stripe iframes:', stripeIframes.length);
    
    if (stripeIframes.length > 0) {
      // Click on card number field (first stripe iframe)
      const cardPos = stripeIframes[0];
      console.log('Clicking card field at', cardPos.x, cardPos.y);
      await clickAt(cardPos.x, cardPos.y);
      await new Promise(r => setTimeout(r, 300));
      
      console.log('Typing card number...');
      await typeText('4232233106941908');
      
      // Tab to expiry
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
      await new Promise(r => setTimeout(r, 200));
      
      console.log('Typing expiry...');
      await typeText('0229');
      
      // Tab to CVV
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
      await new Promise(r => setTimeout(r, 200));
      
      console.log('Typing CVV...');
      await typeText('125');
      
      // Tab to name
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab' });
      await sendAndWait('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab' });
      await new Promise(r => setTimeout(r, 200));
      
      console.log('Typing name...');
      await typeText('Vincent Anderson');
      
      console.log('Done!');
    }
    
  } catch (e) {
    console.error('Error:', e);
  }
  
  ws.close();
  process.exit(0);
});

ws.on('error', (err) => { console.error('Error:', err.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 90000);
