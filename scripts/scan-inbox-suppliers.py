#!/usr/bin/env python
import sys
sys.path.insert(0, r'C:\zoho-console-api-module-system')
sys.stdout.reconfigure(encoding='utf-8')

from src.core.multi_account import MultiAccountManager
from pathlib import Path
import requests
import json

mgr = MultiAccountManager(Path(r'C:\zoho-console-api-module-system\config\accounts.json'))
client = mgr.get_client('mine')
token = client.auth.get_token()
config = client.config

# Get account ID
headers = {'Authorization': f'Zoho-oauthtoken {token}', 'Accept': 'application/json'}
r = requests.get(f'{config.mail_api_url}/accounts', headers=headers, timeout=30)
account_id = r.json()['data'][0]['accountId']

# Get all folders
r = requests.get(f'{config.mail_api_url}/accounts/{account_id}/folders', headers=headers, timeout=30)
resp = r.json()
folders = resp.get('data', []) if isinstance(resp, dict) else resp
inbox_id = next((f['folderId'] for f in folders if f.get('folderName') == 'Inbox'), None)
print(f'Inbox folder ID: {inbox_id}')

# Supplier domains to look for
supplier_domains = [
    'dandh.com', 'ingrammicro.com', 'synnex.com', 'tdsynnex.com', 
    'climbcs.com', 'climbchannel.com', 'quill.com', 'staples.com',
    'lenovo.com', 'dell.com', 'hp.com', 'hpe.com', 'msi.com', 'ibm.com',
    'amazon.com', 'ebay.com', 'newegg.com', 'walmart.com',
    'vexrobotics.com', 'vex.com', 'asicentral.com', 'grainger.com', 
    'pcbway.com', 'malabs.com', 'ma-labs.com',
    'cisco.com', 'pny.com', 'nvidia.com', 'amd.com', 'intel.com',
    'xyab.com', 'microsoft.com', 'google.com'
]

print('Scanning inbox for supplier emails...\n')

# Get messages with pagination
all_msgs = []
start = 1
while len(all_msgs) < 3000:
    url = f'{config.mail_api_url}/accounts/{account_id}/folders/{inbox_id}/messages'
    r = requests.get(url, headers=headers, params={'start': start, 'limit': 200}, timeout=60)
    if r.status_code != 200:
        print(f'Error fetching: {r.status_code}')
        break
    msgs = r.json().get('data', [])
    if not msgs:
        break
    all_msgs.extend(msgs)
    start += 200
    print(f'  Fetched {len(all_msgs)} messages...')

print(f'\nTotal messages scanned: {len(all_msgs)}')

# Filter for supplier emails
supplier_emails = {}
for m in all_msgs:
    sender = m.get('fromAddress', '').lower()
    for domain in supplier_domains:
        if domain in sender:
            if domain not in supplier_emails:
                supplier_emails[domain] = []
            supplier_emails[domain].append({
                'from': m.get('fromAddress'),
                'subject': str(m.get('subject', ''))[:80],
                'date': m.get('receivedTime', ''),
                'messageId': m.get('messageId', '')
            })
            break

print('\n=== SUPPLIER EMAILS FOUND ===\n')
for domain in sorted(supplier_emails.keys()):
    emails = supplier_emails[domain]
    print(f'### {domain} ({len(emails)} emails)')
    for e in emails[:8]:
        date_str = str(e['date'])[:10] if e['date'] else 'N/A'
        from_str = e['from'][:45] if e['from'] else 'Unknown'
        print(f"  {date_str} | {from_str} | {e['subject']}")
    print()

# Save full results
output_path = r'C:\Users\user\.openclaw\workspace\proposals\mhi-procurement\inbox-supplier-scan.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(supplier_emails, f, indent=2, ensure_ascii=False)
print(f'\nFull results saved to: {output_path}')

mgr.close_all()
