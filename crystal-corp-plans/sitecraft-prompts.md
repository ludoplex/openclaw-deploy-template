# Sitecraft Agent Stage Prompts — Crystal Corp

Ready-to-paste prompts for website and legal implementation. Each prompt is self-contained.

---

## Stage 1: Domain Registration (Day 1)

```
Register the domain crystalarcade.gg via Njalla for the Crystal Arcade adult gaming site.

**Why Njalla:**
- Maximum privacy — they own the domain on your behalf
- No WHOIS exposure
- Accepts crypto (optional)

**Registration Steps:**
1. Go to njal.la
2. Search for: crystalarcade.gg
3. If unavailable, alternatives: crystalarcade.io, playcrystalarcade.gg, crystal-arcade.gg
4. Complete registration (~$25/year for .gg)
5. After registration, configure DNS:
   - Go to domain settings
   - Set nameservers to Cloudflare:
     - [NS1 from Cloudflare - e.g., ada.ns.cloudflare.com]
     - [NS2 from Cloudflare - e.g., bob.ns.cloudflare.com]

**Verification:**
- Wait for propagation (up to 48h, usually faster)
- Verify with: dig crystalarcade.gg NS
- Confirm Cloudflare shows "Active" status

**Credentials:**
- Store Njalla login in Bitwarden vault "Crystal Corp Operations"
- Enable 2FA on Njalla account

Output: Confirmed domain, nameserver configuration, propagation status.
```

---

## Stage 2: Astro Project Initialization (Day 2)

```
Initialize Astro 4.x project for Crystal Arcade static website.

**Create Project:**
```bash
npm create astro@latest crystal-arcade -- --template minimal --typescript strict
cd crystal-arcade
npm install
```

**Install Dependencies:**
```bash
# Styling
npm install tailwindcss @astrojs/tailwind

# Image optimization
npm install @astrojs/image sharp

# SEO
npm install astro-seo

# Icons
npm install astro-icon
```

**Configure astro.config.mjs:**
```javascript
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://crystalarcade.gg',
  integrations: [tailwind()],
  output: 'static',
  build: {
    assets: 'assets'
  },
  vite: {
    build: {
      cssMinify: true,
      minify: 'terser'
    }
  }
});
```

**Create Directory Structure:**
```
src/
├── components/
├── layouts/
│   └── BaseLayout.astro
├── pages/
│   └── index.astro
├── styles/
│   └── global.css
└── content/
    └── characters/
```

**tailwind.config.cjs:**
```javascript
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        crystal: {
          bg: '#0a0a0f',
          surface: '#1a1a24',
          primary: '#ff4d6d',
          secondary: '#7c3aed',
          accent: '#00d4ff'
        }
      },
      fontFamily: {
        display: ['Orbitron', 'sans-serif'],
        body: ['Inter', 'sans-serif']
      }
    }
  },
  plugins: []
};
```

**Verify:**
```bash
npm run dev
# Should start on localhost:4321
```

Output: Project structure, configuration files, dev server running.
```

---

## Stage 3: Base Layout & Theme (Day 3)

```
Create the base layout and dark theme for Crystal Arcade.

**src/layouts/BaseLayout.astro:**
```astro
---
import '../styles/global.css';

interface Props {
  title: string;
  description?: string;
}

const { title, description = 'Crystal Arcade - Retro puzzle gaming with stunning visuals' } = Astro.props;
---

