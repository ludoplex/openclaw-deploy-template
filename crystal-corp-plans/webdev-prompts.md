# Webdev Agent Stage Prompts — Crystal Corp

Ready-to-paste prompts for game development and content generation. Each prompt is self-contained.

---

## Stage 1: Phaser 3 Project Setup (Day 15)

```
Set up Phaser 3 game project integrated with the Crystal Arcade Astro site.

**Context:**
- Crystal Arcade is a Qix/Gals Panic style game
- Players draw lines to claim territory and reveal AI-generated pin-up images
- Must work on desktop and mobile (touch)
- Astro 4.x is already set up at /var/www/crystalarcade

**Installation:**
```bash
cd /var/www/crystalarcade
npm install phaser
```

**Create game directory structure:**
```
src/game/
├── main.ts
├── scenes/
│   ├── BootScene.ts
│   ├── PreloadScene.ts
│   ├── GameScene.ts
│   ├── UIScene.ts
│   └── LevelCompleteScene.ts
├── objects/
│   ├── Player.ts
│   ├── Trail.ts
│   ├── ClaimedArea.ts
│   ├── Qix.ts
│   └── ImageReveal.ts
├── systems/
│   ├── InputManager.ts
│   ├── CollisionSystem.ts
│   └── PolygonMath.ts
└── utils/
    └── Constants.ts
```

**src/game/main.ts:**
```typescript
import Phaser from 'phaser';
import { BootScene } from './scenes/BootScene';
import { PreloadScene } from './scenes/PreloadScene';
import { GameScene } from './scenes/GameScene';
import { UIScene } from './scenes/UIScene';
import { LevelCompleteScene } from './scenes/LevelCompleteScene';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',
  backgroundColor: '#0a0a0f',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  input: {
    touch: true,
  },
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 0 },
      debug: false,
    },
  },
  scene: [BootScene, PreloadScene, GameScene, UIScene, LevelCompleteScene],
};

export default new Phaser.Game(config);
```

**src/game/utils/Constants.ts:**
```typescript
export const GAME_WIDTH = 800;
export const GAME_HEIGHT = 600;
export const PLAYFIELD_PADDING = 20;

export const COLORS = {
  BOUNDARY: 0x7c3aed,      // Purple
  PLAYER: 0xff4d6d,        // Pink/red
  TRAIL: 0x00d4ff,         // Cyan
  CLAIMED: 0x4ade80,       // Green
  ENEMY: 0xff0000,         // Red
};

export const SPEEDS = {
  PLAYER: 200,
  ENEMY: 100,
};

export const WIN_PERCENTAGE = 75;

// CDN URL for assets
export const CDN_BASE = 'https://cdn.crystalarcade.gg';
```

**Astro integration (src/pages/game/[level].astro):**
```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';

const { level } = Astro.params;
---

<BaseLayout title={`Level ${level}`}>
  <div class="min-h-screen flex items-center justify-center bg-crystal-bg">
    <div id="game-container" class="w-full max-w-4xl aspect-[4/3]"></div>
  </div>
  
  <script>
    import '../game/main';
  </script>
</BaseLayout>
```

**Verify:**
```bash
npm run dev
# Navigate to /game/1
# Should see blank Phaser canvas
```

Output: Complete project structure, working game bootstrap, Astro integration.
```

---

## Stage 2: Player Movement System (Day 17)

```
Implement player movement for Crystal Arcade Qix gameplay.

**Movement Rules:**
- Player moves along the boundary edges (rectangle perimeter)
- Player can also move INTO the playfield (line drawing mode)
- When on boundary: move clockwise or counter-clockwise
- When drawing line: move in 4 directions (up/down/left/right)
- Player cannot cross their own trail
- Player returns to boundary when line completes

**src/game/objects/Player.ts:**
```typescript
import Phaser from 'phaser';
import { COLORS, SPEEDS, GAME_WIDTH, GAME_HEIGHT, PLAYFIELD_PADDING } from '../utils/Constants';

export enum PlayerState {
  ON_BOUNDARY,
  DRAWING_LINE,
}

export class Player extends Phaser.GameObjects.Container {
  private sprite: Phaser.GameObjects.Arc;
  private state: PlayerState = PlayerState.ON_BOUNDARY;
  private boundary: Phaser.Geom.Rectangle;
  private edgePosition: number = 0; // 0-1 around perimeter
  
  constructor(scene: Phaser.Scene) {
    super(scene, PLAYFIELD_PADDING, PLAYFIELD_PADDING);
    
    // Create player visual
    this.sprite = scene.add.circle(0, 0, 8, COLORS.PLAYER);
    this.add(this.sprite);
    
    // Define playfield boundary
    this.boundary = new Phaser.Geom.Rectangle(
      PLAYFIELD_PADDING,
      PLAYFIELD_PADDING,
      GAME_WIDTH - PLAYFIELD_PADDING * 2,
      GAME_HEIGHT - PLAYFIELD_PADDING * 2
    );
    
    scene.add.existing(this);
  }
  
