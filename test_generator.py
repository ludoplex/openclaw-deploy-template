#!/usr/bin/env python3
"""Test content generator module."""
import sys
sys.path.insert(0, r'C:\Users\user\.openclaw\workspace')
sys.stdout.reconfigure(encoding='utf-8')

from src.content.generator import generate_post, generate_hashtags

print("=== Content Generator Test ===\n")

print("1. Testing generate_post for Computer Store...")
result = generate_post('computer_store', 'Weekly LAN party this Saturday', 'twitter')
print(f"   Platform: {result['platform']}")
print(f"   Chars: {result['char_count']}")
print(f"   Content: {result['content'][:100]}...")

print("\n2. Testing generate_hashtags...")
tags = generate_hashtags('dsaic', 'new API feature release')
print(f"   Hashtags: {tags}")

print("\n=== Tests complete ===")
