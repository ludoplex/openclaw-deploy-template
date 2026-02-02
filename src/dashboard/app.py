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

# Import Scheduler
try:
    from src.sop.scheduler import SOPScheduler, Schedule, ScheduleType
    _scheduler = None
    
    def get_scheduler():
        global _scheduler
        if _scheduler is None:
            _scheduler = SOPScheduler()
        return _scheduler
    
    SCHEDULER_AVAILABLE = True
except Exception as e:
    print(f"Scheduler not available: {e}")
    SCHEDULER_AVAILABLE = False
    
    def get_scheduler():
        return None

# Import Zoho CRM integration
try:
    from src.integrations.zoho.crm_handler import ZohoCRMHandler
    from src.integrations.zoho.webhooks import ZohoWebhookHandler, setup_webhook_mappings
    ZOHO_AVAILABLE = True
    _zoho_handler = ZohoWebhookHandler()
    setup_webhook_mappings(_zoho_handler)
except Exception as e:
    print(f"Zoho integration not available: {e}")
    ZOHO_AVAILABLE = False
    _zoho_handler = None

# Import Media Generator Pipeline
try:
    from src.content.prompt_templates import get_prompt_library, MediaType
    from src.content.media_generator import (
        get_media_pipeline, 
        MediaRequest, 
        RequestStatus,
        OutputFormat
    )
    MEDIA_PIPELINE_AVAILABLE = True
except Exception as e:
    print(f"Media pipeline not available: {e}")
    MEDIA_PIPELINE_AVAILABLE = False

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


# =============================================================================
# EXECUTION HISTORY
# =============================================================================

