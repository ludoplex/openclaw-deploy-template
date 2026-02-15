/**
 * Ward TCG Card Extractor
 * Extracts all card data from ward-cardgame.com gallery pages
 * 
 * The Wix Pro Gallery embeds card data in inline scripts as:
 *   galleryData.items[].metaData.description
 * 
 * Run with: node extract-cards.js
 * Requires: playwright (npm install playwright)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PAGES = [
  { name: 'gen1-ed2', url: 'https://www.ward-cardgame.com/card-library-generation-1-edition-2' },
  { name: 'gen2', url: 'https://www.ward-cardgame.com/card-library-generation-2' },
  { name: 'gen3', url: 'https://www.ward-cardgame.com/gen-3' },
  { name: 'promo', url: 'https://www.ward-cardgame.com/card-library-promo' },
  { name: 'gen1-remastered', url: 'https://www.ward-cardgame.com/gen-1-ed-3' },
  { name: 'gen2-remastered', url: 'https://www.ward-cardgame.com/gen-2-ed-2' },
];

async function extractCardsFromPage(page) {
  return await page.evaluate(() => {
    const scripts = document.querySelectorAll('script');
    const allItems = [];
    
    for (let s of scripts) {
      const t = s.textContent || '';
      const regex = /"items":\s*\[/g;
      let match;
      
      while ((match = regex.exec(t)) !== null) {
        let start = match.index + match[0].length - 1;
        let bracketCount = 0;
        let end = start;
        
        for (let i = start; i < t.length && i < start + 500000; i++) {
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
            allItems.push(...arr);
          }
        } catch(e) {}
      }
    }
    
    return allItems.map(item => {
      const desc = item.metaData?.description || '';
      const parseField = (fieldName) => {
        const regex = new RegExp(`${fieldName}:\\s*([^\\n]+)`);
        const match = desc.match(regex);
        return match ? match[1].trim() : null;
      };
      
      return {
        id: item.itemId,
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
        rawDescription: desc,
        imageUrl: item.mediaUrl || item.metaData?.link?.url || null
      };
    });
  });
}

async function main() {
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  const allCards = {};
  
  for (const { name, url } of PAGES) {
    console.log(`\nFetching ${name}: ${url}`);
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000); // Let JS hydrate
      
      const cards = await extractCardsFromPage(page);
      allCards[name] = cards;
      console.log(`  Found ${cards.length} cards`);
      
      // Save individual generation file
      fs.writeFileSync(
        path.join(__dirname, `cards-${name}.json`),
        JSON.stringify(cards, null, 2)
      );
    } catch (err) {
      console.error(`  Error: ${err.message}`);
      allCards[name] = [];
    }
  }
  
  // Save combined file
  const combined = {
    extractedAt: new Date().toISOString(),
    source: 'ward-cardgame.com',
    generations: allCards,
    totalCards: Object.values(allCards).reduce((sum, arr) => sum + arr.length, 0)
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'all-cards.json'),
    JSON.stringify(combined, null, 2)
  );
  
  console.log(`\n✅ Done! Total cards: ${combined.totalCards}`);
  console.log(`Output: ${path.join(__dirname, 'all-cards.json')}`);
  
  await browser.close();
}

main().catch(console.error);
