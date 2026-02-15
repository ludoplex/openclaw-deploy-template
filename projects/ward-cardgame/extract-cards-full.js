/**
 * Ward TCG Full Card Extractor
 * Uses Playwright to scroll the Wix Pro Gallery and extract ALL cards
 * 
 * Install: npm install playwright
 * Run: node extract-cards-full.js
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PAGES = [
  { name: 'gen1-ed2', url: 'https://www.ward-cardgame.com/card-library-generation-1-edition-2' },
  { name: 'gen2', url: 'https://www.ward-cardgame.com/card-library-generation-2' },
];

function parseCardDescription(desc) {
  const parseField = (fieldName) => {
    const re = new RegExp(`${fieldName}:\\s*([^\\n]+)`);
    const m = desc.match(re);
    return m ? m[1].trim() : null;
  };
  
  return {
    cardName: parseField('Card Name'),
    cardType: parseField('Card Type'),
    cardNumber: parseField('Card Number'),
    rarity: parseField('Rarity'),
    race: parseField('Race'),
    background: parseField('Background'),
    flavorText: parseField('Flavor Text'),
    armorLevel: parseField('Armor Level'),
    speed: parseField('Speed'),
    healthPoints: parseField('Health Points'),
    attackName: parseField('Attack Name'),
    attackDice: parseField('Attack Dice'),
    modifier: parseField('Modifier'),
    otherAttributes: parseField('Other Attributes'),
    affectsBoss: parseField('Affects Boss'),
    extendedEffectDescription: parseField('Extended Effect Description'),
  };
}

async function extractAllCards(page) {
  // Scroll the gallery to trigger lazy loading
  const gallery = await page.$('.pro-gallery-margin-container, .pro-gallery');
  if (gallery) {
    const box = await gallery.boundingBox();
    if (box) {
      // Scroll the gallery container multiple times
      for (let i = 0; i < 50; i++) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.mouse.wheel(0, 500);
        await page.waitForTimeout(200);
      }
    }
  }
  
  // Also scroll the page itself
  for (let i = 0; i < 20; i++) {
    await page.evaluate(() => window.scrollBy(0, 1000));
    await page.waitForTimeout(300);
  }
  
  // Wait for any pending loads
  await page.waitForTimeout(2000);
  
  // Extract all items from the page HTML
  return await page.evaluate(() => {
    const scripts = document.querySelectorAll('script');
    const allItems = [];
    const seenIds = new Set();
    
    for (let s of scripts) {
      const t = s.textContent || '';
      const regex = /"items":\s*\[/g;
      let match;
      
      while ((match = regex.exec(t)) !== null) {
        let start = match.index + match[0].length - 1;
        let bracketCount = 0;
        let end = start;
        
        for (let i = start; i < t.length && i < start + 1000000; i++) {
          if (t[i] === '[') bracketCount++;
          else if (t[i] === ']') {
            bracketCount--;
            if (bracketCount === 0) {
              end = i + 1;
              break;
            }
          }
        }
        
        try {
          const arr = JSON.parse(t.substring(start, end));
          if (arr.length > 0 && arr[0].metaData?.description?.includes('Card Name')) {
            for (const item of arr) {
              if (!seenIds.has(item.itemId)) {
                seenIds.add(item.itemId);
                allItems.push({
                  id: item.itemId,
                  description: item.metaData?.description
                });
              }
            }
          }
        } catch (e) {}
      }
    }
    
    return allItems;
  });
}

async function main() {
  console.log('Launching browser...');
  const browser = await chromium.launch({ 
    headless: true,
  });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });
  const page = await context.newPage();
  
  const allCards = {};
  
  for (const { name, url } of PAGES) {
    console.log(`\nFetching ${name}: ${url}`);
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(5000); // Let gallery hydrate
      
      const items = await extractAllCards(page);
      const cards = items.map(item => ({
        id: item.id,
        ...parseCardDescription(item.description || '')
      }));
      
      allCards[name] = cards;
      console.log(`  Found ${cards.length} cards`);
      
      fs.writeFileSync(
        path.join(__dirname, `cards-${name}-full.json`),
        JSON.stringify(cards, null, 2)
      );
    } catch (err) {
      console.error(`  Error: ${err.message}`);
      allCards[name] = [];
    }
  }
  
  // Save combined
  const combined = {
    extractedAt: new Date().toISOString(),
    source: 'ward-cardgame.com',
    method: 'Playwright scroll extraction',
    generations: allCards,
    totalCards: Object.values(allCards).reduce((sum, arr) => sum + arr.length, 0)
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'all-cards-full.json'),
    JSON.stringify(combined, null, 2)
  );
  
  console.log(`\n✅ Total: ${combined.totalCards} cards`);
  console.log(`Output: ${path.join(__dirname, 'all-cards-full.json')}`);
  
  await browser.close();
}

main().catch(console.error);
