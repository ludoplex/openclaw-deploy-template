const puppeteer = require('puppeteer-core');

const EMAIL = 'theander.project@gmail.com';
const PASSWORD = 'OpenClaw2026!Vultr'; // Strong password for new account

async function main() {
  console.log('Connecting to existing Chromium...');
  
  const browser = await puppeteer.connect({
    browserURL: 'http://127.0.0.1:18801',
    defaultViewport: null
  });
  
  console.log('Connected! Opening Vultr signup...');
  
  const page = await browser.newPage();
  await page.goto('https://my.vultr.com/signup/', { waitUntil: 'networkidle2' });
  
  console.log('Page loaded, filling form...');
  
  // Wait for form to load
  await page.waitForSelector('input[name="email"]', { timeout: 10000 });
  
  // Fill email
  await page.type('input[name="email"]', EMAIL);
  console.log('Email entered');
  
  // Fill password
  await page.type('input[name="password"]', PASSWORD);
  console.log('Password entered');
  
  // Screenshot for debugging
  await page.screenshot({ path: 'C:/Users/user/.openclaw/workspace/vultr-signup.png' });
  console.log('Screenshot saved');
  
  // Get page content
  const title = await page.title();
  console.log('Page title:', title);
  
  // Check for CAPTCHA
  const hasCaptcha = await page.$('iframe[src*="recaptcha"]');
  if (hasCaptcha) {
    console.log('WARNING: CAPTCHA detected - manual intervention required');
  }
  
  // Find signup button
  const submitBtn = await page.$('button[type="submit"]');
  if (submitBtn) {
    console.log('Submit button found');
  }
  
  console.log('Form filled. Review screenshot and decide next steps.');
  
  // Don't disconnect - keep browser open
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
