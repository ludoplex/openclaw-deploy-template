#!/usr/bin/env python3
"""Final status check for tonight's work."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=== FINAL STATUS CHECK ===")
print()

# Test SOP engine
from sop import create_engine
engine = create_engine(load_definitions=True)
stats = engine.get_stats()

print("SOP ENGINE:")
print(f"  Total Definitions: {stats['definitions_loaded']}")
for entity, count in stats["by_entity"].items():
    if count > 0:
        print(f"    - {entity}: {count}")

# List all SOPs
print()
print("ALL SOPs:")
for defn in sorted(engine.list_definitions(), key=lambda x: x.get("entity", "")):
    sop_id = defn.get("sop_id", defn.get("name", "unknown"))
    entity = defn.get("entity", "?")
    print(f"  [{entity[:2].upper()}] {sop_id}")

# Test content templates
print()
from content import list_templates, render_template
templates = list_templates()
print(f"CONTENT TEMPLATES: {len(templates)}")
for t in templates[:5]:
    print(f"  - {t['id']} ({t['entity']})")
if len(templates) > 5:
    print(f"  ... and {len(templates) - 5} more")

# Test template rendering
print()
print("TEMPLATE RENDER TEST:")
content = render_template("cs_deal", {
    "item": "Gaming Mouse",
    "original_price": "79.99",
    "sale_price": "49.99",
    "details": "RGB, 16000 DPI, Wireless"
})
# Print first few lines
for line in content.split("\n")[:5]:
    print(f"  {line}")

print()
print("=== ALL SYSTEMS GO ===")
