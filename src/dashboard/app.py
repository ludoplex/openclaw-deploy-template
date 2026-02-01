"""
SOP Automation Dashboard - FastAPI + HTMX
Multi-entity SOP management for MHI, DSAIC, and Computer Store.
"""

from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import yaml
import sys
from typing import Optional
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import content generator (uses local LLM)
try:
    from src.content.generator import generate_post, generate_hashtags
    LOCAL_LLM_AVAILABLE = True
except Exception as e:
    print(f"Local LLM not available: {e}")
    LOCAL_LLM_AVAILABLE = False

# Import SOP engine
try:
    from src.sop.engine import EnhancedSOPEngine
    _sop_engine = None
    
    def get_sop_engine():
        global _sop_engine
        if _sop_engine is None:
            _sop_engine = EnhancedSOPEngine()
            _sop_engine.load_definitions()
        return _sop_engine
    
    SOP_ENGINE_AVAILABLE = True
except Exception as e:
    print(f"SOP engine not available: {e}")
    SOP_ENGINE_AVAILABLE = False
    
    def get_sop_engine():
        return None

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
async def trigger_sop(
    request: Request,
    entity_id: str,
    sop_id: str,
    dry_run: bool = True  # Default to dry-run for safety
):
    """Trigger SOP execution."""
    if not SOP_ENGINE_AVAILABLE:
        return templates.TemplateResponse("partials/trigger_result.html", {
            "request": request,
            "sop_id": sop_id,
            "status": "error",
            "message": "SOP engine not available"
        })
    
    engine = get_sop_engine()
    
    # Get form data for variables if provided
    form_data = await request.form()
    event_data = {
        "event_type": "manual",
        "trigger_source": "dashboard",
        "entity": entity_id,
        "variables": dict(form_data) if form_data else {}
    }
    
    try:
        result = engine.execute_sop(sop_id, event=event_data, dry_run=dry_run)
        
        return templates.TemplateResponse("partials/trigger_result.html", {
            "request": request,
            "sop_id": sop_id,
            "status": "success" if result.get("success") else "failed",
            "message": f"SOP {sop_id} executed" + (" (dry-run)" if dry_run else ""),
            "result": result,
            "dry_run": dry_run
        })
    except Exception as e:
        return templates.TemplateResponse("partials/trigger_result.html", {
            "request": request,
            "sop_id": sop_id,
            "status": "error",
            "message": f"Execution error: {str(e)}"
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
# CONTENT CALENDAR
# =============================================================================

@app.get("/calendar", response_class=HTMLResponse)
async def content_calendar(request: Request):
    """Content calendar view."""
    from datetime import datetime, timedelta
    import calendar as cal
    
    today = datetime.now()
    
    # Build calendar weeks for current month
    month_cal = cal.monthcalendar(today.year, today.month)
    calendar_weeks = []
    
    for week in month_cal:
        week_data = []
        for day in week:
            day_data = {
                "day": day if day > 0 else "",
                "is_today": day == today.day,
                "is_current_month": day > 0,
                "posts": []  # Would be populated from database
            }
            week_data.append(day_data)
        calendar_weeks.append(week_data)
    
    # Sample upcoming posts (would come from database)
    upcoming_posts = []
    
    stats = {
        "total_scheduled": 0,
        "posts_this_week": 0,
        "drafts": 0,
        "posted_this_month": 0
    }
    
    return templates.TemplateResponse("content_calendar.html", {
        "request": request,
        "calendar_weeks": calendar_weeks,
        "upcoming_posts": upcoming_posts,
        "stats": stats,
        "current_month": today.strftime("%B %Y")
    })


@app.post("/api/calendar/generate", response_class=HTMLResponse)
async def generate_calendar_content(request: Request):
    """Generate content calendar using AI."""
    if not LOCAL_LLM_AVAILABLE:
        return HTMLResponse("<div class='text-red-400 p-4'>Local LLM not available</div>")
    
    try:
        from src.content.generator import generate_content_calendar
        
        # Generate for all entities
        all_content = []
        for entity in ["mighty_house_inc", "dsaic", "computer_store"]:
            content = generate_content_calendar(entity, days=7, posts_per_day=1)
            all_content.extend(content)
        
        # Return HTML with generated content
        html = "<div class='p-4 bg-green-900 rounded-lg'>"
        html += "<h3 class='text-green-300 font-bold mb-3'>✨ Generated Content Ideas</h3>"
        html += "<div class='space-y-2'>"
        for item in all_content[:10]:  # Limit to 10
            html += f"<div class='text-sm text-gray-300'>"
            html += f"<span class='text-gray-500'>{item['date']}</span> - "
            html += f"<span class='font-medium'>{item['topic']}</span> "
            html += f"<span class='text-xs text-gray-500'>({item['platform']})</span>"
            html += "</div>"
        html += "</div></div>"
        
        return HTMLResponse(html)
    except Exception as e:
        return HTMLResponse(f"<div class='text-red-400 p-4'>Error: {str(e)}</div>")


# =============================================================================
# CONTENT GENERATION (Local LLM)
# =============================================================================

@app.get("/content", response_class=HTMLResponse)
async def content_generator_page(request: Request):
    """Content generation page."""
    return templates.TemplateResponse("content_generator.html", {
        "request": request,
        "llm_available": LOCAL_LLM_AVAILABLE,
        "entities": ["mighty_house_inc", "dsaic", "computer_store"],
        "platforms": ["twitter", "linkedin", "discord", "facebook", "instagram"]
    })


@app.post("/api/content/generate", response_class=HTMLResponse)
async def generate_content(
    request: Request,
    entity: str = Form(...),
    topic: str = Form(...),
    platform: str = Form(...),
    context: str = Form("")
):
    """Generate content using local LLM."""
    if not LOCAL_LLM_AVAILABLE:
        return templates.TemplateResponse("partials/content_result.html", {
            "request": request,
            "error": "Local LLM not available. Check llamafile setup.",
            "content": None
        })
    
    try:
        result = generate_post(entity, topic, platform, context if context else None)
        return templates.TemplateResponse("partials/content_result.html", {
            "request": request,
            "content": result["content"],
            "entity": entity,
            "platform": platform,
            "char_count": result["char_count"],
            "error": None
        })
    except Exception as e:
        return templates.TemplateResponse("partials/content_result.html", {
            "request": request,
            "error": str(e),
            "content": None
        })


@app.post("/api/content/hashtags")
async def api_generate_hashtags(entity: str, topic: str, count: int = 5):
    """Generate hashtags using local LLM."""
    if not LOCAL_LLM_AVAILABLE:
        raise HTTPException(status_code=503, detail="Local LLM not available")
    
    hashtags = generate_hashtags(entity, topic, count)
    return {"hashtags": hashtags}


# =============================================================================
# SOP EDITING
# =============================================================================

@app.get("/sop/{entity_id}/{sop_id}/edit", response_class=HTMLResponse)
async def sop_edit_page(request: Request, entity_id: str, sop_id: str):
    """SOP edit form."""
    sops = load_sops()
    
    if entity_id not in sops:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    sop = next((s for s in sops[entity_id] if s.get('sop_id') == sop_id), None)
    if not sop:
        raise HTTPException(status_code=404, detail="SOP not found")
    
    # Load raw YAML for editing
    sop_path = Path(sop['_path'])
    with open(sop_path, 'r', encoding='utf-8') as f:
        raw_yaml = f.read()
    
    return templates.TemplateResponse("sop_edit.html", {
        "request": request,
        "entity_id": entity_id,
        "sop": sop,
        "raw_yaml": raw_yaml
    })


@app.post("/sop/{entity_id}/{sop_id}/edit", response_class=HTMLResponse)
async def sop_edit_save(
    request: Request,
    entity_id: str,
    sop_id: str,
    yaml_content: str = Form(...)
):
    """Save SOP edits."""
    sops = load_sops()
    
    if entity_id not in sops:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    sop = next((s for s in sops[entity_id] if s.get('sop_id') == sop_id), None)
    if not sop:
        raise HTTPException(status_code=404, detail="SOP not found")
    
    # Validate YAML
    try:
        parsed = yaml.safe_load(yaml_content)
        if not parsed:
            raise ValueError("Empty YAML")
    except yaml.YAMLError as e:
        return templates.TemplateResponse("sop_edit.html", {
            "request": request,
            "entity_id": entity_id,
            "sop": sop,
            "raw_yaml": yaml_content,
            "error": f"Invalid YAML: {str(e)}"
        })
    
    # Save to file
    sop_path = Path(sop['_path'])
    with open(sop_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    # Redirect to detail page
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        url=f"/sop/{entity_id}/{sop_id}?saved=1",
        status_code=303
    )


@app.get("/sop/new/{entity_id}", response_class=HTMLResponse)
async def sop_new_page(request: Request, entity_id: str):
    """Create new SOP form."""
    entity_names = {
        "mighty_house_inc": "Mighty House Inc.",
        "dsaic": "DSAIC",
        "computer_store": "Computer Store",
        "cross_entity": "Cross-Entity Pipelines"
    }
    
    if entity_id not in entity_names:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Default template for new SOP
    default_yaml = f'''sop_id: new_sop
name: "New SOP"
description: "Description of the SOP"
entity: {entity_id}
version: "1.0"
status: draft

triggers:
  - type: manual
    description: "Manual trigger"

workflow:
  - step_id: step_1
    name: "First Step"
    type: task
    description: "What this step does"
    config:
      task_type: notification
      message: "SOP started"
'''
    
    return templates.TemplateResponse("sop_edit.html", {
        "request": request,
        "entity_id": entity_id,
        "entity_name": entity_names[entity_id],
        "sop": None,
        "raw_yaml": default_yaml,
        "is_new": True
    })


@app.post("/sop/new/{entity_id}", response_class=HTMLResponse)
async def sop_new_save(
    request: Request,
    entity_id: str,
    yaml_content: str = Form(...)
):
    """Save new SOP."""
    entity_dirs = {
        "mighty_house_inc": "mighty-house-inc",
        "dsaic": "dsaic",
        "computer_store": "computer-store",
        "cross_entity": "cross-entity"
    }
    
    if entity_id not in entity_dirs:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    # Validate YAML
    try:
        parsed = yaml.safe_load(yaml_content)
        if not parsed:
            raise ValueError("Empty YAML")
        sop_id = parsed.get('sop_id', 'new_sop')
    except yaml.YAMLError as e:
        return templates.TemplateResponse("sop_edit.html", {
            "request": request,
            "entity_id": entity_id,
            "sop": None,
            "raw_yaml": yaml_content,
            "is_new": True,
            "error": f"Invalid YAML: {str(e)}"
        })
    
    # Save to file
    entity_path = SOPS_DIR / entity_dirs[entity_id]
    entity_path.mkdir(parents=True, exist_ok=True)
    sop_path = entity_path / f"{sop_id}.yaml"
    
    with open(sop_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    # Redirect to detail page
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        url=f"/sop/{entity_id}/{sop_id}?created=1",
        status_code=303
    )


@app.delete("/api/sop/{entity_id}/{sop_id}")
async def sop_delete(entity_id: str, sop_id: str):
    """Delete an SOP."""
    sops = load_sops()
    
    if entity_id not in sops:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    sop = next((s for s in sops[entity_id] if s.get('sop_id') == sop_id), None)
    if not sop:
        raise HTTPException(status_code=404, detail="SOP not found")
    
    # Move to trash instead of deleting
    sop_path = Path(sop['_path'])
    trash_dir = WORKSPACE / ".trash"
    trash_dir.mkdir(exist_ok=True)
    
    import shutil
    shutil.move(str(sop_path), str(trash_dir / sop_path.name))
    
    return {"status": "deleted", "sop_id": sop_id}


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


@app.get("/api/status")
async def api_status():
    """API: System status."""
    return {
        "status": "running",
        "local_llm": LOCAL_LLM_AVAILABLE,
        "sops": get_sop_stats()
    }


# =============================================================================
# STARTUP
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
