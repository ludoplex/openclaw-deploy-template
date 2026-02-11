# Webdev Agent Plan — Crystal Corp Game Development

**Agent:** webdev  
**Phase:** Game MVP (Weeks 3-4)  
**Focus:** Phaser 3 Game Development, Image Reveal System, Content Generation

---

## Scope

Develop the Crystal Arcade game using Phaser 3, implementing Qix-style gameplay with progressive image reveal mechanics. Create the core game loop, touch controls, enemy AI, and integrate with the CDN for asset delivery. Generate initial content library with AI image generation.

---

## Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| W1 | Phaser 3 project | Game scaffold integrated with Astro |
| W2 | Player movement system | Edge navigation and line drawing |
| W3 | Polygon claiming | Area capture with collision detection |
| W4 | Image reveal system | Progressive mask reveal using Graphics API |
| W5 | Enemy AI (Qix) | Basic enemy with path following |
| W6 | Percentage/win tracking | Level completion at 75%+ |
| W7 | Touch controls | Mobile-optimized input handling |
| W8 | Level progression | Multiple levels with increasing difficulty |
| W9 | Character LoRAs | 3-5 trained character models |
| W10 | Image library | 100 initial images |

---

## Task Schedule

### Week 3: Core Mechanics

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| 15 | Set up Phaser 3 project structure within Astro | 3 | Project scaffold |
| 15 | Configure asset loading from Bunny CDN | 2 | CDN integration |
| 16 | Implement game scene architecture | 4 | Boot, Preload, Game, UI scenes |
| 16 | Create playfield boundary system | 2 | Rectangle game area |
| 17 | Implement player movement (edge-only) | 4 | Arrow keys + WASD |
| 17 | Add player sprite and animations | 2 | Visual player |
| 18 | Implement line drawing mechanics | 5 | Trail following player |
| 18 | Add line collision detection | 2 | Self-intersection check |
| 19 | Implement boundary detection | 3 | Edge snapping |
| 19 | Create polygon claiming logic | 4 | Area calculation |
| 20 | Implement flood fill for region detection | 4 | Which side to claim |
| 20 | Add visual feedback for claimed areas | 2 | Color fill animation |
| 21 | Touch controls (mobile support) | 4 | Swipe-based movement |
| 21 | Test on iOS Safari, Android Chrome | 2 | Cross-platform QA |

### Week 4: Polish & Content

| Day | Task | Hours | Output |
|-----|------|-------|--------|
| 22 | Implement image masking reveal system | 5 | Graphics API masks |
| 22 | Optimize mask updates for performance | 2 | 60fps target |
| 23 | Add enemy (basic Qix) | 4 | Moving enemy sprite |
| 23 | Implement enemy-line collision (game over) | 2 | Death condition |
| 24 | Add percentage tracking | 2 | UI percentage display |
| 24 | Implement win condition (75%+) | 2 | Level complete trigger |
| 24 | Create level transition system | 2 | Next level flow |
| 25 | Set up Stable Diffusion SDXL environment | 3 | Local or RunPod |
| 25 | Train first character LoRA (Luna) | 3 | LoRA checkpoint |
| 26 | Train 2-3 more character LoRAs | 5 | Mika, Diana, Jade LoRAs |
| 27 | Generate batch of 50 images (free tier characters) | 4 | Image set 1 |
| 27 | Post-process: upscale, watermark, export tiers | 2 | Processed images |
| 28 | Generate 50 more images (premium characters) | 4 | Image set 2 |
| 28 | Upload to Bunny CDN, update game data | 2 | CDN populated |

---

## Inputs Required

| Input | Source | Required By |
|-------|--------|-------------|
| Astro project structure | sitecraft agent | Day 15 |
| CDN pull zone URL | neteng agent | Day 15 |
| Character designs/descriptions | Blueprint (Appendix A) | Day 25 |
| Brand colors/style guide | sitecraft agent | Day 15 |

---

## Outputs Produced

| Output | Location | Consumer |
|--------|----------|----------|
| Phaser game files | /src/game/ | Astro build |
| Game assets | Bunny CDN /assets/game/ | Game loader |
| Character images | Bunny CDN /assets/images/characters/ | Game reveal |
| Level data | /data/levels.json | Game loader |
| LoRA models | Local storage (not deployed) | Image generation |

---

## Success Criteria

| Criterion | Measurement | Target |
|-----------|-------------|--------|
| Core loop playable | User testing | Complete level in 2-5 min |
| Touch controls | Mobile testing | Responsive, no lag |
| Image reveal | Visual check | Smooth progressive reveal |
| Performance | FPS counter | 60fps on mobile |
| Image quality | Visual review | No artifacts, consistent style |
| Content library | Count | 100 images minimum |

---

## Handoff to Next Phase

**To social (Week 5):**
- Playable demo for promotional content
- Character images for marketing materials
- Screenshots/recordings for F95zone thread

**To ops (Week 5):**
- Game integrated with subscription system hooks
- Free tier limitations implemented
- Premium content flags in place

