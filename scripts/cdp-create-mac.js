const WebSocket = require('ws');

const targetId = 'A22E9E4B6D58F0C40B1EFE9C7E0C0ABE';
const ws = new WebSocket(`ws://127.0.0.1:18801/devtools/page/${targetId}`);

ws.on('open', () => {
  // Try direct URL to create Mac mini
  ws.send(JSON.stringify({
    id: 1,
    method: 'Page.navigate',
    params: {
      url: 'https://console.scaleway.com/apple-silicon/servers/create'
    }
  }));
});

ws.on('message', (data) => {
  const result = JSON.parse(data);
  console.log('Result:', JSON.stringify(result));
  setTimeout(() => {
    ws.close();
    process.exit(0);
  }, 2000);
});

ws.on('error', (err) => { console.error('Error:', err.message); process.exit(1); });
setTimeout(() => { ws.close(); process.exit(0); }, 10000);
