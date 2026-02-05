"""Extract Claude.ai skill code blocks via CDP and save to skill directories."""
import json, os, sys

try:
    import websocket
except ImportError:
    os.system("pip install websocket-client -q")
    import websocket

SKILLS_DIR = r"C:\Users\user\.openclaw\workspace\skills"
CDP_URL = "ws://127.0.0.1:18793/cdp"
TARGET_ID = "84DABB53948F8DFDC7CA6F085BBF7097"

# Map code block index -> file path (relative to SKILLS_DIR)
FILE_MAP = {
    1: "operational-substrate/SKILL.md",
    2: "operational-substrate/references/compositions.md",
    3: "operational-substrate/references/memetics.md",
    4: "operational-substrate/references/patterns.md",
    5: "advanced-search/SKILL.md",
    6: "advanced-search/references/operators-complete.md",
    7: "advanced-search/references/query-templates.md",
    8: "web-reconnaissance/SKILL.md",
    9: "web-reconnaissance/references/markup-taxonomy.md",
    10: "web-reconnaissance/references/microformats-structured-data.md",
    11: "web-reconnaissance/references/tech-fingerprints.md",
    12: "gov-financial-intel/SKILL.md",
    13: "gov-financial-intel/references/sec-filing-taxonomy.md",
    14: "gov-financial-intel/references/fec-money-flows.md",
    15: "gov-financial-intel/references/agency-databases.md",
    16: "deep-directory-index/SKILL.md",
    17: "deep-directory-index/references/libraries-archives.md",
    18: "deep-directory-index/references/govt-contacts.md",
    19: "deep-directory-index/references/intl-registries.md",
    20: "deep-directory-index/references/specialized-databases.md",
    21: "industry-power-map/SKILL.md",
    22: "industry-power-map/references/naics-21-mining.md",
    23: "industry-power-map/references/naics-48-49-transport.md",
    24: "industry-power-map/references/network-infrastructure.md",
    25: "industry-power-map/references/naics-52-finance.md",
    26: "industry-power-map/references/naics-51-information.md",
    27: "industry-power-map/references/naics-31-33-manufacturing.md",
    28: "industry-power-map/references/activist-investors.md",
    29: "industry-power-map/references/union-relations.md",
    30: "industry-power-map/references/foreign-ownership.md",
    31: "industry-power-map/references/org-charts.md",
    32: "industry-power-map/references/naics-44-45-retail.md",
    33: "industry-power-map/references/naics-53-real-estate.md",
    34: "industry-power-map/references/naics-62-healthcare.md",
    35: "industry-power-map/references/naics-22-utilities.md",
    41: "tech-security-analysis/SKILL.md",
    42: "tech-security-analysis/references/breach-empirics.md",
    43: "tech-security-analysis/references/ai-security.md",
    44: "tech-security-analysis/references/vendor-reality.md",
    45: "tech-security-analysis/references/compliance-theater.md",
}

def extract_blocks(ws, indices):
    """Extract code blocks by index from the page."""
    js = f"""
    (() => {{
        const blocks = document.querySelectorAll('pre code, code[class*="language"]');
        const result = {{}};
        {json.dumps(indices)}.forEach(i => {{
            if (blocks[i]) result[i] = blocks[i].innerText;
        }});
        return JSON.stringify(result);
    }})()
    """
    msg_id = 1
    # First, attach to target
    ws.send(json.dumps({
        "id": msg_id,
        "method": "Target.attachToTarget",
        "params": {"targetId": TARGET_ID, "flatten": True}
    }))
    
    # Read responses until we get our result
    session_id = None
    for _ in range(20):
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id and "result" in resp:
            session_id = resp["result"].get("sessionId")
            break
    
    if not session_id:
        print("ERROR: Could not attach to target")
        return {}
    
    msg_id = 2
    ws.send(json.dumps({
        "id": msg_id,
        "method": "Runtime.evaluate",
        "params": {"expression": js, "returnByValue": True},
        "sessionId": session_id
    }))
    
    for _ in range(30):
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id and "result" in resp:
            value = resp["result"].get("result", {}).get("value", "{}")
            return json.loads(value)
    
    return {}

def main():
    print(f"Connecting to CDP at {CDP_URL}...")
    ws = websocket.create_connection(CDP_URL, timeout=30)
    
    all_indices = sorted(FILE_MAP.keys())
    total_written = 0
    total_bytes = 0
    
    # Extract in batches
    batches = [
        all_indices[i:i+10] for i in range(0, len(all_indices), 10)
    ]
    
    for batch_num, batch in enumerate(batches):
        print(f"Extracting batch {batch_num+1}/{len(batches)}: indices {batch[0]}-{batch[-1]}...")
        blocks = extract_blocks(ws, batch)
        
        for idx_str, content in blocks.items():
            idx = int(idx_str)
            if idx in FILE_MAP:
                filepath = os.path.join(SKILLS_DIR, FILE_MAP[idx])
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                total_written += 1
                total_bytes += len(content)
                print(f"  ✓ {FILE_MAP[idx]} ({len(content)} bytes)")
    
    ws.close()
    print(f"\nDone! Written {total_written} files, {total_bytes:,} bytes total")

if __name__ == "__main__":
    main()
