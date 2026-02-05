---
name: hugo-build
description: Hugo static site. Build/serve. Theme config.
metadata: { "openclaw": { "requires": { "bins": ["hugo"] } } }
---

# Hugo Build

## Commands
```bash
hugo new site mysite        # Init
hugo new posts/my-post.md   # New content
hugo server -D              # Dev (drafts)
hugo --minify               # Prod build → public/
```

## Config (hugo.toml)
```toml
baseURL = "https://example.com/"
title = "My Site"
theme = "papermod"

[params]
  author = "Name"
  description = "Site desc"
```

## Theme Install
```bash
git submodule add https://github.com/user/theme.git themes/theme
# Or Hugo modules:
hugo mod get github.com/user/theme
```

## Content Front Matter
```yaml
---
title: "Post Title"
date: 2024-01-15
draft: false
tags: ["go", "web"]
---
```

## Gotchas
- `hugo server` ≠ `hugo` (server doesn't write files)
- Drafts hidden in prod unless `-D`
- `public/` is gitignored; CI rebuilds