<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content={description}>
  <title>{title} | Crystal Arcade</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
  
  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  
  <!-- Open Graph -->
  <meta property="og:title" content={title}>
  <meta property="og:description" content={description}>
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://crystalarcade.gg/og-image.jpg">
</head>
<body class="bg-crystal-bg text-white min-h-screen font-body">
  <header class="border-b border-white/10">
    <nav class="container mx-auto px-4 py-4 flex justify-between items-center">
      <a href="/" class="font-display text-2xl font-bold text-crystal-primary">
        Crystal Arcade
      </a>
      <div class="flex gap-6 items-center">
        <a href="/characters" class="hover:text-crystal-primary transition">Characters</a>
        <a href="/faq" class="hover:text-crystal-primary transition">FAQ</a>
        <a href="#play" class="bg-crystal-primary px-4 py-2 rounded-lg font-semibold hover:bg-crystal-primary/80 transition">
          Play Now
        </a>
      </div>
    </nav>
  </header>
  
  <main>
    <slot />
  </main>
  
  <footer class="border-t border-white/10 mt-20 py-8">
    <div class="container mx-auto px-4">
      <div class="flex flex-wrap justify-between gap-8">
        <div>
          <h3 class="font-display text-lg mb-4">Crystal Arcade</h3>
          <p class="text-gray-400 max-w-xs">Retro puzzle gaming reimagined with stunning AI-generated artwork.</p>
        </div>
        <div>
          <h4 class="font-semibold mb-4">Legal</h4>
          <ul class="space-y-2 text-gray-400">
            <li><a href="/terms" class="hover:text-white">Terms of Service</a></li>
            <li><a href="/privacy" class="hover:text-white">Privacy Policy</a></li>
            <li><a href="/2257" class="hover:text-white">18 U.S.C. § 2257</a></li>
            <li><a href="/dmca" class="hover:text-white">DMCA</a></li>
          </ul>
        </div>
        <div>
          <h4 class="font-semibold mb-4">Community</h4>
          <ul class="space-y-2 text-gray-400">
            <li><a href="https://discord.gg/crystalarcade" class="hover:text-white">Discord</a></li>
            <li><a href="https://twitter.com/CrystalArcade" class="hover:text-white">Twitter</a></li>
          </ul>
        </div>
      </div>
      <div class="mt-8 pt-8 border-t border-white/10 text-center text-gray-500">
        <p>© 2026 Crystal Corp. Adults only (18+). All rights reserved.</p>
      </div>
    </div>
  </footer>
</body>
</html>
```

**src/styles/global.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    scroll-behavior: smooth;
  }
  
  body {
    @apply antialiased;
  }
  
  ::selection {
    @apply bg-crystal-primary/30;
  }
}

@layer components {
  .btn-primary {
    @apply bg-crystal-primary px-6 py-3 rounded-lg font-semibold 
           hover:bg-crystal-primary/80 transition transform hover:scale-105;
  }
  
  .card {
    @apply bg-crystal-surface rounded-xl p-6 border border-white/5;
  }
}
```

Output: Complete BaseLayout.astro, global.css, responsive header/footer.
```

---

## Stage 4: Landing Page (Day 4)

```
Build the Crystal Arcade landing page with hero, features, and CTA sections.

