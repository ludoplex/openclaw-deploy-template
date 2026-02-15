/**
 * Intercept Wix Pro Gallery network requests to capture ALL card data
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const capturedItems = [];
  
  // Intercept all responses
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('gallery') || url.includes('items') || url.includes('pro-gallery')) {
      try {
        const text = await response.text();
        if (text.includes('Card Name') || text.includes('itemId')) {
          console.log('Captured:', url.substring(0, 80));
          capturedItems.push({ url, data: text.substring(0, 2000) });
        }
      } catch (e) {}
    }
  });
  
  console.log('Loading page...');
  await page.goto('https://www.ward-cardgame.com/card-library-generation-1-edition-2', {
    waitUntil: 'domcontentloaded'
  });
  
  await page.waitForTimeout(3000);
  
  // Scroll to trigger lazy loading
  console.log('Scrolling to trigger loads...');
  for (let i = 0; i < 30; i++) {
    await page.evaluate(() => window.scrollBy(0, 500));
    await page.waitForTimeout(200);
  }
  
  // Try scrolling the gallery container
  const gallery = await page.$('.pro-gallery-margin-container');
  if (gallery) {
    for (let i = 0; i < 50; i++) {
      await gallery.evaluate(el => el.scrollTop += 300);
      await page.waitForTimeout(100);
    }
  }
  
  await page.waitForTimeout(3000);
  
  console.log(`\nCaptured ${capturedItems.length} gallery-related responses`);
  
  if (capturedItems.length > 0) {
    fs.writeFileSync(
      path.join(__dirname, 'network-captures.json'),
      JSON.stringify(capturedItems, null, 2)
    );
    console.log('Saved to network-captures.json');
  }
  
  await browser.close();
}

main().catch(console.error);
