#!/usr/bin/env python3
"""Test dashboard app loads correctly."""
import sys
sys.path.insert(0, '.')

try:
    from src.dashboard.app import app, load_sops, get_sop_stats
    
    print("[OK] Dashboard app imported")
    
    # Test SOP loading
    sops = load_sops()
    total = sum(len(v) for v in sops.values())
    print(f"[OK] Loaded {total} SOPs")
    for entity, entity_sops in sops.items():
        print(f"     {entity}: {len(entity_sops)}")
    
    # Test stats
    stats = get_sop_stats()
    print(f"[OK] Stats: {stats}")
    
    print("\n[SUCCESS] Dashboard ready!")
    print("Run with: python -m uvicorn src.dashboard.app:app --reload --port 8080")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
