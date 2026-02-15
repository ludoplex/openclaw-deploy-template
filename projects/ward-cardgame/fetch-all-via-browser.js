/**
 * Fetch ALL cards using browser context (includes auth cookies)
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const GALLERY_ID = '374b0062-ad2c-4a70-bda1-2c2d7ba81657';
const EXTERNAL_ID = '2e50edb0-be16-4154-a2a3-676d7459f884';

function parseCard(item) {
  const desc = item.description || '';
  const parseField = (fieldName) => {
    const re = new RegExp(`${fieldName}:\\s*([^\\n]+)`);
    const m = desc.match(re);
    return m ? m[1].trim() : null;
  };
  
  return {
    id: item.id,
    title: item.title,
    imageUrl: item.mediaUrl,
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

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Load page to get session
  console.log('Loading page to establish session...');
  await page.goto('https://www.ward-cardgame.com/card-library-generation-1-edition-2', {
    waitUntil: 'domcontentloaded'
  });
  await page.waitForTimeout(3000);
  
  // Fetch all pages via browser
  const allCards = [];
  let offset = 0;
  const total = 151;
  
  while (offset < total) {
    console.log(`Fetching offset ${offset}...`);
    
    const url = `https://www.ward-cardgame.com/pro-gallery-webapp/v1/galleries/${GALLERY_ID}?galleryId=${GALLERY_ID}&offset=${offset}&limit=25&externalId=${EXTERNAL_ID}&state=PUBLISHED`;
    
    const data = await page.evaluate(async (url) => {
      const resp = await fetch(url);
      return resp.json();
    }, url);
    
    const items = data.gallery?.items || [];
    console.log(`  Got ${items.length} items`);
    
    for (const item of items) {
      allCards.push(parseCard(item));
    }
    
    offset += 25;
    await page.waitForTimeout(300);
  }
  
  await browser.close();
  
  // Save
  const output = {
    extractedAt: new Date().toISOString(),
    source: 'ward-cardgame.com',
    method: 'Wix Pro Gallery API via browser',
    galleryId: GALLERY_ID,
    totalCards: allCards.length,
    cards: allCards
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'all-cards-complete.json'),
    JSON.stringify(output, null, 2)
  );
  
  console.log(`\n✅ Extracted ${allCards.length} cards!`);
}

main().catch(console.error);
