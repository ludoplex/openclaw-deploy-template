#!/usr/bin/env python3
"""Quick engine test - ASCII only for Windows compatibility."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=== SOP Engine Quick Test ===")
print()

# Test imports
print("1. Testing imports...")
try:
    from sop import StepType, Entity, create_engine, get_entity_config
    print("   OK - All imports successful")
except ImportError as e:
    print(f"   FAIL - {e}")
    sys.exit(1)

# Test step types
print()
print("2. Testing step types...")
test_types = ["validation", "social_post", "content_generate", "cross_entity_trigger"]
for t in test_types:
    try:
        st = StepType(t)
        print(f"   OK - {t}")
    except ValueError:
        print(f"   FAIL - {t}")

# Test entity configs
print()
print("3. Testing entity configs...")
for e in [Entity.MIGHTY_HOUSE_INC, Entity.DSAIC, Entity.COMPUTER_STORE]:
    cfg = get_entity_config(e)
    hashtag_count = len(cfg.get("hashtags", []))
    print(f"   OK - {e.value}: {hashtag_count} hashtags")

# Test engine
print()
print("4. Testing engine creation...")
engine = create_engine(load_definitions=True)
stats = engine.get_stats()
print(f"   Definitions loaded: {stats['definitions_loaded']}")
print("   By entity:")
for entity, count in stats["by_entity"].items():
    if count > 0:
        print(f"     - {entity}: {count}")

# List SOPs
print()
print("5. SOPs loaded:")
for defn in engine.list_definitions():
    sop_id = defn.get("sop_id", defn.get("name", "unknown"))
    entity = defn.get("entity", "?")
    print(f"   - {sop_id} ({entity})")

# Test dry run
print()
print("6. Testing dry-run...")
definitions = engine.list_definitions()
if definitions:
    test_sop = definitions[0]
    sop_id = test_sop.get("sop_id", test_sop.get("name"))
    result = engine.execute_sop(sop_id, dry_run=True)
    if result["success"]:
        steps = len(result.get("step_results", []))
        print(f"   OK - {sop_id}: {steps} steps executed (dry-run)")
    else:
        print(f"   FAIL - {result.get('error')}")
else:
    print("   SKIP - No SOPs to test")

print()
print("=== Test Complete ===")