---

## Technical Specifications

### Phaser 3 Project Structure

```
src/game/
├── main.ts                 # Phaser game config and init
├── scenes/
│   ├── BootScene.ts        # Asset loading config
│   ├── PreloadScene.ts     # Asset preloader with progress
│   ├── GameScene.ts        # Main gameplay
│   ├── UIScene.ts          # HUD overlay
│   └── LevelCompleteScene.ts
├── objects/
│   ├── Player.ts           # Player entity
│   ├── Trail.ts            # Line drawing system
│   ├── ClaimedArea.ts      # Polygon regions
│   ├── Qix.ts              # Enemy AI
│   └── ImageReveal.ts      # Mask reveal system
├── systems/
│   ├── InputManager.ts     # Keyboard + touch
│   ├── CollisionSystem.ts  # All collision logic
│   └── PolygonMath.ts      # Area calculations
├── data/
│   └── LevelConfig.ts      # Level definitions
└── utils/
    └── Constants.ts        # Game constants
```

### Key Phaser Configuration

```typescript
// main.ts
import Phaser from 'phaser';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO, // WebGL with Canvas fallback
  width: 800,
  height: 600,
  parent: 'game-container',
  backgroundColor: '#0a0a0f',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  physics: {
    default: 'arcade',
    arcade: {
      debug: false,
    },
  },
  scene: [BootScene, PreloadScene, GameScene, UIScene, LevelCompleteScene],
};

new Phaser.Game(config);
```

### Image Reveal System

```typescript
// ImageReveal.ts - Core masking logic
class ImageReveal {
  private image: Phaser.GameObjects.Image;
  private mask: Phaser.GameObjects.Graphics;
  private revealedPolygons: Phaser.Geom.Polygon[] = [];
  
  constructor(scene: Phaser.Scene, imageKey: string) {
    this.image = scene.add.image(400, 300, imageKey);
    this.mask = scene.add.graphics();
    this.image.setMask(this.mask.createGeometryMask());
  }
  
  revealArea(polygon: Phaser.Geom.Polygon): void {
    this.revealedPolygons.push(polygon);
    this.updateMask();
  }
  
  private updateMask(): void {
    this.mask.clear();
    this.mask.fillStyle(0xffffff);
    for (const poly of this.revealedPolygons) {
      this.mask.fillPoints(poly.points, true);
    }
  }
  
  getRevealedPercentage(): number {
    // Calculate total revealed area / total image area
    return this.calculatePolygonArea() / (800 * 600) * 100;
  }
}
```

### Character Definitions (from Blueprint)

```typescript
// Free Tier Characters
const FREE_CHARACTERS = [
  { id: 'luna', name: 'Luna', archetype: 'Mysterious Stranger', style: 'Gothic anime' },
  { id: 'mika', name: 'Mika', archetype: 'Bubbly Idol', style: 'Bright anime' },
  { id: 'diana', name: 'Diana', archetype: 'Confident Temptress', style: 'Semi-realistic' },
  { id: 'jade', name: 'Jade', archetype: 'Athletic Tomboy', style: 'Stylized' },
];

// Premium Characters (partial)
const PREMIUM_CHARACTERS = [
  { id: 'scarlett', name: 'Scarlett', archetype: 'Dominant Queen', style: 'Dark semi-real' },
  { id: 'valentina', name: 'Valentina', archetype: 'Mature Sophisticate', style: 'Painted' },
  { id: 'zara', name: 'Zara', archetype: 'Monster Girl', style: 'Fantasy anime' },
  // ... 11 more
];
```

---

## Image Generation Pipeline

### LoRA Training (per character)

1. **Reference collection**: 20-50 reference images for style/archetype
2. **Training config**: 
   - Model: SDXL / Illustrious / Pony v6
   - Steps: 1500-3000
   - Learning rate: 1e-4
   - Resolution: 1024x1024
3. **Testing**: Generate 10 test images, adjust if needed
4. **Export**: LoRA checkpoint file

### Batch Generation

```bash
# Example ComfyUI workflow (simplified)
Prompt: "1girl, {character_name}, {pose}, {outfit}, {background}, masterpiece, best quality"
Negative: "worst quality, low quality, blurry, watermark, text"
Steps: 30
CFG: 7
Sampler: DPM++ 2M Karras
Size: 1024x1536 (portrait) or 1536x1024 (landscape)
```

### Post-Processing

1. **Upscale**: 2x via Real-ESRGAN
2. **Watermark**: Subtle corner watermark for web tier
3. **Export tiers**:
   - Web (800px) - with watermark
   - HD (2048px) - subscribers only, no watermark
4. **Naming**: `{character}_{set}_{index}.webp`

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Phaser performance issues | Use WebGL, optimize draw calls, pool objects |
| Image reveal flickering | Use proper mask instead of per-pixel |
| Touch controls unresponsive | Add touch areas larger than visuals |
| LoRA training fails | Use proven base models, fallback to prompt-only |
| Image consistency issues | Lock seed for sets, refine LoRA |