  update(cursors: Phaser.Types.Input.Keyboard.CursorKeys, delta: number): void {
    const speed = SPEEDS.PLAYER * (delta / 1000);
    
    if (this.state === PlayerState.ON_BOUNDARY) {
      this.moveOnBoundary(cursors, speed);
    } else {
      this.moveDrawingLine(cursors, speed);
    }
  }
  
  private moveOnBoundary(cursors: Phaser.Types.Input.Keyboard.CursorKeys, speed: number): void {
    // Move along perimeter
    if (cursors.right?.isDown || cursors.down?.isDown) {
      this.edgePosition += speed / this.getPerimeter();
    } else if (cursors.left?.isDown || cursors.up?.isDown) {
      this.edgePosition -= speed / this.getPerimeter();
    }
    
    // Wrap around
    if (this.edgePosition > 1) this.edgePosition -= 1;
    if (this.edgePosition < 0) this.edgePosition += 1;
    
    // Convert to position
    const pos = this.edgeToPosition(this.edgePosition);
    this.setPosition(pos.x, pos.y);
    
    // Check for entering playfield
    if (cursors.space?.isDown) {
      this.state = PlayerState.DRAWING_LINE;
      this.emit('startDrawing', { x: this.x, y: this.y });
    }
  }
  
  private moveDrawingLine(cursors: Phaser.Types.Input.Keyboard.CursorKeys, speed: number): void {
    let dx = 0, dy = 0;
    
    if (cursors.left?.isDown) dx = -speed;
    if (cursors.right?.isDown) dx = speed;
    if (cursors.up?.isDown) dy = -speed;
    if (cursors.down?.isDown) dy = speed;
    
    // Constrain to playfield
    const newX = Phaser.Math.Clamp(this.x + dx, this.boundary.left, this.boundary.right);
    const newY = Phaser.Math.Clamp(this.y + dy, this.boundary.top, this.boundary.bottom);
    
    this.setPosition(newX, newY);
    this.emit('drawing', { x: newX, y: newY });
    
    // Check if returned to boundary
    if (this.isOnBoundary(newX, newY)) {
      this.state = PlayerState.ON_BOUNDARY;
      this.edgePosition = this.positionToEdge(newX, newY);
      this.emit('finishDrawing', { x: newX, y: newY });
    }
  }
  
  private getPerimeter(): number {
    return (this.boundary.width + this.boundary.height) * 2;
  }
  
  private edgeToPosition(t: number): Phaser.Math.Vector2 {
    const perim = this.getPerimeter();
    const dist = t * perim;
    const b = this.boundary;
    
    if (dist < b.width) {
      return new Phaser.Math.Vector2(b.left + dist, b.top);
    } else if (dist < b.width + b.height) {
      return new Phaser.Math.Vector2(b.right, b.top + (dist - b.width));
    } else if (dist < b.width * 2 + b.height) {
      return new Phaser.Math.Vector2(b.right - (dist - b.width - b.height), b.bottom);
    } else {
      return new Phaser.Math.Vector2(b.left, b.bottom - (dist - b.width * 2 - b.height));
    }
  }
  
  private positionToEdge(x: number, y: number): number {
    // Inverse of edgeToPosition
    const b = this.boundary;
    const perim = this.getPerimeter();
    
    if (y === b.top) return (x - b.left) / perim;
    if (x === b.right) return (b.width + (y - b.top)) / perim;
    if (y === b.bottom) return (b.width + b.height + (b.right - x)) / perim;
    return (b.width * 2 + b.height + (b.bottom - y)) / perim;
  }
  
  private isOnBoundary(x: number, y: number): boolean {
    const b = this.boundary;
    const tolerance = 2;
    return (
      Math.abs(x - b.left) < tolerance ||
      Math.abs(x - b.right) < tolerance ||
      Math.abs(y - b.top) < tolerance ||
      Math.abs(y - b.bottom) < tolerance
    );
  }
  
  getState(): PlayerState { return this.state; }
}
```

**Integration in GameScene:**
```typescript
// In GameScene.ts create()
this.player = new Player(this);
this.cursors = this.input.keyboard.createCursorKeys();

this.player.on('startDrawing', (pos) => this.trail.start(pos));
this.player.on('drawing', (pos) => this.trail.addPoint(pos));
this.player.on('finishDrawing', (pos) => this.handlePolygonComplete());

// In update()
this.player.update(this.cursors, delta);
```

Output: Working player movement on boundary with keyboard controls.
```

---

## Stage 3: Line Drawing & Polygon Claiming (Days 18-20)

```
Implement line drawing trail and polygon claiming for territory capture.

**src/game/objects/Trail.ts:**
```typescript
import Phaser from 'phaser';
import { COLORS } from '../utils/Constants';

export class Trail extends Phaser.GameObjects.Graphics {
  private points: Phaser.Math.Vector2[] = [];
  private isDrawing: boolean = false;
  
  constructor(scene: Phaser.Scene) {
    super(scene);
    scene.add.existing(this);
    this.setDepth(10);
  }
  
  start(position: { x: number; y: number }): void {
    this.points = [new Phaser.Math.Vector2(position.x, position.y)];
    this.isDrawing = true;
    this.redraw();
  }
  
