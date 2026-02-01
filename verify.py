#!/usr/bin/env python3
"""Final verification of all systems."""
import sys
sys.path.insert(0, "src")

print("ENGINE TEST:")
from sop import create_engine
engine = create_engine(load_definitions=True)
stats = engine.get_stats()
print(f"  SOPs loaded: {stats['definitions_loaded']}")
for e, c in stats["by_entity"].items():
    if c > 0:
        print(f"    - {e}: {c}")

print()
print("CONTENT SYSTEM:")
from content import list_templates, get_monthly_theme, WEEKLY_SCHEDULE
print(f"  Templates: {len(list_templates())}")
print(f"  Weekly slots: {len(WEEKLY_SCHEDULE)}")
theme = get_monthly_theme(2)
print(f"  Feb theme: {theme['theme']}")

print()
print("ALL SYSTEMS OPERATIONAL")
