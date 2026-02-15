/**
 * Bulk Card Extractor - uses fetch to get page HTML and parse JSON
 * No browser needed - works with raw HTTP requests
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const PAGES = [
  { name: 'gen1-ed2', url: 'https://www.ward-cardgame.com/card-library-generation-1-edition-2' },
  { name: 'gen2', url: 'https://www.ward-cardgame.com/card-library-generation-2' },
  { name: 'promo', url: 'https://www.ward-cardgame.com/card-library-promo' },
  { name: 'gen1-remastered', url: 'https://www.ward-cardgame.com/gen-1-ed-3' },
  { name: 'gen2-remastered', url: 'https://www.ward-cardgame.com/gen-2-ed-2' },
];

function fetchPage(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function extractCards(html) {
  const cards = [];
  const regex = /"items":\s*\[/g;
  let match;
  
  while ((match = regex.exec(html)) !== null) {
    let start = match.index + match[0].length - 1;
    let bracketCount = 0;
    let end = start;
    
    for (let i = start; i < html.length && i < start + 1000000; i++) {
      if (html[i] === '[') bracketCount++;
      else if (html[i] === ']') {
        bracketCount--;
        if (bracketCount === 0) {
          end = i + 1;
          break;
        }
      }
    }
    
    try {
      const arr = JSON.parse(html.substring(start, end));
      if (arr.length > 0 && arr[0].metaData?.description?.includes('Card Name')) {
        for (const item of arr) {
          const desc = item.metaData?.description || '';
          const parseField = (fieldName) => {
            const re = new RegExp(`${fieldName}:\\s*([^\\n]+)`);
            const m = desc.match(re);
            return m ? m[1].trim() : null;
          };
          
          cards.push({
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
            rawDescription: desc
          });
        }
      }
    } catch(e) {}
  }
  
  return cards;
}

async function main() {
  const allCards = {};
  
  for (const { name, url } of PAGES) {
    console.log(`Fetching ${name}...`);
    try {
      const html = await fetchPage(url);
      const cards = extractCards(html);
      allCards[name] = cards;
      console.log(`  Found ${cards.length} cards`);
      
      fs.writeFileSync(
        path.join(__dirname, `cards-${name}.json`),
        JSON.stringify(cards, null, 2)
      );
    } catch (err) {
      console.error(`  Error: ${err.message}`);
      allCards[name] = [];
    }
  }
  
  const combined = {
    extractedAt: new Date().toISOString(),
    source: 'ward-cardgame.com',
    method: 'HTML parse of Wix Pro Gallery items',
    generations: allCards,
    totalCards: Object.values(allCards).reduce((sum, arr) => sum + arr.length, 0)
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'all-cards.json'),
    JSON.stringify(combined, null, 2)
  );
  
  console.log(`\n✅ Total: ${combined.totalCards} cards`);
}

main().catch(console.error);