@app.get("/history", response_class=HTMLResponse)
async def execution_history(request: Request):
    """Execution history view."""
    # Get history from engine if available
    executions = []
    if SOP_ENGINE_AVAILABLE:
        engine = get_sop_engine()
        history = getattr(engine, '_history', [])
        for i, exec_data in enumerate(reversed(history[-50:])):  # Last 50
            steps_passed = sum(1 for s in exec_data.get('step_results', []) if s.get('success'))
            steps_total = len(exec_data.get('step_results', []))
            
            # Calculate duration
            try:
                from datetime import datetime
                started = datetime.fromisoformat(exec_data.get('started_at', ''))
                completed = datetime.fromisoformat(exec_data.get('completed_at', ''))
                duration_ms = int((completed - started).total_seconds() * 1000)
            except:
                duration_ms = 0
            
            executions.append({
                'id': i,
                'sop_id': exec_data.get('sop_id'),
                'sop_name': exec_data.get('sop_name'),
                'entity': exec_data.get('entity'),
                'success': exec_data.get('success'),
                'dry_run': exec_data.get('dry_run'),
                'started_at': exec_data.get('started_at', '')[:19].replace('T', ' '),
                'steps_passed': steps_passed,
                'steps_total': steps_total,
                'duration_ms': duration_ms,
            })
    
    return templates.TemplateResponse("execution_history.html", {
        "request": request,
        "executions": executions,
        "total_pages": 1,
        "current_page": 1
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
# SCHEDULER
# =============================================================================

@app.get("/scheduler", response_class=HTMLResponse)
async def scheduler_page(request: Request):
    """Scheduler dashboard."""
    scheduler = get_scheduler()
    schedules = scheduler.list_schedules() if scheduler else []
    
    # Convert to dicts for template
    schedules_data = []
    for s in schedules:
        schedules_data.append({
            'id': s.id,
            'sop_id': s.sop_id,
            'entity': s.entity,
            'schedule_type': s.schedule_type.value,
            'expression': s.expression,
            'enabled': s.enabled,
            'next_run': s.next_run,
            'run_count': s.run_count,
            'max_runs': s.max_runs
        })
    
    return templates.TemplateResponse("scheduler.html", {
        "request": request,
        "schedules": schedules_data,
        "all_sops": load_sops()
    })


@app.post("/api/scheduler")
async def api_create_schedule(
    entity: str = Form(...),
    sop_id: str = Form(...),
    schedule_type: str = Form(...),
    expression: str = Form(...),
    max_runs: Optional[int] = Form(None)
):
    """Create a new schedule."""
    scheduler = get_scheduler()
    if not scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not available")
    
    import uuid
    schedule = Schedule(
        id=str(uuid.uuid4())[:8],
        sop_id=sop_id,
        entity=entity,
        schedule_type=ScheduleType(schedule_type),
        expression=expression,
        max_runs=max_runs
    )
    
    scheduler.add_schedule(schedule)
    
    # Return the new row HTML for HTMX
    return HTMLResponse(f'''
        <tr class="schedule-row" data-entity="{entity}" data-enabled="enabled">
            <td class="px-6 py-4 whitespace-nowrap">
                <a href="/sop/{entity}/{sop_id}" class="text-blue-600 hover:underline">{sop_id}</a>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full bg-gray-100">{entity.replace('_', ' ').title()}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{schedule_type}</td>
            <td class="px-6 py-4 whitespace-nowrap font-mono text-sm">{expression}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">{schedule.next_run or '—'}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">0{f'/{max_runs}' if max_runs else ''}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">Enabled</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="text-green-600">✓ Created</span>
            </td>
        </tr>
    ''')


@app.post("/api/scheduler/{schedule_id}/toggle")
async def api_toggle_schedule(schedule_id: str):
    """Toggle schedule enabled/disabled."""
    scheduler = get_scheduler()
    if not scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not available")
    
    schedule = scheduler.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    scheduler.update_schedule(schedule_id, {'enabled': not schedule.enabled})
    schedule = scheduler.get_schedule(schedule_id)  # Refresh
    
    status_class = "bg-green-100 text-green-800" if schedule.enabled else "bg-gray-100 text-gray-500"
    status_text = "Enabled" if schedule.enabled else "Disabled"
    
    return HTMLResponse(f'''
        <tr class="schedule-row" data-entity="{schedule.entity}" data-enabled="{'enabled' if schedule.enabled else 'disabled'}">
            <td class="px-6 py-4 whitespace-nowrap">
                <a href="/sop/{schedule.entity}/{schedule.sop_id}" class="text-blue-600 hover:underline">{schedule.sop_id}</a>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full bg-gray-100">{schedule.entity.replace('_', ' ').title()}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{schedule.schedule_type.value}</td>
            <td class="px-6 py-4 whitespace-nowrap font-mono text-sm">{schedule.expression}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">{schedule.next_run[:16].replace('T', ' ') if schedule.next_run else '—'}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">{schedule.run_count}{f'/{schedule.max_runs}' if schedule.max_runs else ''}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <button hx-post="/api/scheduler/{schedule_id}/toggle" hx-swap="outerHTML" hx-target="closest tr"
                        class="px-2 py-1 text-xs rounded-full {status_class}">{status_text}</button>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <div class="flex gap-2">
                    <button hx-post="/api/scheduler/{schedule_id}/run" hx-target="#runResult" class="text-green-600">▶️</button>
                    <button hx-delete="/api/scheduler/{schedule_id}" hx-confirm="Delete?" hx-target="closest tr" hx-swap="outerHTML" class="text-red-600">🗑️</button>
                </div>
            </td>
        </tr>
    ''')


@app.delete("/api/scheduler/{schedule_id}")
async def api_delete_schedule(schedule_id: str):
    """Delete a schedule."""
    scheduler = get_scheduler()
    if not scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not available")
    
    if scheduler.remove_schedule(schedule_id):
        return HTMLResponse("")  # Empty = row removed
    raise HTTPException(status_code=404, detail="Schedule not found")


@app.post("/api/scheduler/{schedule_id}/run")
async def api_run_schedule(schedule_id: str):
    """Run a schedule immediately."""
    scheduler = get_scheduler()
    engine = get_sop_engine()
    
    if not scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not available")
    
    schedule = scheduler.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Execute the SOP
    if engine:
        try:
            result = engine.execute_sop(schedule.sop_id, schedule.entity, schedule.variables)
            scheduler.mark_run(schedule_id)
            return HTMLResponse(f'''
                <div class="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <p class="text-green-800 font-medium">✓ SOP Executed: {schedule.sop_id}</p>
                    <p class="text-sm text-green-600">Steps completed: {result.get('steps_completed', 'N/A')}</p>
                </div>
            ''')
        except Exception as e:
            return HTMLResponse(f'''
                <div class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                    <p class="text-red-800 font-medium">✗ Execution Failed</p>
                    <p class="text-sm text-red-600">{str(e)}</p>
                </div>
            ''')
    else:
        return HTMLResponse(f'''
            <div class="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p class="text-yellow-800 font-medium">⚠ Dry Run Mode</p>
                <p class="text-sm text-yellow-600">SOP engine not available. Would execute: {schedule.sop_id}</p>
            </div>
        ''')


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
        "zoho_crm": ZOHO_AVAILABLE,
        "sops": get_sop_stats()
    }


# =============================================================================
# ZOHO WEBHOOKS
# =============================================================================

@app.post("/webhooks/zoho")
async def receive_zoho_webhook(request: Request):
    """Receive Zoho CRM webhook."""
    if not ZOHO_AVAILABLE or not _zoho_handler:
        raise HTTPException(status_code=503, detail="Zoho integration not available")
    
    try:
        data = await request.json()
        signature = request.headers.get("X-Zoho-Signature")
        
        result = _zoho_handler.process_webhook(data, signature)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Processing failed"))
        
        # Trigger SOPs if any matched
        engine = get_sop_engine()
        triggered = []
        if engine and result.get("triggered_sops"):
            for trigger in result["triggered_sops"]:
                try:
                    exec_result = engine.execute_sop(
                        trigger["sop_id"],
                        event=trigger["event"]
                    )
                    triggered.append({
                        "sop_id": trigger["sop_id"],
                        "success": exec_result.get("success", False)
                    })
                except Exception as e:
                    triggered.append({
                        "sop_id": trigger["sop_id"],
                        "success": False,
                        "error": str(e)
                    })
        
        return {
            "status": "ok",
            "event_type": result.get("event_type"),
            "sops_triggered": triggered
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/zoho/mappings")
async def get_zoho_mappings():
    """Get Zoho webhook to SOP mappings."""
    if not ZOHO_AVAILABLE or not _zoho_handler:
        return {"available": False, "mappings": {}}
    return {
        "available": True,
        **_zoho_handler.get_mappings_summary()
    }


@app.get("/api/zoho/status")
async def get_zoho_status():
    """Check Zoho CRM connection status."""
    if not ZOHO_AVAILABLE:
        return {"available": False, "connected": False, "error": "Zoho integration not loaded"}
    
    try:
        from src.integrations.zoho.crm_handler import ZohoCRMHandler
        with ZohoCRMHandler() as crm:
            if crm.connected:
                return {
                    "available": True,
                    "connected": True,
                    "message": "Connected to Zoho CRM"
                }
            else:
                return {
                    "available": True,
                    "connected": False,
                    "error": crm._last_error
                }
    except Exception as e:
        return {"available": True, "connected": False, "error": str(e)}


# =============================================================================
# MEDIA CONTENT PIPELINE
# =============================================================================

@app.get("/media", response_class=HTMLResponse)
async def media_pipeline_page(request: Request):
    """Media generation pipeline dashboard."""
    if not MEDIA_PIPELINE_AVAILABLE:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Media pipeline not available"
        })
    
    library = get_prompt_library()
    pipeline = get_media_pipeline()
    
    # Get library stats
    lib_stats = library.to_dict()
    
    # Get pending approvals and recent requests
    pending = pipeline.get_pending_approvals()
    recent = sorted(
        pipeline.requests.values(), 
        key=lambda r: r.created_at, 
        reverse=True
    )[:10]
    
    return templates.TemplateResponse("media_pipeline.html", {
        "request": request,
        "library_stats": lib_stats,
        "pending_approvals": [r.to_dict() for r in pending],
        "recent_requests": [r.to_dict() for r in recent],
        "pipeline_stats": pipeline.get_stats(),
        "categories": library.get_categories(),
        "entities": ["mighty_house_inc", "dsaic", "computer_store"],
    })