  addPoint(position: { x: number; y: number }): void {
    if (!this.isDrawing) return;
    
    const newPoint = new Phaser.Math.Vector2(position.x, position.y);
    const last = this.points[this.points.length - 1];
    
    // Only add if moved significantly
    if (last && Phaser.Math.Distance.BetweenPoints(last, newPoint) > 5) {
      // Check for self-intersection
      if (this.intersectsSelf(last, newPoint)) {
        this.scene.events.emit('trailCollision');
        return;
      }
      
      this.points.push(newPoint);
      this.redraw();
    }
  }
  
  finish(position: { x: number; y: number }): Phaser.Geom.Polygon | null {
    if (!this.isDrawing) return null;
    
    this.points.push(new Phaser.Math.Vector2(position.x, position.y));
    this.isDrawing = false;
    
    const polygon = this.createPolygon();
    this.clear();
    this.points = [];
    
    return polygon;
  }
  
  private redraw(): void {
    this.clear();
    if (this.points.length < 2) return;
    
    this.lineStyle(4, COLORS.TRAIL, 1);
    this.beginPath();
    this.moveTo(this.points[0].x, this.points[0].y);
    
    for (let i = 1; i < this.points.length; i++) {
      this.lineTo(this.points[i].x, this.points[i].y);
    }
    
    this.strokePath();
  }
  
  private intersectsSelf(from: Phaser.Math.Vector2, to: Phaser.Math.Vector2): boolean {
    // Check if new segment intersects any existing segment
    const newLine = new Phaser.Geom.Line(from.x, from.y, to.x, to.y);
    
    for (let i = 0; i < this.points.length - 2; i++) {
      const existingLine = new Phaser.Geom.Line(
        this.points[i].x, this.points[i].y,
        this.points[i + 1].x, this.points[i + 1].y
      );
      
      if (Phaser.Geom.Intersects.LineToLine(newLine, existingLine)) {
        return true;
      }
    }
    
    return false;
  }
  
  private createPolygon(): Phaser.Geom.Polygon {
    // Create polygon from trail points + boundary connection
    return new Phaser.Geom.Polygon(this.points);
  }
  
  getPoints(): Phaser.Math.Vector2[] {
    return [...this.points];
  }
}
```

**src/game/systems/PolygonMath.ts:**
```typescript
import Phaser from 'phaser';

export class PolygonMath {
  
  /**
   * Calculate area of polygon using Shoelace formula
   */
  static calculateArea(polygon: Phaser.Geom.Polygon): number {
    const points = polygon.points;
    let area = 0;
    const n = points.length;
    
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      area += points[i].x * points[j].y;
      area -= points[j].x * points[i].y;
    }
    
    return Math.abs(area / 2);
  }
  
  /**
   * Determine which side of the trail to claim (flood fill based)
   * Returns the side with the smaller area OR the side without the enemy
   */
  static determineSideToClam(
    trail: Phaser.Math.Vector2[],
    boundary: Phaser.Geom.Rectangle,
    enemyPosition: Phaser.Math.Vector2
  ): 'left' | 'right' {
    // Create test points on each side of the trail
    const midPoint = trail[Math.floor(trail.length / 2)];
    
    // Perpendicular test points
    const leftTest = new Phaser.Math.Vector2(midPoint.x - 10, midPoint.y);
    const rightTest = new Phaser.Math.Vector2(midPoint.x + 10, midPoint.y);
    
    // Pick the side without the enemy (if possible)
    // Otherwise pick the smaller side
    const leftContainsEnemy = this.pointOnSameSide(leftTest, enemyPosition, trail);
    
    return leftContainsEnemy ? 'right' : 'left';
  }
  
  private static pointOnSameSide(
    p1: Phaser.Math.Vector2,
    p2: Phaser.Math.Vector2,
    line: Phaser.Math.Vector2[]
  ): boolean {
    // Simplified - actual implementation needs proper geometry
    return true;
  }
  
  /**
   * Create claimed polygon combining trail with boundary edges
   */
  static createClaimedPolygon(
    trail: Phaser.Math.Vector2[],
    boundary: Phaser.Geom.Rectangle,
    side: 'left' | 'right'
  ): Phaser.Geom.Polygon {
    // This is simplified - real implementation needs to:
    // 1. Find where trail starts/ends on boundary
    // 2. Trace boundary edge between those points
    // 3. Combine with trail to form closed polygon
    return new Phaser.Geom.Polygon(trail);
  }
}
```

**src/game/objects/ClaimedArea.ts:**
```typescript
import Phaser from 'phaser';
import { COLORS } from '../utils/Constants';

export class ClaimedArea extends Phaser.GameObjects.Graphics {
  private polygons: Phaser.Geom.Polygon[] = [];
  private totalArea: number = 0;
  private playfieldArea: number;
  
  constructor(scene: Phaser.Scene, playfieldArea: number) {
    super(scene);
    this.playfieldArea = playfieldArea;
    scene.add.existing(this);
    this.setDepth(5);
  }
  
  addPolygon(polygon: Phaser.Geom.Polygon): void {
    this.polygons.push(polygon);
    this.calculateTotalArea();
    this.redraw();
    this.scene.events.emit('areaUpdated', this.getPercentage());
  }
  
