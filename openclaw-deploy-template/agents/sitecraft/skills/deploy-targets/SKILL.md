---
name: deploy-targets
description: Deploy to Netlify/Vercel/CF Pages. CLI commands.
---

# Deploy Targets

## Netlify
```bash
# Install
npm i -g netlify-cli

# Deploy
netlify deploy --prod --dir=public

# Config (netlify.toml)
[build]
  publish = "public"
  command = "hugo --minify"
```

## Vercel
```bash
# Install
npm i -g vercel

# Deploy
vercel --prod

# Config (vercel.json)
{"buildCommand":"hugo --minify","outputDirectory":"public"}
```

## Cloudflare Pages
```bash
# Install
npm i -g wrangler

# Deploy
wrangler pages deploy public --project-name=mysite

# Or link Git: Dashboard → Pages → Connect
```

## Comparison
| Feature | Netlify | Vercel | CF Pages |
|---------|---------|--------|----------|
| Free builds | 300 min/mo | 6000 min/mo | Unlimited |
| Bandwidth | 100GB | 100GB | Unlimited |
| Functions | ✓ | ✓ | Workers |

## Gotchas
- Set `HUGO_VERSION` env for reproducible builds
- Netlify/Vercel: auto-deploy on git push
- CF Pages: add `NODE_VERSION=18` env
