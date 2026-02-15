const puppeteer = require('puppeteer-core');

async function main() {
  console.log('Connecting to existing Chromium...');
  
  const browser = await puppeteer.connect({
    browserURL: 'http://127.0.0.1:18801',
    defaultViewport: null
  });
  
  console.log('Connected!');
  
  const page = await browser.newPage();
  await page.goto('https://my.vultr.com/signup/', { waitUntil: 'networkidle2', timeout: 30000 });
  
  console.log('Page loaded');
  
  // Screenshot
  await page.screenshot({ path: 'C:/Users/user/.openclaw/workspace/vultr-page.png', fullPage: true });
  console.log('Screenshot saved to vultr-page.png');
  
  // Get page HTML to understand structure
  const html = await page.content();
  const fs = require('fs');
  fs.writeFileSync('C:/Users/user/.openclaw/workspace/vultr-page.html', html);
  console.log('HTML saved to vultr-page.html');
  
  // Get all input fields
  const inputs = await page.$$eval('input', els => els.map(e => ({
    name: e.name,
    id: e.id,
    type: e.type,
    placeholder: e.placeholder
  })));
  console.log('Input fields:', JSON.stringify(inputs, null, 2));
  
  // Get all form elements
  const forms = await page.$$eval('form', els => els.map(e => ({
    id: e.id,
    action: e.action,
    method: e.method
  })));
  console.log('Forms:', JSON.stringify(forms, null, 2));
  
  // Check page title
  const title = await page.title();
  console.log('Title:', title);
  
  // Check URL (in case of redirect)
  const url = page.url();
  console.log('Current URL:', url);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
