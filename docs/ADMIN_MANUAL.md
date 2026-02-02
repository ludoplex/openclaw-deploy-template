# Admin Manual

## Quick Start

1. **Start the dashboard:**
   ```bash
   cd sop-automation-dashboard
   python -m uvicorn src.dashboard.app:app --host 0.0.0.0 --port 8080 --reload
   ```

2. **Start llamafile (AI content generation):**
   ```bash
   ./bin/llamafile.exe -m models/qwen2.5-7b-instruct-q3_k_m.gguf --server --port 8081 -ngl 99
   ```

3. **Access the dashboard:** http://localhost:8080

## Dashboard Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Entity overview, stats |
| Entity View | `/entity/{id}` | SOPs for specific entity |
| SOP Detail | `/sop/{entity}/{sop}` | View/run individual SOP |
| Drafts | `/drafts` | Content review workflow |
| Media | `/media` | Image/video prompt library |
| Approvals | `/approvals` | Pending SOP approvals |
| Scheduler | `/scheduler` | Scheduled SOP runs |
| Calendar | `/calendar` | Content calendar view |
| History | `/history` | Execution logs |

## API Endpoints

### SOPs
- `GET /api/sops` - List all SOPs
- `GET /api/sops/{entity}` - List entity SOPs
- `POST /api/sop/{entity}/{sop}/trigger` - Execute SOP
- `DELETE /api/sop/{entity}/{sop}` - Delete SOP

### Content
- `POST /api/content/generate` - Generate content with AI
- `POST /api/content/hashtags` - Generate hashtags
- `POST /api/drafts/generate` - Create AI draft
- `POST /api/drafts/{id}/approve` - Approve draft
- `POST /api/drafts/{id}/publish` - Publish draft

### Media Pipeline
- `GET /api/media/prompts` - List prompt library
- `POST /api/media/request/image` - Create image request
- `POST /api/media/request/video` - Create video request
- `GET /api/media/request/{id}/export/canva` - Export for Canva
- `GET /api/media/request/{id}/export/sora` - Export for Sora 2

### Integrations
- `POST /webhooks/zoho` - Zoho CRM webhook receiver
- `GET /api/zoho/status` - Zoho connection status

## Entity Configuration

Entities are configured in `src/sop/step_types.py`:

```python
ENTITY_CONFIGS = {
    "mighty_house_inc": {
        "name": "Mighty House Inc.",
        "hashtags": ["#MightyHouseInc", "#EDWOSB"],
        "platforms": ["linkedin", "twitter", "facebook"],
        "voice": VoiceProfile.PROFESSIONAL,
    },
    # ...
}
```

## Content Workflow

### Draft → Review → Publish Flow

1. **Generate Draft** (`POST /api/drafts/generate`)
   - AI creates content based on entity, platform, topic

2. **Review** (`/drafts` page)
   - Human reviews AI-generated content
   - Can edit before approving

3. **Approve/Reject** (`POST /api/drafts/{id}/approve`)
   - Approved drafts move to "Ready to Publish"

4. **Publish** (`POST /api/drafts/{id}/publish`)
   - Sends to MixPost (when configured)
   - Or marks as published for manual posting

## Data Storage

All data is stored in JSON files under `data/`:

| File | Contents |
|------|----------|
| `data/content_drafts.json` | Content review workflow |
| `data/media_requests.json` | Media generation requests |
| `data/approvals.json` | SOP approval requests |
| `data/content/content_items.json` | Archived content |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLAMAFILE_URL` | `http://localhost:8081` | Local LLM server |
| `MIXPOST_URL` | - | MixPost API base URL |
| `MIXPOST_TOKEN` | - | MixPost API token |
| `ZOHO_CLIENT_ID` | - | Zoho OAuth client |
| `ZOHO_CLIENT_SECRET` | - | Zoho OAuth secret |

## Backup

Critical files to backup:
- `data/` directory (all JSON state)
- `sops/` directory (SOP definitions)
- `src/content/` templates

## Updating SOPs

1. Edit YAML file directly, or
2. Use dashboard: `/sop/{entity}/{sop}/edit`
3. Changes take effect immediately (no restart needed)

## Monitoring

- Health check: `GET /api/status`
- LLM health: `GET http://localhost:8081/health`
- View logs in terminal running uvicorn
