// Save extracted Gen 2 card data
const fs = require('fs');
const { chromium } = require('playwright');

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  console.log('Navigating to Gen 2 card library...');
  await page.goto('https://www.ward-cardgame.com/card-library-generation-2', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  console.log('Scrolling to load all cards...');
  let lastCount = 0;
  let sameCount = 0;
  for (let i = 0; i < 50; i++) {
    await page.evaluate(() => window.scrollBy(0, 1000));
    await page.waitForTimeout(300);
    const count = await page.evaluate(() => document.querySelectorAll('[data-hook="item-container"]').length);
    if (count === lastCount) {
      sameCount++;
      if (sameCount > 5) break;
    } else {
      sameCount = 0;
      lastCount = count;
    }
  }
  console.log(`Loaded ${lastCount} cards`);
  
  console.log('Extracting card data...');
  const cards = await page.evaluate(() => {
    const results = [];
    const fields = ['Card Name:', 'Card Type:', 'Card Number:', 'Rarity:', 'Race:', 'Background:', 'Flavor Text:', 'Armor Level:', 'Speed:', 'Health Points:', 'Attack Name:', 'Attack Dice:', 'Damage Dice:', 'Modifier:', 'Other Attributes:', 'Affects Boss:', 'Extended Effect Description:'];
    const keyMap = {
      'Card Name': 'cardName', 'Card Type': 'cardType', 'Card Number': 'cardNumber',
      'Rarity': 'rarity', 'Race': 'race', 'Background': 'background',
      'Flavor Text': 'flavorText', 'Armor Level': 'armorLevel', 'Speed': 'speed',
      'Health Points': 'healthPoints', 'Attack Name': 'attackName',
      'Attack Dice': 'attackDice', 'Damage Dice': 'attackDice', 'Modifier': 'modifier',
      'Other Attributes': 'otherAttributes', 'Affects Boss': 'affectsBoss',
      'Extended Effect Description': 'extendedEffectDescription'
    };
    
    document.querySelectorAll('[data-hook="item-container"]').forEach((item) => {
      const title = item.querySelector('[data-hook="item-title"]')?.textContent?.trim() || '';
      const descEl = item.querySelector('[data-hook="item-description"]');
      if (!descEl) return;
      
      const lines = Array.from(descEl.querySelectorAll('p, span, div')).map(el => el.textContent.trim()).filter(Boolean);
      const card = { displayTitle: title };
      let currentKey = null;
      let currentValue = '';
      
      for (const line of lines) {
        let foundKey = false;
        for (const field of fields) {
          if (line.startsWith(field)) {
            if (currentKey && keyMap[currentKey]) {
              card[keyMap[currentKey]] = currentValue.trim();
            }
            currentKey = field.replace(':', '');
            currentValue = line.substring(field.length).trim();
            foundKey = true;
            break;
          }
        }
        if (!foundKey && currentKey) {
          currentValue += ' ' + line;
        }
      }
      if (currentKey && keyMap[currentKey]) {
        card[keyMap[currentKey]] = currentValue.trim();
      }
      results.push(card);
    });
    return results;
  });
  
  await browser.close();
  
  console.log(`Extracted ${cards.length} cards`);
  fs.writeFileSync('./gen2-all-cards-complete.json', JSON.stringify(cards, null, 2));
  console.log('Saved to gen2-all-cards-complete.json');
}

main().catch(console.error);
