"""
SOP Automation Dashboard - FastAPI + HTMX
Multi-entity SOP management for MHI, DSAIC, and Computer Store.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import yaml
from typing import Optional
from datetime import datetime

# Setup paths
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
WORKSPACE = Path(__file__).parent.parent.parent
SOPS_DIR = WORKSPACE / "sops"

app = FastAPI(
    title="SOP Automation Dashboard",
    description="Multi-entity SOP management system",
    version="0.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# =============================================================================
# HELPERS
# =============================================================================

def load_sops() -> dict:
    """Load all SOPs from the sops directory."""
    sops = {
        "mighty_house_inc": [],
        "dsaic": [],
        "computer_store": [],
        "cross_entity": []
    }
    
    entity_dirs = {
        "mighty-house-inc": "mighty_house_inc",
        "dsaic": "dsaic", 
        "computer-store": "computer_store",
        "cross-entity": "cross_entity"
    }
    
    for dir_name, entity_key in entity_dirs.items():
        entity_path = SOPS_DIR / dir_name
        if entity_path.exists():
            for sop_file in entity_path.glob("*.yaml"):
                try:
                    with open(sop_file, 'r', encoding='utf-8') as f:
                        sop_data = yaml.safe_load(f)
                        sop_data['_file'] = sop_file.name
                        sop_data['_path'] = str(sop_file)
                        sops[entity_key].append(sop_data)
                except Exception as e:
                    print(f"Error loading {sop_file}: {e}")
    
    return sops


def get_sop_stats() -> dict:
    """Get SOP statistics."""
    sops = load_sops()
    return {
        "total": sum(len(v) for v in sops.values()),
        "by_entity": {k: len(v) for k, v in sops.items()},
        "entities": list(sops.keys())
    }


# =============================================================================
# ROUTES
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard view."""
    stats = get_sop_stats()
    sops = load_sops()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "sops": sops,
        "now": datetime.now()
    })


@app.get("/entity/{entity_id}", response_class=HTMLResponse)
async def entity_view(request: Request, entity_id: str):
    """Entity-specific SOP view."""
    sops = load_sops()
    
    if entity_id not in sops:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    entity_names = {
        "mighty_house_inc": "Mighty House Inc.",
        "dsaic": "DSAIC",
        "computer_store": "Computer Store",
        "cross_entity": "Cross-Entity Pipelines"
    }
    
    return templates.TemplateResponse("entity.html", {
        "request": request,
        "entity_id": entity_id,
        "entity_name": entity_names.get(entity_id, entity_id),
        "sops": sops[entity_id]
    })


@app.get("/sop/{entity_id}/{sop_id}", response_class=HTMLResponse)
async def sop_detail(request: Request, entity_id: str, sop_id: str):
    """SOP detail view."""
    sops = load_sops()
    
    if entity_id not in sops:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    sop = next((s for s in sops[entity_id] if s.get('sop_id') == sop_id), None)
    if not sop:
        raise HTTPException(status_code=404, detail="SOP not found")
    
    return templates.TemplateResponse("sop_detail.html", {
        "request": request,
        "entity_id": entity_id,
        "sop": sop
    })


# =============================================================================
# HTMX PARTIALS
# =============================================================================

@app.get("/partials/sop-list/{entity_id}", response_class=HTMLResponse)
async def sop_list_partial(request: Request, entity_id: str):
    """HTMX partial: SOP list for an entity."""
    sops = load_sops()
    
    return templates.TemplateResponse("partials/sop_list.html", {
        "request": request,
        "entity_id": entity_id,
        "sops": sops.get(entity_id, [])
    })


@app.post("/api/sop/{entity_id}/{sop_id}/trigger", response_class=HTMLResponse)
async def trigger_sop(request: Request, entity_id: str, sop_id: str):
    """Trigger SOP execution (dry-run for now)."""
    return templates.TemplateResponse("partials/trigger_result.html", {
        "request": request,
        "sop_id": sop_id,
        "status": "triggered",
        "message": f"SOP {sop_id} triggered (dry-run mode)"
    })


@app.get("/api/stats", response_class=HTMLResponse)
async def stats_partial(request: Request):
    """HTMX partial: Dashboard stats."""
    stats = get_sop_stats()
    return templates.TemplateResponse("partials/stats.html", {
        "request": request,
        "stats": stats
    })


# =============================================================================
# API ENDPOINTS (JSON)
# =============================================================================

@app.get("/api/sops")
async def api_list_sops():
    """API: List all SOPs."""
    return load_sops()


@app.get("/api/sops/{entity_id}")
async def api_entity_sops(entity_id: str):
    """API: List SOPs for an entity."""
    sops = load_sops()
    if entity_id not in sops:
        raise HTTPException(status_code=404, detail="Entity not found")
    return sops[entity_id]


# =============================================================================
# STARTUP
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