@app.get("/api/media/prompts")
async def api_list_prompts(
    entity: Optional[str] = None,
    category: Optional[str] = None,
    media_type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50
):
    """API: List marketing prompts from library."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    library = get_prompt_library()
    
    if search:
        prompts = library.search_prompts(search)[:limit]
    else:
        mt = MediaType(media_type) if media_type else None
        prompts = library.get_all_prompts(entity, category, mt)[:limit]
    
    return {
        "prompts": [
            {
                "id": p.id,
                "service_id": p.service_id,
                "service_name": p.service_name,
                "price": p.price,
                "media_type": p.media_type.value,
                "variant": p.variant,
                "category": p.category,
                "entity": p.entity,
                "prompt_preview": p.prompt[:200] + "..." if len(p.prompt) > 200 else p.prompt,
            }
            for p in prompts
        ],
        "total": len(prompts),
    }


@app.get("/api/media/prompts/{entity}/{service_id}")
async def api_get_service_prompts(entity: str, service_id: int):
    """API: Get all prompts for a specific service."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    library = get_prompt_library()
    service = library.get_service(entity, service_id)
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {
        "service_id": service.service_id,
        "name": service.name,
        "price": service.price,
        "category": service.category,
        "entity": service.entity,
        "canva_prompts": service.canva_prompts,
        "sora2_prompts": service.sora2_prompts,
    }


