/**
 * Fetch ALL Ward TCG cards directly from the Wix Pro Gallery API
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const GALLERY_ID = '374b0062-ad2c-4a70-bda1-2c2d7ba81657';
const EXTERNAL_ID = '2e50edb0-be16-4154-a2a3-676d7459f884';
const BASE_URL = `https://www.ward-cardgame.com/pro-gallery-webapp/v1/galleries/${GALLERY_ID}`;

function fetchPage(offset) {
  const url = `${BASE_URL}?galleryId=${GALLERY_ID}&offset=${offset}&limit=25&externalId=${EXTERNAL_ID}&state=PUBLISHED`;
  
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

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
    rawDescription: desc
  };
}

async function main() {
  console.log('Fetching all cards from Wix Pro Gallery API...\n');
  
  const allCards = [];
  let offset = 0;
  let total = 0;
  
  do {
    console.log(`Fetching offset ${offset}...`);
    const data = await fetchPage(offset);
    
    if (!total) {
      total = data.gallery?.totalItemsCount || 0;
      console.log(`Total items: ${total}`);
    }
    
    const items = data.gallery?.items || [];
    for (const item of items) {
      allCards.push(parseCard(item));
    }
    
    console.log(`  Got ${items.length} items (total so far: ${allCards.length})`);
    
    offset += 25;
    
    // Rate limit
    await new Promise(r => setTimeout(r, 500));
    
  } while (offset < total);
  
  // Save results
  const output = {
    extractedAt: new Date().toISOString(),
    source: 'ward-cardgame.com',
    method: 'Direct Wix Pro Gallery API',
    galleryId: GALLERY_ID,
    totalCards: allCards.length,
    cards: allCards
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'all-cards-complete.json'),
    JSON.stringify(output, null, 2)
  );
  
  console.log(`\n✅ Success! Extracted ${allCards.length} cards`);
  console.log(`Output: ${path.join(__dirname, 'all-cards-complete.json')}`);
}

main().catch(console.error);
