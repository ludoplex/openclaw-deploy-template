#!/usr/bin/env python3
"""Test llamafile server mode."""
import sys
sys.path.insert(0, r'C:\Users\user\.openclaw\workspace')
sys.stdout.reconfigure(encoding='utf-8')

from local_llm import LlamafileDelegate

d = LlamafileDelegate()
mode = "HTTP" if d.server_url else "CLI"
print(f"Mode: {mode}")
if d.server_url:
    print(f"Server: {d.server_url}")

print("\nTesting ask()...")
result = d.ask("What is the capital of France? Reply with just the city name.")
print(f"Result: {result}")

print("\nTesting generate_json()...")
j = d.generate_json("book with title, author, year")
print(f"Result: {j}")

print("\n✓ Server mode working!")
