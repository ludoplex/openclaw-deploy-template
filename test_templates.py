#!/usr/bin/env python3
"""Test content templates system."""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

try:
    from src.content.templates import (
        list_templates, 
        render_template, 
        get_template,
        get_templates_by_entity,
        ALL_TEMPLATES
    )
    
    print(f"[OK] Templates loaded: {len(ALL_TEMPLATES)}")
    
    entities = list(set(t.entity for t in ALL_TEMPLATES))
    print(f"[OK] Entities: {entities}")
    
    # Test rendering a template
    test_data = {
        "event_name": "Smash Bros Tournament",
        "date": "February 15, 2026",
        "time": "2:00 PM",
        "prize": "$100",
        "game": "Super Smash Bros Ultimate",
        "registration": "In-store or call 307-322-4755"
    }
    
    result = render_template("cs_tournament_announce", test_data)
    print(f"[OK] Template render test:")
    print("-" * 40)
    # Strip emojis for console output
    import re
    clean = re.sub(r'[^\x00-\x7F]+', '', result[:200])
    print(clean + "...")
    print("-" * 40)
    
    print("\n=== All Templates ===")
    for t in ALL_TEMPLATES:
        print(f"  - {t.id} ({t.entity}) [{t.category.value}]")
    
    print("\n=== By Entity ===")
    for entity in entities:
        count = len(get_templates_by_entity(entity))
        print(f"  {entity}: {count} templates")
    
    print("\n[SUCCESS] Content templates system working!")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