  private calculateTotalArea(): void {
    this.totalArea = 0;
    for (const poly of this.polygons) {
      this.totalArea += this.calculatePolygonArea(poly);
    }
  }
  
  private calculatePolygonArea(polygon: Phaser.Geom.Polygon): number {
    const points = polygon.points;
    let area = 0;
    const n = points.length;
    
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      area += points[i].x * points[j].y;
      area -= points[j].x * points[i].y;
    }
    
    return Math.abs(area / 2);
  }
  
  private redraw(): void {
    this.clear();
    this.fillStyle(COLORS.CLAIMED, 0.3);
    this.lineStyle(2, COLORS.CLAIMED, 0.8);
    
    for (const polygon of this.polygons) {
      this.beginPath();
      this.moveTo(polygon.points[0].x, polygon.points[0].y);
      
      for (let i = 1; i < polygon.points.length; i++) {
        this.lineTo(polygon.points[i].x, polygon.points[i].y);
      }
      
      this.closePath();
      this.fillPath();
      this.strokePath();
    }
  }
  
  getPercentage(): number {
    return (this.totalArea / this.playfieldArea) * 100;
  }
  
  getPolygons(): Phaser.Geom.Polygon[] {
    return this.polygons;
  }
}
```

Output: Trail drawing with self-intersection detection, polygon calculation, claimed area display.
```

---

## Stage 4: Image Reveal System (Day 22)

```
Implement progressive image reveal using Phaser 3 Graphics masking.

**src/game/objects/ImageReveal.ts:**
```typescript
import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, PLAYFIELD_PADDING, CDN_BASE } from '../utils/Constants';

export class ImageReveal {
  private scene: Phaser.Scene;
  private image: Phaser.GameObjects.Image;
  private maskGraphics: Phaser.GameObjects.Graphics;
  private mask: Phaser.Display.Masks.GeometryMask;
  private revealedPolygons: Phaser.Geom.Polygon[] = [];
  
  constructor(scene: Phaser.Scene, characterId: string, imageIndex: number) {
    this.scene = scene;
    
    // Load image (already loaded in PreloadScene)
    const imageKey = `${characterId}_${imageIndex}`;
    
    // Create image centered in playfield
    this.image = scene.add.image(
      GAME_WIDTH / 2,
      GAME_HEIGHT / 2,
      imageKey
    );
    
    // Scale image to fit playfield while maintaining aspect ratio
    const playfieldWidth = GAME_WIDTH - PLAYFIELD_PADDING * 2;
    const playfieldHeight = GAME_HEIGHT - PLAYFIELD_PADDING * 2;
    const scale = Math.max(
      playfieldWidth / this.image.width,
      playfieldHeight / this.image.height
    );
    this.image.setScale(scale);
    this.image.setDepth(1);
    
    // Create mask graphics
    this.maskGraphics = scene.add.graphics();
    this.maskGraphics.setVisible(false);
    
    // Create geometry mask
    this.mask = this.maskGraphics.createGeometryMask();
    this.image.setMask(this.mask);
    
    // Initialize with empty mask (nothing visible)
    this.updateMask();
  }
  
  /**
   * Reveal a new area by adding a polygon to the mask
   */
  reveal(polygon: Phaser.Geom.Polygon): void {
    this.revealedPolygons.push(polygon);
    this.updateMask();
    
    // Optional: Add particle effect or flash
    this.playRevealEffect(polygon);
  }
  
  private updateMask(): void {
    this.maskGraphics.clear();
    this.maskGraphics.fillStyle(0xffffff);
    
    for (const polygon of this.revealedPolygons) {
      if (polygon.points.length < 3) continue;
      
      this.maskGraphics.beginPath();
      this.maskGraphics.moveTo(polygon.points[0].x, polygon.points[0].y);
      
      for (let i = 1; i < polygon.points.length; i++) {
        this.maskGraphics.lineTo(polygon.points[i].x, polygon.points[i].y);
      }
      
      this.maskGraphics.closePath();
      this.maskGraphics.fillPath();
    }
  }
  
  private playRevealEffect(polygon: Phaser.Geom.Polygon): void {
    // Flash effect on newly revealed area
    const flash = this.scene.add.graphics();
    flash.fillStyle(0xffffff, 0.5);
    flash.beginPath();
    flash.moveTo(polygon.points[0].x, polygon.points[0].y);
    for (let i = 1; i < polygon.points.length; i++) {
      flash.lineTo(polygon.points[i].x, polygon.points[i].y);
    }
    flash.closePath();
    flash.fillPath();
    flash.setDepth(100);
    
    // Fade out
    this.scene.tweens.add({
      targets: flash,
      alpha: 0,
      duration: 300,
      onComplete: () => flash.destroy(),
    });
  }
  
  getRevealedPercentage(): number {
    let totalArea = 0;
    for (const polygon of this.revealedPolygons) {
      totalArea += this.calculatePolygonArea(polygon);
    }
    
    const playfieldArea = 
      (GAME_WIDTH - PLAYFIELD_PADDING * 2) * 
      (GAME_HEIGHT - PLAYFIELD_PADDING * 2);
    
    return (totalArea / playfieldArea) * 100;
  }
  