@app.post("/api/media/request/image", response_class=HTMLResponse)
async def create_image_request(
    request: Request,
    entity: str = Form(...),
    service_id: int = Form(...),
    variant: int = Form(1),
    output_format: str = Form("1080x1080"),
    custom_prompt: Optional[str] = Form(None)
):
    """Create an image generation request."""
    if not MEDIA_PIPELINE_AVAILABLE:
        return HTMLResponse("<div class='text-red-400'>Media pipeline not available</div>")
    
    library = get_prompt_library()
    pipeline = get_media_pipeline()
    
    service = library.get_service(entity, service_id)
    if not service:
        return HTMLResponse(f"<div class='text-red-400'>Service {service_id} not found</div>")
    
    # Get the specific prompt
    canva_prompts = service.get_prompts(MediaType.CANVA)
    if variant > len(canva_prompts):
        return HTMLResponse(f"<div class='text-red-400'>Variant {variant} not found</div>")
    
    prompt = canva_prompts[variant - 1]
    
    # Create request
    media_request = pipeline.create_image_request(
        prompt=prompt,
        output_format=OutputFormat(output_format),
    )
    
    # Apply custom prompt if provided
    if custom_prompt:
        pipeline.update_prompt(media_request.id, custom_prompt)
    
    return HTMLResponse(f'''
        <div class="p-4 bg-green-900 rounded-lg">
            <p class="text-green-300 font-bold">✓ Image Request Created</p>
            <p class="text-sm text-gray-300 mt-2">Request ID: {media_request.id}</p>
            <p class="text-sm text-gray-400">Service: {service.name}</p>
            <p class="text-sm text-gray-400">Format: {output_format}</p>
            <div class="mt-3 flex gap-2">
                <button hx-post="/api/media/request/{media_request.id}/submit" 
                        hx-target="#requestResult"
                        class="px-3 py-1 bg-blue-600 text-white rounded text-sm">
                    Submit for Approval
                </button>
                <a href="/api/media/request/{media_request.id}/export/canva" 
                   class="px-3 py-1 bg-gray-600 text-white rounded text-sm">
                    Export Prompt
                </a>
            </div>
        </div>
    ''')