**src/pages/index.astro:**
```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="Home">
  <!-- Hero Section -->
  <section class="relative py-20 overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-b from-crystal-primary/20 to-transparent"></div>
    <div class="container mx-auto px-4 relative z-10">
      <div class="max-w-3xl mx-auto text-center">
        <h1 class="font-display text-5xl md:text-7xl font-bold mb-6">
          <span class="text-crystal-primary">Reveal</span> the Beauty
        </h1>
        <p class="text-xl text-gray-300 mb-8">
          Classic Qix-style puzzle gameplay meets stunning AI-generated pin-up art. 
          Claim territory, reveal images, and unlock exclusive characters.
        </p>
        <div class="flex gap-4 justify-center">
          <a href="#play" class="btn-primary text-lg">
            Play Free Demo
          </a>
          <a href="/characters" class="border border-white/20 px-6 py-3 rounded-lg hover:bg-white/5 transition">
            View Characters
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- How It Works -->
  <section class="py-20">
    <div class="container mx-auto px-4">
      <h2 class="font-display text-3xl font-bold text-center mb-12">How It Works</h2>
      <div class="grid md:grid-cols-3 gap-8">
        <div class="card text-center">
          <div class="text-4xl mb-4">🎮</div>
          <h3 class="font-display text-xl mb-2">Draw Lines</h3>
          <p class="text-gray-400">Navigate the playfield and draw lines to claim territory. Classic Qix gameplay perfected.</p>
        </div>
        <div class="card text-center">
          <div class="text-4xl mb-4">✨</div>
          <h3 class="font-display text-xl mb-2">Reveal Art</h3>
          <p class="text-gray-400">Each area you claim reveals part of a stunning AI-generated image beneath.</p>
        </div>
        <div class="card text-center">
          <div class="text-4xl mb-4">🏆</div>
          <h3 class="font-display text-xl mb-2">Unlock More</h3>
          <p class="text-gray-400">Progress through levels to unlock new characters and exclusive content.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Character Preview -->
  <section class="py-20 bg-crystal-surface/50">
    <div class="container mx-auto px-4">
      <h2 class="font-display text-3xl font-bold text-center mb-4">Meet the Characters</h2>
      <p class="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
        18+ unique characters, each with their own personality and style. 
        Start with our free tier and unlock premium characters with a subscription.
      </p>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <!-- Character cards will be populated here -->
        <div class="aspect-[3/4] rounded-xl bg-gradient-to-br from-crystal-primary/20 to-crystal-secondary/20 flex items-center justify-center">
          <span class="text-gray-500">Luna</span>
        </div>
        <div class="aspect-[3/4] rounded-xl bg-gradient-to-br from-crystal-primary/20 to-crystal-secondary/20 flex items-center justify-center">
          <span class="text-gray-500">Mika</span>
        </div>
        <div class="aspect-[3/4] rounded-xl bg-gradient-to-br from-crystal-primary/20 to-crystal-secondary/20 flex items-center justify-center">
          <span class="text-gray-500">Diana</span>
        </div>
        <div class="aspect-[3/4] rounded-xl bg-gradient-to-br from-crystal-primary/20 to-crystal-secondary/20 flex items-center justify-center">
          <span class="text-gray-500">Jade</span>
        </div>
      </div>
      <div class="text-center mt-8">
        <a href="/characters" class="text-crystal-primary hover:underline">View all characters →</a>
      </div>
    </div>
  </section>

  <!-- Pricing Preview -->
  <section class="py-20">
    <div class="container mx-auto px-4">
      <h2 class="font-display text-3xl font-bold text-center mb-12">Choose Your Experience</h2>
      <div class="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
        <div class="card">
          <h3 class="font-display text-xl mb-2">Free</h3>
          <p class="text-3xl font-bold mb-4">$0</p>
          <ul class="space-y-2 text-gray-400 mb-6">
            <li>✓ 4 characters</li>
            <li>✓ 5 plays/day</li>
            <li>✓ Softcore content</li>
          </ul>
          <a href="#play" class="block text-center border border-white/20 py-2 rounded-lg hover:bg-white/5">
            Play Free
          </a>
        </div>
        <div class="card border-crystal-primary relative">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-crystal-primary px-3 py-1 rounded-full text-sm font-semibold">
            Popular
          </div>
          <h3 class="font-display text-xl mb-2">Basic</h3>
          <p class="text-3xl font-bold mb-4">$9.99<span class="text-lg text-gray-400">/mo</span></p>
          <ul class="space-y-2 text-gray-400 mb-6">
            <li>✓ 12+ characters</li>
            <li>✓ Unlimited plays</li>
            <li>✓ Explicit content</li>
            <li>✓ Discord access</li>
          </ul>
          <a href="#subscribe" class="btn-primary block text-center">
            Subscribe
          </a>
        </div>
        <div class="card">
          <h3 class="font-display text-xl mb-2">Premium</h3>
          <p class="text-3xl font-bold mb-4">$19.99<span class="text-lg text-gray-400">/mo</span></p>
          <ul class="space-y-2 text-gray-400 mb-6">
            <li>✓ All 18+ characters</li>
            <li>✓ Early access</li>
            <li>✓ HD downloads</li>
            <li>✓ Request priority</li>
          </ul>
          <a href="#subscribe" class="block text-center border border-white/20 py-2 rounded-lg hover:bg-white/5">
            Go Premium
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Email Capture -->
  <section class="py-20 bg-gradient-to-r from-crystal-primary/20 to-crystal-secondary/20">
    <div class="container mx-auto px-4 text-center">
      <h2 class="font-display text-3xl font-bold mb-4">Get Early Access</h2>
      <p class="text-gray-300 mb-8 max-w-xl mx-auto">
        Join our newsletter for launch updates, exclusive previews, and special offers.
      </p>
      <form class="flex gap-4 max-w-md mx-auto" id="email-form">
        <input 
          type="email" 
          placeholder="your@email.com" 
          class="flex-1 px-4 py-3 rounded-lg bg-crystal-bg border border-white/20 focus:border-crystal-primary outline-none"
          required
        >
        <button type="submit" class="btn-primary">
          Subscribe
        </button>
      </form>
    </div>
  </section>
</BaseLayout>
```

Output: Complete landing page with all sections, responsive design, optimized for conversion.
```

---

## Stage 5: Age Verification Gate (Day 10)

```
Implement age verification gate for Crystal Arcade adult content.