  private calculatePolygonArea(polygon: Phaser.Geom.Polygon): number {
    const points = polygon.points;
    let area = 0;
    const n = points.length;
    
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      area += points[i].x * points[j].y;
      area -= points[j].x * points[i].y;
    }
    
    return Math.abs(area / 2);
  }
  
  destroy(): void {
    this.image.destroy();
    this.maskGraphics.destroy();
  }
}
```

**PreloadScene image loading:**
```typescript
// In PreloadScene.ts
preload() {
  const levelData = this.registry.get('levelData');
  const characterId = levelData.character;
  const imageIndex = levelData.imageIndex;
  
  // Load from CDN
  this.load.image(
    `${characterId}_${imageIndex}`,
    `${CDN_BASE}/assets/images/characters/${characterId}/${imageIndex}.webp`
  );
}
```

**Integration in GameScene:**
```typescript
// In GameScene create()
const levelData = this.registry.get('levelData');
this.imageReveal = new ImageReveal(this, levelData.character, levelData.imageIndex);

// When polygon is claimed
handlePolygonComplete() {
  const polygon = this.trail.finish({ x: this.player.x, y: this.player.y });
  if (polygon) {
    this.claimedArea.addPolygon(polygon);
    this.imageReveal.reveal(polygon);
    
    // Check win condition
    if (this.imageReveal.getRevealedPercentage() >= WIN_PERCENTAGE) {
      this.scene.start('LevelCompleteScene');
    }
  }
}
```

Output: Working image reveal system with mask updates and visual effects.
```

---

## Stage 5: Enemy AI (Day 23)

```
Implement basic Qix enemy that moves within the playfield.

**src/game/objects/Qix.ts:**
```typescript
import Phaser from 'phaser';
import { COLORS, SPEEDS, GAME_WIDTH, GAME_HEIGHT, PLAYFIELD_PADDING } from '../utils/Constants';

export class Qix extends Phaser.GameObjects.Container {
  private sprite: Phaser.GameObjects.Arc;
  private velocity: Phaser.Math.Vector2;
  private boundary: Phaser.Geom.Rectangle;
  private trailGraphics: Phaser.GameObjects.Graphics;
  private trailPoints: Phaser.Math.Vector2[] = [];
  
  constructor(scene: Phaser.Scene) {
    // Start in center of playfield
    const startX = GAME_WIDTH / 2;
    const startY = GAME_HEIGHT / 2;
    
    super(scene, startX, startY);
    
    // Visual
    this.sprite = scene.add.circle(0, 0, 15, COLORS.ENEMY);
    this.add(this.sprite);
    
    // Trail effect
    this.trailGraphics = scene.add.graphics();
    this.trailGraphics.setDepth(8);
    
    // Random initial velocity
    const angle = Phaser.Math.FloatBetween(0, Math.PI * 2);
    this.velocity = new Phaser.Math.Vector2(
      Math.cos(angle) * SPEEDS.ENEMY,
      Math.sin(angle) * SPEEDS.ENEMY
    );
    
    // Boundary
    this.boundary = new Phaser.Geom.Rectangle(
      PLAYFIELD_PADDING + 15,
      PLAYFIELD_PADDING + 15,
      GAME_WIDTH - PLAYFIELD_PADDING * 2 - 30,
      GAME_HEIGHT - PLAYFIELD_PADDING * 2 - 30
    );
    
    scene.add.existing(this);
    this.setDepth(20);
  }
  
  update(delta: number, claimedPolygons: Phaser.Geom.Polygon[]): void {
    const dt = delta / 1000;
    
    // Move
    this.x += this.velocity.x * dt;
    this.y += this.velocity.y * dt;
    
    // Bounce off boundary
    if (this.x <= this.boundary.left || this.x >= this.boundary.right) {
      this.velocity.x *= -1;
      this.addRandomness();
    }
    if (this.y <= this.boundary.top || this.y >= this.boundary.bottom) {
      this.velocity.y *= -1;
      this.addRandomness();
    }
    
    // Bounce off claimed areas
    for (const polygon of claimedPolygons) {
      if (this.isInsidePolygon(polygon)) {
        this.bounceOffPolygon(polygon);
      }
    }
    
    // Constrain to boundary
    this.x = Phaser.Math.Clamp(this.x, this.boundary.left, this.boundary.right);
    this.y = Phaser.Math.Clamp(this.y, this.boundary.top, this.boundary.bottom);
    
    // Update trail
    this.updateTrail();
  }
  
  private addRandomness(): void {
    // Add slight random variation to movement
    const variation = Phaser.Math.FloatBetween(-0.3, 0.3);
    this.velocity.rotate(variation);
    
    // Normalize speed
    this.velocity.normalize().scale(SPEEDS.ENEMY);
  }
  
  private isInsidePolygon(polygon: Phaser.Geom.Polygon): boolean {
    return Phaser.Geom.Polygon.Contains(polygon, this.x, this.y);
  }
  
  private bounceOffPolygon(polygon: Phaser.Geom.Polygon): void {
    // Simple bounce - reverse direction
    this.velocity.scale(-1);
    this.addRandomness();
  }
  
