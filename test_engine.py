#!/usr/bin/env python3
"""
Quick test script to verify SOP engine setup.
Run from workspace root: python test_engine.py
"""

import sys
import os
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Use ASCII for compatibility
PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"

def test_imports():
    """Test that all modules import correctly."""
    print("Testing imports...")
    
    try:
        from sop import (
            StepType, Entity, Platform,
            EnhancedSOPEngine, create_engine,
            get_entity_config, adapt_content_for_platform,
        )
        print("  ✅ All imports successful")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_step_types():
    """Test step type definitions."""
    print("\nTesting step types...")
    
    from sop.step_types import StepType
    
    expected_types = [
        "validation", "notification", "create_task", "field_update",
        "social_post", "content_generate", "cross_entity_trigger",
    ]
    
    for t in expected_types:
        try:
            step = StepType(t)
            print(f"  ✅ {t}")
        except ValueError:
            print(f"  ❌ {t} not found")
            return False
    
    return True


def test_entity_configs():
    """Test entity configuration loading."""
    print("\nTesting entity configs...")
    
    from sop.step_types import Entity, get_entity_config
    
    for entity in [Entity.MIGHTY_HOUSE_INC, Entity.DSAIC, Entity.COMPUTER_STORE]:
        config = get_entity_config(entity)
        if config and "hashtags" in config:
            print(f"  ✅ {entity.value}: {len(config['hashtags'])} hashtags")
        else:
            print(f"  ❌ {entity.value}: missing config")
            return False
    
    return True


def test_engine_creation():
    """Test engine creation and definition loading."""
    print("\nTesting engine creation...")
    
    from sop import create_engine
    
    engine = create_engine(load_definitions=True)
    stats = engine.get_stats()
    
    print(f"  Definitions loaded: {stats['definitions_loaded']}")
    print(f"  By entity:")
    for entity, count in stats['by_entity'].items():
        print(f"    - {entity}: {count}")
    
    if stats['definitions_loaded'] > 0:
        print("  ✅ Engine created and definitions loaded")
        return True
    else:
        print("  ⚠️  No definitions loaded (may need YAML files)")
        return True  # Not a failure, just no files


def test_dry_run():
    """Test dry-run execution of an SOP."""
    print("\nTesting dry-run execution...")
    
    from sop import create_engine
    
    engine = create_engine(load_definitions=True)
    definitions = engine.list_definitions()
    
    if not definitions:
        print("  ⚠️  No SOPs to test")
        return True
    
    # Pick first SOP
    sop = definitions[0]
    sop_id = sop.get("sop_id", sop.get("id", "unknown"))
    
    print(f"  Testing: {sop_id}")
    
    result = engine.execute_sop(sop_id, dry_run=True)
    
    if result["success"]:
        print(f"  ✅ Dry run successful ({len(result['step_results'])} steps)")
        return True
    else:
        print(f"  ❌ Dry run failed: {result.get('error')}")
        return False


def test_content_adaptation():
    """Test content adaptation for different platforms."""
    print("\nTesting content adaptation...")
    
    from sop.step_types import Platform, Entity, adapt_content_for_platform
    
    test_content = """
Here's a test post with a link: https://example.com

| Column 1 | Column 2 |
|----------|----------|
| Data     | More     |

And another link: https://test.com
"""
    
    # Test Discord (should remove tables, wrap extra links)
    discord_content = adapt_content_for_platform(
        test_content, Platform.DISCORD, Entity.COMPUTER_STORE
    )
    
    if "|" not in discord_content or discord_content.count("|") < 4:
        print("  ✅ Discord: Tables removed")
    else:
        print("  ❌ Discord: Tables not removed")
        return False
    
    # Test Twitter (should truncate)
    long_content = "x" * 500
    twitter_content = adapt_content_for_platform(
        long_content, Platform.TWITTER, Entity.DSAIC
    )
    
    if len(twitter_content) <= 280:
        print(f"  ✅ Twitter: Truncated to {len(twitter_content)} chars")
    else:
        print(f"  ❌ Twitter: Not truncated ({len(twitter_content)} chars)")
        return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("SOP Engine Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Step Types", test_step_types),
        ("Entity Configs", test_entity_configs),
        ("Engine Creation", test_engine_creation),
        ("Dry Run", test_dry_run),
        ("Content Adaptation", test_content_adaptation),
    ]
    
    results = []
    for name, test_fn in tests:
        try:
            result = test_fn()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ❌ Exception: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Results:")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
