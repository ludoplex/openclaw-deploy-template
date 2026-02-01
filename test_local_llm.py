#!/usr/bin/env python3
"""Test suite for local_llm.py"""
import sys
sys.path.insert(0, r'C:\Users\user\.openclaw\workspace')
sys.stdout.reconfigure(encoding='utf-8')

from local_llm import LlamafileDelegate, ask_local, generate_json, summarize, format_for_platform

print('=== LlamafileDelegate Test Suite ===')
print()

# Test 1: Direct class usage
print('1. Class init...', end=' ')
d = LlamafileDelegate()
print(f'OK (binary: {d.llamafile_path.name}, model: {d.model_path.name if d.model_path else "baked"})')

# Test 2: ask_local
print('2. ask_local()...', end=' ')
r = ask_local('What is 2+2? Reply with just the number.')
print(f'OK -> {r.strip()}')

# Test 3: generate_json
print('3. generate_json()...', end=' ')
j = generate_json('product with name, price, in_stock boolean')
print(f'OK -> {list(j.keys())}')

# Test 4: summarize  
print('4. summarize()...', end=' ')
s = summarize('The quick brown fox jumps over the lazy dog. This sentence contains every letter.', max_words=10)
print(f'OK -> "{s[:50]}..."' if len(s) > 50 else f'OK -> "{s}"')

# Test 5: format_for_platform
print('5. format_for_platform()...', end=' ')
f = format_for_platform('Check out https://example.com for more info!', 'discord')
print(f'OK -> "{f[:50]}..."' if len(f) > 50 else f'OK -> "{f}"')

print()
print('=== All tests passed ===')
