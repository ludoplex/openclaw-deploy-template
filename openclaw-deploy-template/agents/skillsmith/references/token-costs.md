# Token Cost Reference

## Skill Token Formula

```
total_chars = 195 + Σ(97 + len(name) + len(description) + len(location))
```

### Examples

| Skill | Name | Description | Location | Cost |
|-------|------|-------------|----------|------|
| Minimal | `git` (3) | `Git commands` (12) | `skills/git` (10) | 122 chars |
| Typical | `nano-pdf` (8) | `Extract text from PDFs using pdfplumber` (40) | `skills/nano-pdf` (15) | 160 chars |
| Bloated | `comprehensive-api-helper` (24) | `Comprehensive helper for working with REST APIs including authentication, pagination, error handling, and response parsing` (118) | `~/.openclaw/skills/comprehensive-api-helper` (44) | 283 chars |

### Token Conversion
- ~4 characters ≈ 1 token (rough estimate)
- Minimal skill: ~30 tokens
- Typical skill: ~40 tokens  
- Bloated skill: ~70 tokens

### Per-Turn Cost
If agent runs 100 turns/day with 10 skills at 50 tokens each:
- Daily: 100 × 500 = 50,000 tokens just for skill metadata
- Monthly: 1.5M tokens = ~$4.50 at Claude rates

**Conclusion:** Every token in skill metadata multiplies across all turns.

## Hook Token Cost

Hooks cost nothing in prompts — they're event handlers, not context.
But they cost:
- Execution time (blocks command briefly)
- Log storage (if logging)
- Complexity (debugging surface)

Keep hooks fast and focused.
