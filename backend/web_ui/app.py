"""
Web-based Settings UI (v1.0)
Simple settings interface accessible via browser
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="web_ui/templates")


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings page"""
    # Load current config
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
    else:
        config = {}
    
    return templates.TemplateResponse(
        "settings.html",
        {"request": request, "config": config}
    )


@router.post("/api/settings")
async def update_settings(settings: dict):
    """Update settings"""
    config_file = Path("config.json")
    
    # Load existing config
    if config_file.exists():
        with open(config_file) as f:
            config = json.load(f)
    else:
        config = {}
    
    # Update with new settings
    config.update(settings)
    
    # Save
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return {"success": True, "message": "Settings updated"}