  private updateTrail(): void {
    // Add current position to trail
    this.trailPoints.push(new Phaser.Math.Vector2(this.x, this.y));
    
    // Keep only last 20 points
    if (this.trailPoints.length > 20) {
      this.trailPoints.shift();
    }
    
    // Draw trail
    this.trailGraphics.clear();
    if (this.trailPoints.length < 2) return;
    
    this.trailGraphics.lineStyle(3, COLORS.ENEMY, 0.3);
    this.trailGraphics.beginPath();
    this.trailGraphics.moveTo(this.trailPoints[0].x, this.trailPoints[0].y);
    
    for (let i = 1; i < this.trailPoints.length; i++) {
      this.trailGraphics.lineTo(this.trailPoints[i].x, this.trailPoints[i].y);
    }
    
    this.trailGraphics.strokePath();
  }
  
  /**
   * Check if Qix collides with player's active trail
   */
  checkTrailCollision(trail: Phaser.Math.Vector2[]): boolean {
    if (trail.length < 2) return false;
    
    for (let i = 0; i < trail.length - 1; i++) {
      const line = new Phaser.Geom.Line(
        trail[i].x, trail[i].y,
        trail[i + 1].x, trail[i + 1].y
      );
      
      const circle = new Phaser.Geom.Circle(this.x, this.y, 15);
      
      if (Phaser.Geom.Intersects.LineToCircle(line, circle)) {
        return true;
      }
    }
    
    return false;
  }
  
  getPosition(): Phaser.Math.Vector2 {
    return new Phaser.Math.Vector2(this.x, this.y);
  }
}
```

**Collision handling in GameScene:**
```typescript
// In GameScene update()
if (this.player.getState() === PlayerState.DRAWING_LINE) {
  if (this.qix.checkTrailCollision(this.trail.getPoints())) {
    this.handleDeath();
  }
}

handleDeath() {
  // Visual feedback
  this.cameras.main.shake(200, 0.01);
  
  // Lose a life or game over
  this.lives--;
  if (this.lives <= 0) {
    this.scene.start('GameOverScene');
  } else {
    this.resetTrail();
    this.player.returnToBoundary();
  }
}
```

Output: Qix enemy with bouncing movement, trail visual, collision detection.
```

---

## Stage 6: Touch Controls (Day 21)

```
Implement mobile-friendly touch controls for Crystal Arcade.

**src/game/systems/InputManager.ts:**
```typescript
import Phaser from 'phaser';

export interface InputState {
  left: boolean;
  right: boolean;
  up: boolean;
  down: boolean;
  action: boolean; // Enter playfield / confirm
}

export class InputManager {
  private scene: Phaser.Scene;
  private cursors: Phaser.Types.Input.Keyboard.CursorKeys;
  private wasd: { [key: string]: Phaser.Input.Keyboard.Key };
  private touchStartPos: Phaser.Math.Vector2 | null = null;
  private currentTouch: Phaser.Math.Vector2 | null = null;
  private isTouching: boolean = false;
  private swipeThreshold: number = 30;
  
  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    
    // Keyboard input
    this.cursors = scene.input.keyboard!.createCursorKeys();
    this.wasd = {
      W: scene.input.keyboard!.addKey('W'),
      A: scene.input.keyboard!.addKey('A'),
      S: scene.input.keyboard!.addKey('S'),
      D: scene.input.keyboard!.addKey('D'),
      SPACE: scene.input.keyboard!.addKey('SPACE'),
    };
    
    // Touch input
    scene.input.on('pointerdown', this.onPointerDown, this);
    scene.input.on('pointermove', this.onPointerMove, this);
    scene.input.on('pointerup', this.onPointerUp, this);
  }
  
  private onPointerDown(pointer: Phaser.Input.Pointer): void {
    this.touchStartPos = new Phaser.Math.Vector2(pointer.x, pointer.y);
    this.currentTouch = new Phaser.Math.Vector2(pointer.x, pointer.y);
    this.isTouching = true;
  }
  
  private onPointerMove(pointer: Phaser.Input.Pointer): void {
    if (this.isTouching) {
      this.currentTouch = new Phaser.Math.Vector2(pointer.x, pointer.y);
    }
  }
  
  private onPointerUp(): void {
    this.isTouching = false;
    this.touchStartPos = null;
    this.currentTouch = null;
  }
  
  getInput(): InputState {
    const state: InputState = {
      left: false,
      right: false,
      up: false,
      down: false,
      action: false,
    };
    
    // Keyboard
    state.left = this.cursors.left?.isDown || this.wasd.A.isDown;
    state.right = this.cursors.right?.isDown || this.wasd.D.isDown;
    state.up = this.cursors.up?.isDown || this.wasd.W.isDown;
    state.down = this.cursors.down?.isDown || this.wasd.S.isDown;
    state.action = this.cursors.space?.isDown || this.wasd.SPACE.isDown;
    
    // Touch - virtual joystick style
    if (this.isTouching && this.touchStartPos && this.currentTouch) {
      const dx = this.currentTouch.x - this.touchStartPos.x;
      const dy = this.currentTouch.y - this.touchStartPos.y;
      
      if (Math.abs(dx) > this.swipeThreshold) {
        state.left = dx < 0;
        state.right = dx > 0;
      }
      
      if (Math.abs(dy) > this.swipeThreshold) {
        state.up = dy < 0;
        state.down = dy > 0;
      }
      
      // Double-tap for action (simplified - detect quick tap)
      const dist = Phaser.Math.Distance.BetweenPoints(this.touchStartPos, this.currentTouch);
      if (dist < 10) {
        state.action = true;
      }
    }
    
    return state;
  }
  
  destroy(): void {
    this.scene.input.off('pointerdown', this.onPointerDown, this);
    this.scene.input.off('pointermove', this.onPointerMove, this);
    this.scene.input.off('pointerup', this.onPointerUp, this);
  }
}
```

**Virtual joystick overlay (optional):**
```typescript
// Add visual touch indicator
createTouchIndicator() {
  this.touchBase = this.add.circle(100, 500, 50, 0x333333, 0.5);
  this.touchKnob = this.add.circle(100, 500, 25, 0x666666, 0.8);
  this.touchBase.setVisible(false);
  this.touchKnob.setVisible(false);
  this.touchBase.setScrollFactor(0);
  this.touchKnob.setScrollFactor(0);
  this.touchBase.setDepth(1000);
  this.touchKnob.setDepth(1001);
}

