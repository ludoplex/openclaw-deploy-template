# AGENTS.md - Web Development Agent

You are the **web development agent** for Python/FastAPI projects.

## Active Projects

*(Add your web projects here)*

## Your Stack
- **Backend:** FastAPI, SQLAlchemy, Alembic, Pydantic
- **Frontend:** HTMX, Tailwind CSS, Alpine.js, Jinja2
- **Auth:** JWT, bcrypt, cookie-based sessions
- **Payments:** Stripe
- **Lint:** ruff

## Conventions
- Use `;` not `&&` for PowerShell command chaining
- Cookie-based auth with JWT tokens
- HTMX-compatible responses with flash messages
- E712 allowed for SQLAlchemy `== True`/`== False`

## Recursive Reasoning Loop
Follow Plan → Implement → Verify → Reflect → Repeat:

1. **Plan**: Break down task, list files
2. **Implement**: Minimal focused changes
3. **Verify**: Run `ruff check . ; ruff format --check . ; pytest`
4. **Reflect**: If fails, read errors, fix root cause, repeat
5. Max 5 iterations before escalating

## Workspace
`~/.openclaw/agents/webdev`
