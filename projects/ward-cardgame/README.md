# Ward TCG Card Data Extraction

## Summary

Ward TCG (ward-cardgame.com) is built on Wix with a Pro Gallery widget showing cards.

### Data Structure Found

Card data is embedded in the page's inline `<script>` tags as:
```javascript
appsWarmupData["comp-m3o0xz46_galleryData"] = {
  items: [
    {
      itemId: "uuid",
      metaData: {
        description: "Card Name: ...\nCard Type: ...\n..."
      }
    }
  ]
}
```

### The Problem

- **Total cards**: 150+ per generation
- **Initial page load**: Only 25 cards embedded in HTML
- **Pagination**: Wix Pro Gallery uses lazy-loading; remaining cards fetched via internal API

### Files

| File | Description |
|------|-------------|
| `gen1-rarity-list.xlsx` | Official Excel with all 150 card names/types/rarities (no effects) |
| `gen2-rarity-list.xlsx` | Same for Gen 2 |
| `cards-gen1-ed2-sample.json` | 25 cards with full Extended Effect Descriptions |
| `extract-cards.js` | Playwright script to extract cards from page |
| `bulk-extract.js` | Node.js HTTP-only extractor (gets first 25 per page) |

### Card Data Schema

```json
{
  "cardName": "Basilisk",
  "cardType": "Creature",
  "cardNumber": "25",
  "rarity": "Epic",
  "race": "Beast",
  "background": "Forest",
  "flavorText": "This monster searches the darkest areas...",
  "armorLevel": "10",
  "speed": "5",
  "healthPoints": "100",
  "attackName": "Toxic Strike",
  "attackDice": "2",
  "modifier": "3",
  "otherAttributes": "N/A",
  "affectsBoss": "Yes",
  "extendedEffectDescription": "While on the field the target creature takes 5 poison damage..."
}
```

### Pages

| Generation | URL | Total Cards |
|------------|-----|-------------|
| Gen 1 Ed 2 | /card-library-generation-1-edition-2 | 151 |
| Gen 1 Ed 1 | /card-library-generation-1-edition-1 | ~150 |
| Gen 2 | /card-library-generation-2 | ~150 |
| Gen 3 | /gen-3 | ~150 |
| Promo | /card-library-promo | TBD |
| Gen 1 Remastered | /gen-1-ed-3 | TBD |
| Gen 2 Remastered | /gen-2-ed-2 | TBD |

### Solution: Full Extraction with Playwright

To get ALL cards (not just the initial 25), use Playwright to:
1. Load the page
2. Scroll the gallery to trigger lazy-loading
3. Extract all items after they load

```javascript
// See extract-cards-full.js for implementation
```

### Quick Start

```bash
# Install dependencies
npm install playwright

# Run extraction
node extract-cards-full.js
```

### API Discovery (for future)

The Wix Pro Gallery loads additional items via XHR. Key identifiers:
- Gallery ID: `374b0062-ad2c-4a70-bda1-2c2d7ba81657`
- Site ID: `ad96a979-faab-40b2-9ac6-41be6a12fee9`
- Meta Site ID: `b9fa2abe-4edd-4200-9371-980fa1ae26f9`

If you can intercept/replay the gallery pagination API, you could fetch all items directly.