**src/components/AgeGate.astro:**
```astro
---
// Server-side check not possible with static site
// This is client-side verification + cookie
---

<div id="age-gate" class="fixed inset-0 bg-crystal-bg z-50 flex items-center justify-center p-4">
  <div class="bg-crystal-surface rounded-2xl p-8 max-w-md w-full text-center border border-white/10">
    <div class="text-6xl mb-4">🔞</div>
    <h2 class="font-display text-2xl font-bold mb-4">Age Verification Required</h2>
    <p class="text-gray-400 mb-6">
      Crystal Arcade contains adult content intended for viewers 18 years of age or older.
      By entering, you confirm you are of legal age in your jurisdiction.
    </p>
    <div class="space-y-4">
      <button 
        id="age-confirm" 
        class="btn-primary w-full text-lg"
      >
        I am 18 or older — Enter
      </button>
      <button 
        id="age-deny"
        class="w-full py-3 border border-white/20 rounded-lg hover:bg-white/5 transition"
      >
        I am under 18 — Exit
      </button>
    </div>
    <p class="text-xs text-gray-500 mt-6">
      By entering, you agree to our <a href="/terms" class="underline">Terms of Service</a> 
      and <a href="/privacy" class="underline">Privacy Policy</a>.
    </p>
  </div>
</div>

<script>
  const COOKIE_NAME = 'crystal_age_verified';
  const COOKIE_DAYS = 30;
  
  function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
  }
  
  function setCookie(name: string, value: string, days: number): void {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
  }
  
  const ageGate = document.getElementById('age-gate');
  const confirmBtn = document.getElementById('age-confirm');
  const denyBtn = document.getElementById('age-deny');
  
  // Check if already verified
  if (getCookie(COOKIE_NAME) === 'true') {
    ageGate?.remove();
  }
  
  confirmBtn?.addEventListener('click', () => {
    setCookie(COOKIE_NAME, 'true', COOKIE_DAYS);
    localStorage.setItem('crystal_age_verified', 'true');
    ageGate?.classList.add('opacity-0', 'transition-opacity', 'duration-300');
    setTimeout(() => ageGate?.remove(), 300);
  });
  
  denyBtn?.addEventListener('click', () => {
    window.location.href = 'https://google.com';
  });
</script>

<style>
  #age-gate {
    backdrop-filter: blur(8px);
  }
</style>
```

**Usage in BaseLayout.astro:**
Add before closing </body>:
```astro
import AgeGate from '../components/AgeGate.astro';
---
...
<AgeGate />
</body>
```

**Exempt pages (legal pages should be accessible):**
Create a prop to disable age gate on /terms, /privacy, /dmca, /2257.

Output: Age gate component, cookie handling, exempt page logic.
```

---

## Stage 6: Legal Pages (Days 8-12)

```
Create all required legal pages for Crystal Arcade.

**src/layouts/LegalLayout.astro:**
```astro
---
import BaseLayout from './BaseLayout.astro';

interface Props {
  title: string;
  lastUpdated: string;
}

const { title, lastUpdated } = Astro.props;
---

<BaseLayout title={title} exemptFromAgeGate={true}>
  <div class="container mx-auto px-4 py-12">
    <div class="max-w-3xl mx-auto">
      <h1 class="font-display text-4xl font-bold mb-4">{title}</h1>
      <p class="text-gray-400 mb-8">Last updated: {lastUpdated}</p>
      <div class="prose prose-invert prose-lg max-w-none">
        <slot />
      </div>
    </div>
  </div>
</BaseLayout>
```

**src/pages/terms.astro:**
```astro
---
import LegalLayout from '../layouts/LegalLayout.astro';
---

<LegalLayout title="Terms of Service" lastUpdated="February 2026">
  <h2>1. Acceptance of Terms</h2>
  <p>
    By accessing Crystal Arcade ("the Service"), you agree to be bound by these Terms of Service.
    If you do not agree, do not use the Service.
  </p>
  
  <h2>2. Age Requirement</h2>
  <p>
    You must be at least 18 years of age (or the age of majority in your jurisdiction) to use this Service.
    By using Crystal Arcade, you represent and warrant that you meet this requirement.
  </p>
  
  <h2>3. Account Registration</h2>
  <p>
    You are responsible for maintaining the confidentiality of your account credentials.
    You agree to notify us immediately of any unauthorized use.
  </p>
  
  <h2>4. Subscription and Payments</h2>
  <p>
    Paid subscriptions are billed monthly or annually. You may cancel at any time.
    Refunds are available within 7 days of initial purchase for first-time subscribers only.
  </p>
  
  <h2>5. Content Ownership</h2>
  <p>
    All content, including AI-generated artwork, is owned by Crystal Corp.
    Subscribers may download content for personal use only.
    Redistribution, resale, or commercial use is prohibited.
  </p>
  
  <h2>6. Prohibited Conduct</h2>
  <p>You agree not to:</p>
  <ul>
    <li>Share or redistribute premium content</li>
    <li>Attempt to reverse-engineer the Service</li>
    <li>Use automated tools to access the Service</li>
    <li>Harass other users or staff</li>
  </ul>
  
  <h2>7. Termination</h2>
  <p>
    We may terminate your access for violation of these terms.
    Upon termination, your right to use the Service ceases immediately.
  </p>
  
  <h2>8. Disclaimer of Warranties</h2>
  <p>
    The Service is provided "as is" without warranties of any kind.
    We do not guarantee uninterrupted or error-free service.
  </p>
  
  <h2>9. Limitation of Liability</h2>
  <p>
    Crystal Corp shall not be liable for any indirect, incidental, or consequential damages.
    Our total liability is limited to the amount you paid in the past 12 months.
  </p>
  
  <h2>10. Governing Law</h2>
  <p>
    These terms are governed by the laws of the State of Wyoming, USA.
  </p>
  
  <h2>11. Contact</h2>
  <p>
    For questions about these terms, contact: legal@crystalarcade.gg
  </p>
</LegalLayout>
```

