#!/usr/bin/env python3
"""Test AI content generator."""
import sys
sys.path.insert(0, r'C:\Users\user\.openclaw\workspace')
sys.stdout.reconfigure(encoding='utf-8')

from src.content.ai_generator import AIContentGenerator, generate_hashtags, generate_content_brief

print("=== AI Content Generator Test ===\n")

# Initialize
print("1. Initializing generator...", end=" ")
gen = AIContentGenerator()
print(f"OK (mode: {gen.mode})")

# Test hashtag generation
print("\n2. Testing hashtag generation...")
hashtags = gen.generate_hashtags(
    "Join us for our weekly LAN party! Fortnite tournament this Saturday.",
    "computer_store",
    count=5
)
print(f"   Hashtags: {hashtags}")

# Test content brief
print("\n3. Testing content brief generation...")
brief = gen.generate_content_brief(
    entity="dsaic",
    category="announcement",
    topic="New API rate limiting feature"
)
print(f"   Brief: {brief}")

# Test platform adaptation
print("\n4. Testing platform adaptation...")
original = "🎮 Big news! We just upgraded our gaming PCs to RTX 4080s! Come check them out at the Computer Store in Wheatland. Open 10am-8pm daily. https://computerstore.example.com"
adapted = gen.adapt_for_platform(original, "twitter")
print(f"   Twitter version: {adapted[:100]}...")

print("\n=== All tests complete ===")
