# Workflows

Lightweight, repeatable patterns captured during sessions. Lighter than skills — just quick reference recipes.

## Structure

```
workflows/
├── README.md           # This file
├── laravel-provider.md # Add social provider to MixPost
├── pr-review-fix.md    # Handle PR review feedback
├── new-feature.md      # Add feature with PR workflow
└── ...
```

## Format

Each workflow is a single markdown file:

```markdown
# Workflow Name

> One-line description

## When to Use
- Trigger condition 1
- Trigger condition 2

## Steps
1. Step one
2. Step two
3. ...

## Templates/Commands
\`\`\`bash
# Useful commands
\`\`\`

## Checklist
- [ ] Item 1
- [ ] Item 2
```

## vs Skills

| Workflows | Skills |
|-----------|--------|
| Project-specific | Global/reusable |
| Quick recipes | Full tooling |
| Captured ad-hoc | Carefully designed |
| Single file | Directory + assets |

## Adding Workflows

When you notice a repeatable pattern:
1. Create `workflows/pattern-name.md`
2. Document the steps
3. Include commands/templates
4. Add to this README's index

---

## Index

- **[laravel-provider](laravel-provider.md)** — Add social provider to MixPost fork
- **[pr-review-fix](pr-review-fix.md)** — Handle PR review feedback cycle
- **[feature-branch](feature-branch.md)** — Feature development with PR workflow