**src/pages/privacy.astro:**
```astro
---
import LegalLayout from '../layouts/LegalLayout.astro';
---

<LegalLayout title="Privacy Policy" lastUpdated="February 2026">
  <h2>1. Information We Collect</h2>
  <p>We collect:</p>
  <ul>
    <li><strong>Account information:</strong> Email address, username, password hash</li>
    <li><strong>Payment information:</strong> Processed by third-party providers (SubscribeStar)</li>
    <li><strong>Usage data:</strong> Game progress, preferences, analytics</li>
    <li><strong>Device information:</strong> Browser type, IP address, device identifiers</li>
  </ul>
  
  <h2>2. How We Use Information</h2>
  <p>We use your information to:</p>
  <ul>
    <li>Provide and improve the Service</li>
    <li>Process payments and subscriptions</li>
    <li>Send service-related communications</li>
    <li>Respond to support requests</li>
  </ul>
  
  <h2>3. Data Sharing</h2>
  <p>
    We do not sell your personal information.
    We may share data with service providers (payment processors, analytics) as necessary.
  </p>
  
  <h2>4. Cookies</h2>
  <p>
    We use cookies for authentication, preferences, and analytics.
    You can disable cookies in your browser settings.
  </p>
  
  <h2>5. Your Rights (GDPR/CCPA)</h2>
  <p>You have the right to:</p>
  <ul>
    <li>Access your personal data</li>
    <li>Request correction or deletion</li>
    <li>Object to processing</li>
    <li>Data portability</li>
    <li>Opt-out of marketing communications</li>
  </ul>
  
  <h2>6. Data Retention</h2>
  <p>
    We retain account data while your account is active.
    After deletion request, data is removed within 30 days.
  </p>
  
  <h2>7. Security</h2>
  <p>
    We implement industry-standard security measures.
    However, no method of transmission is 100% secure.
  </p>
  
  <h2>8. Contact</h2>
  <p>
    Privacy inquiries: privacy@crystalarcade.gg
  </p>
</LegalLayout>
```

**src/pages/2257.astro:**
```astro
---
import LegalLayout from '../layouts/LegalLayout.astro';
---

<LegalLayout title="18 U.S.C. § 2257 Compliance Statement" lastUpdated="February 2026">
  <h2>Record-Keeping Requirements Compliance Statement</h2>
  
  <p>
    All visual content appearing on Crystal Arcade (crystalarcade.gg) is 
    <strong>computer-generated imagery (CGI)</strong> created using artificial intelligence 
    image generation technology. No actual human beings were photographed or filmed in the 
    creation of any content on this website.
  </p>
  
  <p>
    Pursuant to 18 U.S.C. § 2257, the record-keeping requirements do not apply to 
    computer-generated images that do not depict actual human beings.
  </p>
  
  <h2>Content Classification</h2>
  <p>
    All artwork and images on this website are:
  </p>
  <ul>
    <li>100% AI-generated using Stable Diffusion and similar technologies</li>
    <li>Not based on or depicting any real individuals</li>
    <li>Created without the involvement of human models or performers</li>
    <li>Fictional characters and artistic representations only</li>
  </ul>
  
  <h2>Custodian of Records</h2>
  <p>
    For any inquiries regarding this compliance statement:<br>
    Crystal Corp<br>
    [Registered Agent Address - Wyoming]<br>
    legal@crystalarcade.gg
  </p>
</LegalLayout>
```

