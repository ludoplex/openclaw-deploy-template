// Parse raw extracted Gen 2 card data
const fs = require('fs');

const rawData = JSON.parse(fs.readFileSync('./gen2-raw-extract.json', 'utf8'));

const cards = rawData.map((raw, idx) => {
  // The cardName contains all concatenated text, need to parse it
  const fullText = raw.cardName || '';
  const card = { displayTitle: raw.displayTitle };
  
  // Split by field names
  const fields = [
    'Card Name:', 'Card Type:', 'Card Number:', 'Rarity:', 'Race:',
    'Background:', 'Flavor Text:', 'Armor Level:', 'Speed:', 'Health Points:',
    'Attack Name:', 'Attack Dice:', 'Damage Dice:', 'Modifier:', 'Hit/Attack Modifier:',
    'Other Attributes:', 'Affects Boss:', 'Extended Effect Description:'
  ];
  
  const keyMap = {
    'Card Name': 'cardName', 'Card Type': 'cardType', 'Card Number': 'cardNumber',
    'Rarity': 'rarity', 'Race': 'race', 'Background': 'background',
    'Flavor Text': 'flavorText', 'Armor Level': 'armorLevel', 'Speed': 'speed',
    'Health Points': 'healthPoints', 'Attack Name': 'attackName',
    'Attack Dice': 'attackDice', 'Damage Dice': 'attackDice', 'Modifier': 'modifier',
    'Other Attributes': 'otherAttributes', 'Affects Boss': 'affectsBoss',
    'Extended Effect Description': 'extendedEffectDescription'
  };
  
  let remaining = fullText;
  
  for (let i = 0; i < fields.length; i++) {
    const field = fields[i];
    const key = field.replace(':', '');
    const idx = remaining.indexOf(field);
    if (idx !== -1) {
      // Find where the next field starts
      let endIdx = remaining.length;
      for (let j = i + 1; j < fields.length; j++) {
        const nextIdx = remaining.indexOf(fields[j]);
        if (nextIdx !== -1 && nextIdx > idx) {
          endIdx = nextIdx;
          break;
        }
      }
      const value = remaining.substring(idx + field.length, endIdx).trim();
      if (keyMap[key]) {
        card[keyMap[key]] = value;
      }
    }
  }
  
  return card;
});

fs.writeFileSync('./gen2-all-cards-complete.json', JSON.stringify(cards, null, 2));
console.log(`Parsed ${cards.length} cards`);
console.log('Sample:', JSON.stringify(cards[0], null, 2));