@app.post("/api/media/request/video", response_class=HTMLResponse)
async def create_video_request(
    request: Request,
    entity: str = Form(...),
    service_id: int = Form(...),
    variant: int = Form(1),
    output_format: str = Form("9:16"),
    duration: int = Form(15),
    custom_prompt: Optional[str] = Form(None)
):
    """Create a video generation request."""
    if not MEDIA_PIPELINE_AVAILABLE:
        return HTMLResponse("<div class='text-red-400'>Media pipeline not available</div>")
    
    library = get_prompt_library()
    pipeline = get_media_pipeline()
    
    service = library.get_service(entity, service_id)
    if not service:
        return HTMLResponse(f"<div class='text-red-400'>Service {service_id} not found</div>")
    
    # Get the specific prompt
    sora_prompts = service.get_prompts(MediaType.SORA2)
    if variant > len(sora_prompts):
        return HTMLResponse(f"<div class='text-red-400'>Variant {variant} not found</div>")
    
    prompt = sora_prompts[variant - 1]
    
    # Create request
    media_request = pipeline.create_video_request(
        prompt=prompt,
        output_format=OutputFormat(output_format),
        duration_seconds=duration,
    )
    
    # Apply custom prompt if provided
    if custom_prompt:
        pipeline.update_prompt(media_request.id, custom_prompt)
    
    return HTMLResponse(f'''
        <div class="p-4 bg-purple-900 rounded-lg">
            <p class="text-purple-300 font-bold">🎬 Video Request Created</p>
            <p class="text-sm text-gray-300 mt-2">Request ID: {media_request.id}</p>
            <p class="text-sm text-gray-400">Service: {service.name}</p>
            <p class="text-sm text-gray-400">Duration: {duration}s | Format: {output_format}</p>
            <div class="mt-3 flex gap-2">
                <button hx-post="/api/media/request/{media_request.id}/submit" 
                        hx-target="#requestResult"
                        class="px-3 py-1 bg-blue-600 text-white rounded text-sm">
                    Submit for Approval
                </button>
                <a href="/api/media/request/{media_request.id}/export/sora" 
                   class="px-3 py-1 bg-gray-600 text-white rounded text-sm">
                    Export Prompt
                </a>
            </div>
        </div>
    ''')


@app.post("/api/media/request/{request_id}/submit")
async def submit_media_request(request_id: str):
    """Submit a media request for approval."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    pipeline = get_media_pipeline()
    
    try:
        req = pipeline.submit_for_approval(request_id)
        return HTMLResponse(f'''
            <div class="p-3 bg-yellow-900 rounded text-yellow-300 text-sm">
                ⏳ Request {request_id} submitted for approval
            </div>
        ''')
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/media/request/{request_id}/approve")
async def approve_media_request(
    request_id: str,
    approved_by: str = Form("dashboard")
):
    """Approve a media request."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    pipeline = get_media_pipeline()
    
    try:
        req = pipeline.approve_request(request_id, approved_by)
        return {"status": "approved", "request_id": request_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/media/request/{request_id}/reject")
async def reject_media_request(
    request_id: str,
    reason: str = Form("")
):
    """Reject a media request."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    pipeline = get_media_pipeline()
    
    try:
        req = pipeline.reject_request(request_id, reason)
        return {"status": "rejected", "request_id": request_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/media/request/{request_id}/export/canva")
async def export_canva_request(request_id: str):
    """Export request as Canva-ready format."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    pipeline = get_media_pipeline()
    
    try:
        return pipeline.export_for_canva(request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/media/request/{request_id}/export/sora")
async def export_sora_request(request_id: str):
    """Export request as Sora 2-ready format."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    pipeline = get_media_pipeline()
    
    try:
        return pipeline.export_for_sora(request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/media/requests")
async def list_media_requests(
    status: Optional[str] = None,
    entity: Optional[str] = None,
    limit: int = 50
):
    """List media requests with filters."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    pipeline = get_media_pipeline()
    
    if status:
        requests = pipeline.get_requests_by_status(RequestStatus(status))
    elif entity:
        requests = pipeline.get_requests_by_entity(entity)
    else:
        requests = list(pipeline.requests.values())
    
    # Sort by created_at descending
    requests = sorted(requests, key=lambda r: r.created_at, reverse=True)[:limit]
    
    return {
        "requests": [r.to_dict() for r in requests],
        "total": len(requests),
    }


@app.post("/api/media/brief")
async def generate_content_brief(
    entity: str = Form(...),
    category: Optional[str] = Form(None),
    count: int = Form(5)
):
    """Generate a content brief with AI recommendations."""
    if not MEDIA_PIPELINE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Media pipeline not available")
    
    pipeline = get_media_pipeline()
    brief = pipeline.generate_content_brief(entity, category, count=count)
    
    return {"brief": brief, "entity": entity, "count": len(brief)}


@app.get("/api/media/stats")
async def get_media_stats():
    """Get media pipeline statistics."""
    if not MEDIA_PIPELINE_AVAILABLE:
        return {"available": False}
    
    pipeline = get_media_pipeline()
    return {"available": True, **pipeline.get_stats()}


# =============================================================================
# STARTUP
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
