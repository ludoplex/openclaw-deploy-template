// Fetch all Gen 2 Ward cards via Wix Pro Gallery API
// Run with: node --experimental-fetch fetch-gen2-cards.js

const { chromium } = require('playwright');
const fs = require('fs');

const GALLERY_ID = 'f6d3af31-8149-4558-a1e7-bf9b91e634a1';
const COMP_ID = 'comp-lw0x3t30';
const BASE_URL = 'https://www.ward-cardgame.com';
const PAGE_URL = `${BASE_URL}/card-library-generation-2`;

async function parseCardDescription(desc) {
  if (!desc) return {};
  
  const lines = desc.split('\n').filter(l => l.trim());
  const card = {};
  
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim();
      
      const keyMap = {
        'Card Name': 'cardName',
        'Card Type': 'cardType',
        'Card Number': 'cardNumber',
        'Rarity': 'rarity',
        'Race': 'race',
        'Background': 'background',
        'Flavor Text': 'flavorText',
        'Armor Level': 'armorLevel',
        'Speed': 'speed',
        'Health Points': 'healthPoints',
        'Attack Name': 'attackName',
        'Attack Dice': 'attackDice',
        'Damage Dice': 'attackDice',
        'Modifier': 'modifier',
        'Hit/Attack Modifier': 'modifier',
        'Other Attributes': 'otherAttributes',
        'Affects Boss': 'affectsBoss',
        'Extended Effect Description': 'extendedEffectDescription'
      };
      
      if (keyMap[key]) {
        card[keyMap[key]] = value;
      }
    }
  }
  
  return card;
}

async function fetchAllCards() {
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Navigate to the page to establish session cookies
  console.log('Navigating to page...');
  await page.goto(PAGE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  // Get all cookies
  const cookies = await context.cookies();
  const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');
  
  const allCards = [];
  const limit = 25;
  let offset = 0;
  let hasMore = true;
  
  console.log('Fetching cards via API...');
  
  while (hasMore) {
    const apiUrl = `${BASE_URL}/pro-gallery-webapp/v1/galleries/${GALLERY_ID}?galleryId=${GALLERY_ID}&offset=${offset}&limit=${limit}&compId=${COMP_ID}&state=PUBLISHED`;
    
    console.log(`Fetching offset ${offset}...`);
    
    const response = await page.evaluate(async (url) => {
      const res = await fetch(url, {
        headers: {
          'Accept': 'application/json',
        },
        credentials: 'include'
      });
      return await res.json();
    }, apiUrl);
    
    if (response.items && response.items.length > 0) {
      for (const item of response.items) {
        const desc = item.metaData?.description || '';
        const card = parseCardDescription(desc);
        card.id = item.id;
        card.imageUrl = item.metaData?.link?.url || '';
        allCards.push(card);
      }
      
      console.log(`  Got ${response.items.length} cards (total: ${allCards.length})`);
      
      if (response.items.length < limit) {
        hasMore = false;
      } else {
        offset += limit;
      }
    } else {
      hasMore = false;
    }
  }
  
  await browser.close();
  
  return allCards;
}

async function main() {
  try {
    const cards = await fetchAllCards();
    console.log(`\nTotal cards fetched: ${cards.length}`);
    
    // Save to file
    const outputPath = './gen2-all-cards.json';
    fs.writeFileSync(outputPath, JSON.stringify(cards, null, 2));
    console.log(`Saved to ${outputPath}`);
    
    // Also save full data
    const fullPath = './gen2-all-cards-complete.json';
    fs.writeFileSync(fullPath, JSON.stringify(cards, null, 2));
    console.log(`Saved to ${fullPath}`);
    
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