// Show on touch start at touch position
// Hide on touch end
```

**Update Player to use InputManager:**
```typescript
// In Player update()
update(input: InputState, delta: number): void {
  const speed = SPEEDS.PLAYER * (delta / 1000);
  
  if (this.state === PlayerState.ON_BOUNDARY) {
    if (input.right || input.down) {
      this.edgePosition += speed / this.getPerimeter();
    } else if (input.left || input.up) {
      this.edgePosition -= speed / this.getPerimeter();
    }
    
    if (input.action) {
      this.state = PlayerState.DRAWING_LINE;
      this.emit('startDrawing', { x: this.x, y: this.y });
    }
  }
  // ... rest of movement
}
```

Output: Touch-friendly input system with swipe detection, works on mobile browsers.
```

---

## Stage 7: Character LoRA Training (Days 25-26)

```
Train character LoRAs for Crystal Arcade's image generation pipeline.

**Prerequisites:**
- ComfyUI or Automatic1111 with Kohya scripts
- SDXL base model (or Illustrious/Pony v6)
- GPU with 12GB+ VRAM (or RunPod for cloud)

**Free Tier Characters to Train:**
1. Luna - Gothic anime, mysterious stranger
2. Mika - Bright anime, bubbly idol  
3. Diana - Semi-realistic, confident temptress (mature 28)
4. Jade - Stylized, athletic tomboy

**For each character:**

**Step 1: Prepare Training Data**
- Collect 20-50 reference images defining:
  - Face structure
  - Body type
  - Hairstyle/color
  - Outfit themes
- Create captions for each image:
  ```
  luna, 1girl, gothic, dark hair, purple eyes, pale skin, mysterious expression
  ```

**Step 2: LoRA Training Config (kohya_ss)**
```yaml
# luna_lora_config.toml
[metadata]
name = "crystal_luna"
trigger = "ccluna"

[training]
base_model = "sdxl_base_1.0"
resolution = 1024
batch_size = 1
epochs = 10
learning_rate = 1e-4
text_encoder_lr = 5e-5
unet_lr = 1e-4
network_dim = 64
network_alpha = 32
scheduler = "cosine_with_restarts"

[dataset]
image_dir = "./training_data/luna"
caption_extension = ".txt"
```

**Step 3: Run Training**
```bash
# Using kohya_ss
accelerate launch train_network.py \
  --config_file="luna_lora_config.toml" \
  --output_dir="./output/luna" \
  --output_name="crystal_luna"
```

Training time: ~30-60 min per character on RTX 4090 / RunPod A100

**Step 4: Test LoRA**
```
Prompt: "ccluna, 1girl, gothic style, dark bedroom, sitting on bed, looking at viewer, masterpiece, best quality"
Negative: "worst quality, low quality, blurry, watermark"
LoRA strength: 0.7-0.9
```

Generate 10 test images, adjust if needed.

**Output per character:**
- LoRA file: crystal_{name}.safetensors
- Trigger word: cc{name}
- Recommended prompt template
- Sample images for verification

**Character Prompt Templates:**

**Luna:**
```
ccluna, 1girl, gothic anime style, long dark hair, purple eyes, pale skin, 
{pose}, {outfit}, {setting}, 
dramatic lighting, detailed, masterpiece, best quality
```

**Mika:**
```
ccmika, 1girl, bright anime style, pink hair with highlights, cheerful expression,
{pose}, idol outfit, {setting},
vibrant colors, energetic, masterpiece, best quality  
```

**Diana:**
```
ccdiana, 1girl, semi-realistic, mature woman (28), confident, elegant,
{pose}, {outfit}, {setting},
professional lighting, detailed skin, masterpiece, best quality
```

**Jade:**
```
ccjade, 1girl, athletic build, short hair, tomboy, toned,
{pose}, {outfit}, {setting},
dynamic pose, fit body, masterpiece, best quality
```

Output: 4 LoRA files with trigger words and prompt templates.
```