**src/pages/dmca.astro:**
```astro
---
import LegalLayout from '../layouts/LegalLayout.astro';
---

<LegalLayout title="DMCA Policy" lastUpdated="February 2026">
  <h2>Digital Millennium Copyright Act Notice</h2>
  
  <p>
    Crystal Corp respects the intellectual property rights of others. 
    If you believe that content on Crystal Arcade infringes your copyright, 
    please submit a DMCA takedown notice.
  </p>
  
  <h2>Designated Agent</h2>
  <p>
    DMCA notices should be sent to our designated agent:<br><br>
    Crystal Corp DMCA Agent<br>
    [Registered Agent Address]<br>
    Email: dmca@crystalarcade.gg
  </p>
  
  <h2>Required Information</h2>
  <p>Your notice must include:</p>
  <ol>
    <li>Your physical or electronic signature</li>
    <li>Identification of the copyrighted work claimed to be infringed</li>
    <li>Identification of the material to be removed (URL)</li>
    <li>Your contact information (address, phone, email)</li>
    <li>A statement of good faith belief that use is not authorized</li>
    <li>A statement under penalty of perjury that the information is accurate</li>
  </ol>
  
  <h2>Counter-Notification</h2>
  <p>
    If you believe your content was removed in error, you may submit a counter-notification
    with the required information as specified in 17 U.S.C. § 512(g).
  </p>
  
  <h2>Repeat Infringers</h2>
  <p>
    We will terminate accounts of repeat infringers in appropriate circumstances.
  </p>
</LegalLayout>
```

Output: All four legal pages (terms, privacy, 2257, dmca) with proper layout and content.
```

---

## Stage 7: Cookie Consent Banner (Day 10)

```
Create GDPR-compliant cookie consent banner.

**src/components/CookieConsent.astro:**
```astro
<div id="cookie-banner" class="fixed bottom-0 left-0 right-0 bg-crystal-surface border-t border-white/10 p-4 z-40 hidden">
  <div class="container mx-auto flex flex-wrap items-center justify-between gap-4">
    <p class="text-gray-300 text-sm">
      We use cookies to enhance your experience. By continuing to visit this site, you agree to our use of cookies.
      <a href="/privacy" class="text-crystal-primary hover:underline">Learn more</a>
    </p>
    <div class="flex gap-2">
      <button id="cookie-accept" class="bg-crystal-primary px-4 py-2 rounded text-sm font-semibold hover:bg-crystal-primary/80">
        Accept
      </button>
      <button id="cookie-decline" class="border border-white/20 px-4 py-2 rounded text-sm hover:bg-white/5">
        Decline
      </button>
    </div>
  </div>
</div>

<script>
  const COOKIE_CONSENT = 'crystal_cookie_consent';
  
  function getConsent(): string | null {
    return localStorage.getItem(COOKIE_CONSENT);
  }
  
  function setConsent(value: string): void {
    localStorage.setItem(COOKIE_CONSENT, value);
  }
  
  const banner = document.getElementById('cookie-banner');
  const acceptBtn = document.getElementById('cookie-accept');
  const declineBtn = document.getElementById('cookie-decline');
  
  // Show banner if no consent recorded
  if (!getConsent() && banner) {
    banner.classList.remove('hidden');
  }
  
  acceptBtn?.addEventListener('click', () => {
    setConsent('accepted');
    banner?.classList.add('hidden');
    // Enable analytics here if needed
  });
  
  declineBtn?.addEventListener('click', () => {
    setConsent('declined');
    banner?.classList.add('hidden');
    // Disable non-essential cookies
  });
</script>
```

Output: Cookie consent component with accept/decline, localStorage persistence.
```

---

## Verification Checklist

After completing all stages, verify:

```
[ ] Domain crystalarcade.gg resolves correctly
[ ] Astro dev server runs without errors
[ ] Landing page renders on mobile and desktop
[ ] Age gate appears on first visit
[ ] Age gate remembers verification (cookie + localStorage)
[ ] Legal pages accessible without age gate
[ ] All legal pages have correct content
[ ] Cookie consent banner appears once
[ ] Email form submits correctly
[ ] Lighthouse score > 90 for performance
[ ] All internal links work
[ ] Footer legal links work
[ ] Build succeeds: npm run build
[ ] Built files work when served by Caddy
```
