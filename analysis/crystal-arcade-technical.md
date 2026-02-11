# Crystal Arcade: Technical Architecture Document
## Gals Panic/Qix-Style Image Reveal Game

**Document Version:** 1.0  
**Date:** February 10, 2026  
**Purpose:** Technical deep dive for implementing a Qix/Gals Panic-style puzzle game with AI-generated pin-up reveals

---

## Table of Contents
1. [Game Mechanics Deep Dive](#1-game-mechanics-deep-dive)
2. [Framework Selection](#2-framework-selection)
3. [Progressive Reveal Architecture](#3-progressive-reveal-architecture)
4. [Image Optimization Strategy](#4-image-optimization-strategy)
5. [Technical Implementation](#5-technical-implementation)
6. [Development Timeline](#6-development-timeline)
7. [References & Resources](#7-references--resources)

---

## 1. Game Mechanics Deep Dive

### 1.1 The Qix/Gals Panic Gameplay Loop

**Core Loop (from original Qix, 1981):**
1. Player controls a marker that moves along edges of playfield
2. Player can "draw" lines (Stix) into unclaimed territory
3. Closing a shape claims that area (fills with color/reveals image)
4. Enemies threaten:
   - **Qix** (the abstract entity) - kills if it touches your drawing line
   - **Sparx** - patrol the edges, kill on contact
5. **Win condition:** Claim 75-80% of playfield (configurable 50-90%)

**Gals Panic Enhancements (1990):**
- Claimed areas reveal parts of an underlying image (photos/drawings of women)
- Timer-based gauge instead of pure percentage
- More complex enemy patterns
- Bonus symbols that modify gameplay
- Round ends when ~80% of silhouette is uncovered

### 1.2 What Makes It Addictive

| Element | Why It Works |
|---------|--------------|
| **Risk/Reward Tension** | Drawing slowly = 2x points but more danger |
| **Progressive Reveal** | Visual dopamine hit as image appears piece by piece |
| **Territory Control** | Primal satisfaction of "claiming" space |
| **Near-Miss Mechanics** | Close calls with enemies create adrenaline |
| **Percentage Counter** | Constant progress feedback (67%... 68%... 69%...) |
| **Variable Difficulty** | Each level adds more enemies, faster Qix |
| **Mastery Curve** | Easy to learn, hard to master route optimization |

### 1.3 Key Design Decisions for Crystal Arcade

```
+------------------+---------------------+---------------------------+
| Original Feature | Our Implementation  | Reasoning                 |
+------------------+---------------------+---------------------------+
| 75% to win       | 80% to reveal       | More image shown = better |
| Slow/Fast draw   | Single speed        | Simplify for mobile touch |
| Multiple Sparx   | 1-2 enemies         | Mobile-friendly difficulty|
| Timer pressure   | Optional timer      | Casual-friendly option    |
| Lives system     | Hearts + continues  | Monetizable continues     |
+------------------+---------------------+---------------------------+
```

---

## 2. Framework Selection

### 2.1 Options Comparison

| Framework | Pros | Cons | Best For |
|-----------|------|------|----------|
| **Phaser.js** | Full game engine, physics, tweens, particles, huge community, TypeScript support, mobile-optimized | Larger bundle (~1MB), learning curve | Full-featured games |
| **PixiJS** | Pure renderer, fastest 2D WebGL, tiny core (~100KB), flexible | No game logic built-in, DIY everything | Custom game engines |
| **Raw Canvas** | Zero dependencies, full control, smallest size | Everything manual, performance varies | Simple games only |

### 2.2 Recommendation: **Phaser 3.90+**

**Why Phaser wins for this project:**

1. **Built-in Touch Controls** - Phaser has excellent pointer event handling:
```javascript
// Works identically for mouse and touch
this.input.on('pointerdown', (pointer) => {
    this.player.startDrawing(pointer.x, pointer.y);
});

this.input.on('pointermove', (pointer) => {
    if (pointer.isDown) {
        this.player.continueLine(pointer.x, pointer.y);
    }
});
```

2. **Graphics API for Polygon Drawing** - Essential for Qix-style gameplay:
```javascript
// Draw the claimed territory
this.graphics = this.add.graphics();
this.graphics.fillStyle(0x00ff00, 0.5);
this.graphics.fillPoints(polygonPoints, true);

// Mask the reveal image
this.revealMask = this.make.graphics();
this.revealMask.fillPoints(claimedPoints, true);
this.revealImage.setMask(this.revealMask.createGeometryMask());
```

3. **Mobile Performance** - WebGL renderer with fallback
4. **Asset Loading** - Built-in loader for images, audio, spritesheets
5. **Tween System** - Smooth animations for reveals
6. **Scene Management** - Easy level transitions

### 2.3 Performance Benchmarks (Mobile)

| Device Type | Target FPS | Phaser Performance |
|-------------|------------|-------------------|
| iPhone 12+ | 60 | ✅ Solid 60fps |
| iPhone 8-11 | 60 | ✅ 55-60fps |
| iPhone 6-7 | 30-60 | ⚠️ 40-50fps (acceptable) |
| Android Mid-range | 60 | ✅ 50-60fps |
| Android Low-end | 30 | ⚠️ 30-40fps |

---

## 3. Progressive Reveal Architecture

### 3.1 How Original Gals Panic Did It

The original arcade game used **hardware sprite masking**:
- Background layer: The "reward" image
- Foreground layer: Solid color or pattern
- As areas claimed, foreground mask removed to show background

### 3.2 Modern Web Implementation: Mask-Based Reveal

**Architecture:**
```
┌─────────────────────────────────────┐
│         CANVAS LAYER STACK          │
├─────────────────────────────────────┤
│ Layer 4: UI (score, timer, %)       │
│ Layer 3: Enemies (Qix, Sparx)       │
│ Layer 2: Player + Drawing Line      │
│ Layer 1: Claimed Area (green)       │
│ Layer 0: Background Image (masked)  │
└─────────────────────────────────────┘
```

**Key Technique: Geometry Masking**

```javascript
class RevealSystem {
    constructor(scene) {
        this.scene = scene;
        this.claimedPolygons = [];
        this.totalArea = 0;
        
        // The image to reveal
        this.revealImage = scene.add.image(400, 300, 'pinup_001');
        this.revealImage.setVisible(false); // Hidden until revealed
        
        // The mask graphics object
        this.maskGraphics = scene.make.graphics();
        this.mask = this.maskGraphics.createGeometryMask();
        this.revealImage.setMask(this.mask);
        this.revealImage.setVisible(true);
    }
    
    claimArea(polygon) {
        // Add to claimed polygons
        this.claimedPolygons.push(polygon);
        
        // Redraw mask
        this.maskGraphics.clear();
        this.maskGraphics.fillStyle(0xffffff);
        
        for (const poly of this.claimedPolygons) {
            this.maskGraphics.fillPoints(poly.points, true);
        }
        
        // Calculate new percentage
        this.totalArea = this.calculateTotalArea();
        this.scene.events.emit('areaUpdated', this.totalArea);
    }
    
    calculateTotalArea() {
        // Polygon area calculation using Shoelace formula
        let total = 0;
        for (const poly of this.claimedPolygons) {
            total += this.shoelaceArea(poly.points);
        }
        const playFieldArea = 800 * 600; // Example dimensions
        return (total / playFieldArea) * 100;
    }
    
    shoelaceArea(points) {
        let area = 0;
        const n = points.length;
        for (let i = 0; i < n; i++) {
            const j = (i + 1) % n;
            area += points[i].x * points[j].y;
            area -= points[j].x * points[i].y;
        }
        return Math.abs(area / 2);
    }
}
```

### 3.3 Percentage vs Zone-Based Unlock

| Approach | Implementation | User Experience |
|----------|---------------|-----------------|
| **Percentage-based** | Track total claimed % | Classic feel, constant progress |
| **Zone-based** | Predefined "hot zones" | Strategic reveals of key areas |
| **Hybrid** | Both! | Best of both worlds |

**Recommendation: Hybrid Approach**
- Track overall % for level completion
- Define "bonus zones" that give extra points when revealed
- Strategic zones could overlay... interesting parts of the image

### 3.4 Making Reveals Rewarding

```javascript
// Celebratory effects when claiming territory
onAreaClaimed(percentage) {
    // Screen shake on large claims
    if (percentage >= 5) {
        this.cameras.main.shake(100, 0.005);
    }
    
    // Particles burst
    this.revealParticles.emitParticleAt(claimCenter.x, claimCenter.y, 20);
    
    // Sound effects scaled to claim size
    if (percentage >= 10) {
        this.sound.play('big_claim');
    } else {
        this.sound.play('small_claim', { volume: 0.5 + percentage * 0.05 });
    }
    
    // Milestone celebrations
    const milestones = [25, 50, 75, 80];
    for (const m of milestones) {
        if (this.prevTotal < m && this.totalClaimed >= m) {
            this.celebrateMilestone(m);
        }
    }
}

celebrateMilestone(percentage) {
    // Pause gameplay briefly
    this.tweens.add({
        targets: this.physics.world,
        timeScale: 0,
        duration: 500,
        yoyo: true
    });
    
    // Big text popup
    const text = this.add.text(400, 300, `${percentage}%!`, {
        fontSize: '128px',
        color: '#FFD700',
        stroke: '#000',
        strokeThickness: 8
    }).setOrigin(0.5);
    
    this.tweens.add({
        targets: text,
        scale: { from: 0.5, to: 1.5 },
        alpha: { from: 1, to: 0 },
        duration: 1000,
        onComplete: () => text.destroy()
    });
}
```

---

## 4. Image Optimization Strategy

### 4.1 Format Comparison for 2026

| Format | Browser Support | Compression | Animation | Alpha | Recommendation |
|--------|----------------|-------------|-----------|-------|----------------|
| **WebP** | 97%+ global | Excellent | Yes | Yes | ✅ Primary format |
| **AVIF** | 93%+ global | Best | Yes | Yes | ✅ Modern browsers |
| **JPEG** | 100% | Good | No | No | Fallback only |
| **PNG** | 100% | Poor | No | Yes | Source only |

### 4.2 Recommended Strategy: Progressive Enhancement

```javascript
// Image loading with format fallback
async function loadRevealImage(scene, key, basePath) {
    const formats = ['avif', 'webp', 'jpg'];
    
    for (const format of formats) {
        const url = `${basePath}.${format}`;
        const supported = await checkFormatSupport(format);
        
        if (supported) {
            scene.load.image(key, url);
            return;
        }
    }
}

// Format detection
async function checkFormatSupport(format) {
    const testImages = {
        webp: 'data:image/webp;base64,UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=',
        avif: 'data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUIAAADybWV0YQAAAAAAAAAoaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAGxpYmF2aWYAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAAB0AAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAIAAAACAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQ0MAAAAABNjb2xybmNseAACAAIAAYAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAACVtZGF0EgAKBzgABpAgMDQQEAoIBAABAAEAAQAAAB0gG'
    };
    
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = testImages[format];
    });
}
```

### 4.3 Image Sizing Strategy for 1000+ Images

**Storage Calculations:**
| Quality Tier | Dimensions | Avg File Size | 1000 Images |
|--------------|------------|---------------|-------------|
| Thumbnail | 200x300 | 15KB (WebP) | 15MB |
| Preview | 400x600 | 40KB (WebP) | 40MB |
| Full Game | 800x1200 | 100KB (WebP) | 100MB |
| HD Unlock | 1600x2400 | 300KB (WebP) | 300MB |

**Total CDN storage estimate: ~500MB for 1000 images with all tiers**

### 4.4 Lazy Loading Architecture

```javascript
class ImageManager {
    constructor() {
        this.cache = new Map();
        this.preloadQueue = [];
        this.maxCacheSize = 50; // Images in memory
    }
    
    async getImage(imageId) {
        // Check cache first
        if (this.cache.has(imageId)) {
            this.cache.get(imageId).lastAccess = Date.now();
            return this.cache.get(imageId).data;
        }
        
        // Load image
        const imageData = await this.loadImage(imageId);
        
        // Add to cache
        this.cache.set(imageId, {
            data: imageData,
            lastAccess: Date.now()
        });
        
        // Evict old entries if needed
        this.evictIfNeeded();
        
        return imageData;
    }
    
    preloadLevel(levelId, imageIds) {
        // Start loading next level's images in background
        for (const id of imageIds) {
            if (!this.cache.has(id)) {
                this.preloadQueue.push(id);
            }
        }
        this.processPreloadQueue();
    }
    
    async processPreloadQueue() {
        while (this.preloadQueue.length > 0) {
            const id = this.preloadQueue.shift();
            await this.getImage(id);
            // Small delay to not block main thread
            await new Promise(r => setTimeout(r, 100));
        }
    }
    
    evictIfNeeded() {
        if (this.cache.size <= this.maxCacheSize) return;
        
        // Find oldest accessed entry
        let oldest = null;
        let oldestTime = Infinity;
        
        for (const [key, value] of this.cache.entries()) {
            if (value.lastAccess < oldestTime) {
                oldestTime = value.lastAccess;
                oldest = key;
            }
        }
        
        if (oldest) {
            this.cache.delete(oldest);
        }
    }
}
```

---

## 5. Technical Implementation

### 5.1 Core Game Objects

```javascript
// Main game scene
class GameScene extends Phaser.Scene {
    create() {
        // Initialize systems
        this.revealSystem = new RevealSystem(this);
        this.player = new Player(this);
        this.enemyManager = new EnemyManager(this);
        this.lineDrawer = new LineDrawer(this);
        
        // Setup boundary polygon (the playfield edges)
        this.boundary = new Phaser.Geom.Polygon([
            new Phaser.Math.Vector2(50, 50),
            new Phaser.Math.Vector2(750, 50),
            new Phaser.Math.Vector2(750, 550),
            new Phaser.Math.Vector2(50, 550)
        ]);
        
        // Input handling
        this.setupInput();
        
        // Win condition check
        this.events.on('areaUpdated', (percentage) => {
            if (percentage >= 80) {
                this.levelComplete();
            }
        });
    }
    
    update(time, delta) {
        this.player.update(time, delta);
        this.enemyManager.update(time, delta);
        
        // Check collisions
        if (this.player.isDrawing) {
            this.checkLineCollisions();
        }
    }
}
```

### 5.2 Player Movement System

```javascript
class Player {
    constructor(scene) {
        this.scene = scene;
        this.x = 50;
        this.y = 50;
        this.speed = 200; // pixels per second
        this.isDrawing = false;
        this.currentLine = [];
        this.onBoundary = true;
        
        // Visual representation
        this.sprite = scene.add.circle(this.x, this.y, 8, 0x00ff00);
    }
    
    move(direction, delta) {
        const distance = this.speed * (delta / 1000);
        let newX = this.x;
        let newY = this.y;
        
        switch (direction) {
            case 'up': newY -= distance; break;
            case 'down': newY += distance; break;
            case 'left': newX -= distance; break;
            case 'right': newX += distance; break;
        }
        
        // Validate movement
        if (this.onBoundary) {
            // Can only move along boundary edges
            if (this.isOnBoundary(newX, newY)) {
                this.x = newX;
                this.y = newY;
            }
        } else if (this.isDrawing) {
            // Can move anywhere while drawing
            this.x = newX;
            this.y = newY;
            this.currentLine.push({ x: this.x, y: this.y });
        }
        
        this.sprite.setPosition(this.x, this.y);
    }
    
    startDrawing() {
        if (!this.onBoundary) return;
        
        this.isDrawing = true;
        this.onBoundary = false;
        this.currentLine = [{ x: this.x, y: this.y }];
    }
    
    finishDrawing() {
        if (!this.isDrawing) return;
        
        // Check if we've returned to boundary
        if (this.isOnBoundary(this.x, this.y)) {
            this.onBoundary = true;
            this.isDrawing = false;
            
            // Calculate claimed area
            const claimedPolygon = this.calculateClaimedArea();
            this.scene.revealSystem.claimArea(claimedPolygon);
            
            this.currentLine = [];
        }
    }
    
    isOnBoundary(x, y) {
        const boundary = this.scene.boundary;
        const points = boundary.points;
        const threshold = 3; // pixels
        
        for (let i = 0; i < points.length; i++) {
            const p1 = points[i];
            const p2 = points[(i + 1) % points.length];
            
            const dist = Phaser.Geom.Line.GetNearestPoint(
                new Phaser.Geom.Line(p1.x, p1.y, p2.x, p2.y),
                new Phaser.Geom.Point(x, y)
            );
            
            if (Phaser.Math.Distance.Between(x, y, dist.x, dist.y) < threshold) {
                return true;
            }
        }
        return false;
    }
}
```

### 5.3 Polygon Clipping (Using ClipperLib)

For complex polygon operations (union, difference), use **Javascript Clipper**:

```javascript
// npm install js-clipper or include from CDN

class PolygonOperations {
    constructor() {
        this.clipper = new ClipperLib.Clipper();
        this.scale = 100; // Integer scaling for precision
    }
    
    union(polygon1, polygon2) {
        const subj = this.toClipperPath(polygon1);
        const clip = this.toClipperPath(polygon2);
        const solution = new ClipperLib.Paths();
        
        this.clipper.Clear();
        this.clipper.AddPaths([subj], ClipperLib.PolyType.ptSubject, true);
        this.clipper.AddPaths([clip], ClipperLib.PolyType.ptClip, true);
        this.clipper.Execute(
            ClipperLib.ClipType.ctUnion,
            solution,
            ClipperLib.PolyFillType.pftNonZero,
            ClipperLib.PolyFillType.pftNonZero
        );
        
        return this.fromClipperPaths(solution);
    }
    
    toClipperPath(points) {
        return points.map(p => ({
            X: Math.round(p.x * this.scale),
            Y: Math.round(p.y * this.scale)
        }));
    }
    
    fromClipperPaths(paths) {
        return paths.map(path => 
            path.map(p => ({
                x: p.X / this.scale,
                y: p.Y / this.scale
            }))
        );
    }
}
```

### 5.4 Touch Controls Implementation

```javascript
class TouchControls {
    constructor(scene) {
        this.scene = scene;
        this.virtualPad = null;
        this.drawButton = null;
        
        this.setupControls();
    }
    
    setupControls() {
        // Virtual joystick for movement
        this.virtualPad = this.scene.plugins.get('rexVirtualJoystick').add(this.scene, {
            x: 100,
            y: 500,
            radius: 60,
            base: this.scene.add.circle(0, 0, 60, 0x888888, 0.5),
            thumb: this.scene.add.circle(0, 0, 30, 0xcccccc, 0.8),
        });
        
        // Draw button
        this.drawButton = this.scene.add.circle(700, 500, 50, 0xff0000, 0.8)
            .setInteractive()
            .on('pointerdown', () => this.scene.player.startDrawing())
            .on('pointerup', () => this.scene.player.finishDrawing());
        
        // Alternative: Swipe to draw
        this.setupSwipeControls();
    }
    
    setupSwipeControls() {
        let startPoint = null;
        
        this.scene.input.on('pointerdown', (pointer) => {
            startPoint = { x: pointer.x, y: pointer.y };
            
            // Check if on boundary - auto start drawing
            if (this.scene.player.isNearBoundary(pointer.x, pointer.y)) {
                this.scene.player.teleportTo(pointer.x, pointer.y);
                this.scene.player.startDrawing();
            }
        });
        
        this.scene.input.on('pointermove', (pointer) => {
            if (pointer.isDown && this.scene.player.isDrawing) {
                // Move player to pointer position (constrained)
                this.scene.player.moveTo(pointer.x, pointer.y);
            }
        });
        
        this.scene.input.on('pointerup', () => {
            if (this.scene.player.isDrawing) {
                this.scene.player.finishDrawing();
            }
        });
    }
    
    getDirection() {
        if (!this.virtualPad) return null;
        
        const force = this.virtualPad.force;
        if (force < 30) return null; // Dead zone
        
        const angle = this.virtualPad.angle;
        
        // Convert to 4-way direction
        if (angle >= -45 && angle < 45) return 'right';
        if (angle >= 45 && angle < 135) return 'down';
        if (angle >= -135 && angle < -45) return 'up';
        return 'left';
    }
}
```

### 5.5 Project Structure

```
crystal-arcade/
├── src/
│   ├── main.js                 # Entry point
│   ├── config.js               # Phaser config
│   ├── scenes/
│   │   ├── BootScene.js        # Asset preloading
│   │   ├── MenuScene.js        # Main menu
│   │   ├── GameScene.js        # Core gameplay
│   │   ├── LevelCompleteScene.js
│   │   └── GalleryScene.js     # Unlocked images
│   ├── objects/
│   │   ├── Player.js           # Player movement/drawing
│   │   ├── Enemy.js            # Qix behavior
│   │   ├── Sparx.js            # Edge-patrolling enemy
│   │   └── Boundary.js         # Playfield boundary
│   ├── systems/
│   │   ├── RevealSystem.js     # Image masking/reveal
│   │   ├── PolygonSystem.js    # Area calculations
│   │   ├── CollisionSystem.js  # Hit detection
│   │   └── AudioSystem.js      # Sound management
│   ├── ui/
│   │   ├── TouchControls.js    # Mobile input
│   │   ├── HUD.js              # Score/percentage display
│   │   └── Animations.js       # Celebration effects
│   └── utils/
│       ├── ImageManager.js     # Image loading/caching
│       └── PolygonMath.js      # Geometry helpers
├── assets/
│   ├── images/
│   │   ├── pinups/             # Reveal images
│   │   │   ├── webp/
│   │   │   └── avif/
│   │   └── ui/                 # UI elements
│   ├── audio/
│   │   ├── sfx/
│   │   └── music/
│   └── data/
│       └── levels.json         # Level configurations
├── public/
│   └── index.html
├── package.json
├── vite.config.js              # Or webpack
└── README.md
```

---

## 6. Development Timeline

### 6.1 Phase Breakdown

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Phase 1: Core Engine** | 2-3 weeks | Player movement, boundary system, basic drawing, polygon claiming |
| **Phase 2: Enemies** | 1-2 weeks | Qix AI, Sparx patrolling, collision detection, death/respawn |
| **Phase 3: Reveal System** | 1-2 weeks | Image masking, progressive reveal, percentage tracking |
| **Phase 4: Polish** | 2-3 weeks | Touch controls, animations, sound, particles, UI |
| **Phase 5: Content** | 1-2 weeks | Level design, difficulty curve, 10+ test images |
| **Phase 6: Testing** | 1-2 weeks | Mobile testing, performance optimization, bug fixes |

**Total Estimated Time: 8-14 weeks** (solo developer)  
**With 2-person team: 5-8 weeks**

### 6.2 MVP Feature Set

**Must Have (MVP):**
- [ ] Player movement along boundary
- [ ] Line drawing into territory
- [ ] Area claiming with polygon fill
- [ ] Single enemy (Qix-like)
- [ ] Image reveal via masking
- [ ] 80% completion = level win
- [ ] 5 playable levels
- [ ] Touch controls (mobile)
- [ ] Basic sound effects

**Should Have (v1.0):**
- [ ] Sparx enemies
- [ ] Score system
- [ ] Lives/continues
- [ ] Level select
- [ ] Gallery of unlocked images
- [ ] Save progress (localStorage)
- [ ] 10+ images

**Nice to Have (v1.5+):**
- [ ] Multiple game modes
- [ ] Leaderboards
- [ ] Daily challenges
- [ ] Achievement system
- [ ] Image packs (DLC)
- [ ] Social sharing

---

## 7. References & Resources

### 7.1 Open Source Implementations to Study

| Project | Language | Notes |
|---------|----------|-------|
| [qixxy](https://github.com/thenanisore/qixxy) | Scala/LibGDX | Qix clone, good algorithm reference |
| [quix](https://github.com/SirWumpus/quix) | C | Unix terminal Qix, core logic reference |

### 7.2 Libraries & Tools

| Library | Purpose | URL |
|---------|---------|-----|
| Phaser 3 | Game framework | https://phaser.io |
| Javascript Clipper | Polygon operations | https://sourceforge.net/projects/jsclipper/ |
| Howler.js | Audio (if not using Phaser's) | https://howlerjs.com |
| rexUI | Phaser UI plugins | https://rexrainbow.github.io/phaser3-rex-notes/ |

### 7.3 Algorithm References

**Polygon Area (Shoelace Formula):**
```javascript
function polygonArea(vertices) {
    let area = 0;
    const n = vertices.length;
    for (let i = 0; i < n; i++) {
        const j = (i + 1) % n;
        area += vertices[i].x * vertices[j].y;
        area -= vertices[j].x * vertices[i].y;
    }
    return Math.abs(area / 2);
}
```

**Point in Polygon (Ray Casting):**
```javascript
function pointInPolygon(point, polygon) {
    let inside = false;
    const n = polygon.length;
    
    for (let i = 0, j = n - 1; i < n; j = i++) {
        const xi = polygon[i].x, yi = polygon[i].y;
        const xj = polygon[j].x, yj = polygon[j].y;
        
        if (((yi > point.y) !== (yj > point.y)) &&
            (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi)) {
            inside = !inside;
        }
    }
    return inside;
}
```

### 7.4 Image Sources for Testing

During development, use placeholder/stock images. For production with AI pin-ups:
- Generate via Stable Diffusion XL or similar
- Ensure consistent style/quality
- Pre-process to game resolution
- Convert to WebP/AVIF with quality ~80

---

## Appendix A: Phaser Quick Start

```javascript
// package.json dependencies
{
    "dependencies": {
        "phaser": "^3.90.0"
    },
    "devDependencies": {
        "vite": "^5.0.0"
    }
}

// src/main.js
import Phaser from 'phaser';
import { GameScene } from './scenes/GameScene';

const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'game-container',
    backgroundColor: '#1a1a2e',
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    scene: [GameScene],
    physics: {
        default: 'arcade',
        arcade: {
            debug: true // Set false for production
        }
    },
    input: {
        activePointers: 2 // Support multi-touch
    }
};

new Phaser.Game(config);
```

---

## Appendix B: Performance Optimization Checklist

- [ ] Use texture atlases for UI elements
- [ ] Limit simultaneous particles (max 50-100)
- [ ] Use object pools for enemies/effects
- [ ] WebP images with quality 80 (not 100)
- [ ] Lazy load images beyond current level
- [ ] Disable debug physics in production
- [ ] Use `visible = false` instead of `destroy()` for recycled objects
- [ ] Test on low-end Android before release
- [ ] Monitor FPS with `scene.game.loop.actualFps`
- [ ] Consider reducing game resolution on low-end devices

---

*Document prepared for Crystal Arcade development planning. Implementation decisions should be validated through prototyping.*