---

## Stage 8: Batch Image Generation (Days 27-28)

```
Generate 100 images for Crystal Arcade content library.

**Distribution:**
- Luna: 25 images (free tier)
- Mika: 25 images (free tier)
- Diana: 25 images (premium)
- Jade: 25 images (premium)

**Generation Settings:**
```
Model: SDXL 1.0 (or Illustrious XL)
Size: 1024x1536 (portrait) for reveal game
Steps: 30
CFG Scale: 7
Sampler: DPM++ 2M Karras
```

**Pose/Setting Variations per Character:**
1. Casual lounging
2. Standing confident
3. Sitting relaxed
4. Action/dynamic pose
5. Playful/teasing

**Batch Script (ComfyUI API):**
```python
import requests
import json
import os

COMFYUI_URL = "http://localhost:8188/prompt"
OUTPUT_DIR = "./generated"

characters = {
    "luna": {
        "lora": "crystal_luna.safetensors",
        "trigger": "ccluna",
        "base_prompt": "ccluna, 1girl, gothic anime style, long dark hair, purple eyes",
    },
    # ... other characters
}

poses = [
    "sitting on bed, relaxed",
    "standing confidently, hands on hips",
    "lounging on couch",
    "leaning against wall, smirking",
    "stretching, morning light",
]

settings = [
    "bedroom, dim lighting",
    "studio, professional lighting",
    "outdoor, sunset",
    "bathroom, steamy",
    "luxury apartment, night city view",
]

def generate_batch(character_id, count=25):
    char = characters[character_id]
    
    for i in range(count):
        pose = poses[i % len(poses)]
        setting = settings[i % len(settings)]
        
        prompt = f"{char['trigger']}, {char['base_prompt']}, {pose}, {setting}, masterpiece, best quality"
        
        workflow = create_workflow(prompt, char['lora'])
        
        response = requests.post(COMFYUI_URL, json={"prompt": workflow})
        # Handle response, save image
        
        print(f"Generated {character_id}_{i:03d}")

def create_workflow(prompt, lora):
    # Return ComfyUI workflow dict
    # ... workflow JSON structure
    pass

# Generate all
for char_id in characters:
    generate_batch(char_id, 25)
```

**Post-Processing Pipeline:**
```bash
#!/bin/bash
# post_process.sh

INPUT_DIR="./generated"
OUTPUT_DIR="./processed"

for file in $INPUT_DIR/*.png; do
    filename=$(basename "$file" .png)
    
    # 1. Upscale 2x with Real-ESRGAN
    realesrgan-ncnn-vulkan -i "$file" -o "$OUTPUT_DIR/hd/${filename}.png" -s 2
    
    # 2. Create web version (800px width)
    convert "$OUTPUT_DIR/hd/${filename}.png" -resize 800x "$OUTPUT_DIR/web/${filename}.webp"
    
    # 3. Add watermark to web version
    composite -gravity southeast -geometry +10+10 \
        watermark.png "$OUTPUT_DIR/web/${filename}.webp" "$OUTPUT_DIR/web/${filename}.webp"
    
done
```

**Upload to CDN:**
```bash
# Upload structure:
# /assets/images/characters/{character_id}/{index}.webp (web)
# /assets/images/characters/{character_id}/hd/{index}.webp (premium HD)

rclone sync ./processed/web bunny:crystalarcade-assets/assets/images/characters --include "*.webp"
rclone sync ./processed/hd bunny:crystalarcade-assets/assets/images/characters/hd --include "*.webp"
```

**Level Data Configuration:**
```json
// data/levels.json
{
  "levels": [
    { "id": 1, "character": "luna", "imageIndex": 0, "difficulty": 1 },
    { "id": 2, "character": "luna", "imageIndex": 1, "difficulty": 1 },
    { "id": 3, "character": "mika", "imageIndex": 0, "difficulty": 1 },
    // ... 100 levels total
  ],
  "characters": {
    "luna": { "name": "Luna", "tier": "free", "imageCount": 25 },
    "mika": { "name": "Mika", "tier": "free", "imageCount": 25 },
    "diana": { "name": "Diana", "tier": "premium", "imageCount": 25 },
    "jade": { "name": "Jade", "tier": "premium", "imageCount": 25 }
  }
}
```

Output: 100 processed images uploaded to CDN, level configuration complete.
```

---

## Verification Checklist

After completing all stages, verify:

```
[ ] Phaser game loads in browser
[ ] Player moves on boundary (keyboard)
[ ] Player can enter playfield and draw line
[ ] Line self-intersection triggers death
[ ] Polygon claiming calculates area
[ ] Claimed area reveals image beneath
[ ] Enemy bounces correctly
[ ] Enemy-trail collision works
[ ] Win condition triggers at 75%
[ ] Touch controls work on mobile
[ ] 4 LoRAs trained and tested
[ ] 100 images generated
[ ] Images uploaded to CDN
[ ] Images load in game from CDN
[ ] Game plays through 5+ levels successfully
```
