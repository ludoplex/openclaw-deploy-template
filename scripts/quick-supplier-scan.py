#!/usr/bin/env python
import sys
sys.path.insert(0, r'C:\zoho-console-api-module-system')
sys.stdout.reconfigure(encoding='utf-8')

from src.core.multi_account import MultiAccountManager
from pathlib import Path
import json

mgr = MultiAccountManager(Path(r'C:\zoho-console-api-module-system\config\accounts.json'))
client = mgr.get_client('mine')

# Known working searches
searches = [
    ('Quill', 'subject:quill'),
    ('D&H', 'subject:D&H OR subject:dandh'),
    ('Ingram', 'subject:ingram'),
    ('SYNNEX', 'subject:synnex'),
    ('Climb', 'subject:climb'),
    ('Lenovo', 'subject:lenovo'),
    ('Dell', 'subject:dell'),
    ('HP', 'subject:HP partner'),
    ('MSI', 'subject:msi'),
    ('IBM', 'subject:ibm'),
    ('Amazon', 'subject:amazon seller'),
    ('eBay', 'subject:ebay'),
    ('sFTP/API', 'subject:sftp OR subject:API credentials'),
    ('Reseller', 'subject:reseller'),
    ('Partner', 'subject:partner'),
    ('LOA', 'subject:authorization'),
]

results = {}
print('=== SUPPLIER EMAIL SEARCH ===\n')

for name, query in searches:
    try:
        msgs = client.search_mail(query, limit=30)
        if msgs:
            print(f'{name}: {len(msgs)} emails')
            results[name] = []
            for m in msgs[:8]:
                sender = m.get('fromAddress', '')
                subj = str(m.get('subject', ''))[:70]
                date = str(m.get('receivedTime', ''))[:10]
                results[name].append({'from': sender, 'subject': subj, 'date': date})
                print(f'    {date} - {sender[:35]} - {subj[:50]}')
        else:
            print(f'{name}: 0 emails')
    except Exception as e:
        print(f'{name}: Error - {e}')
    print()

# Save results
output = r'C:\Users\user\.openclaw\workspace\proposals\mhi-procurement\inbox-supplier-scan.json'
with open(output, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f'\nResults saved to: {output}')
mgr.close_all()
