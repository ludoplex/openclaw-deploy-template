"""Use Playwright to connect to Chrome relay and extract all skill blocks."""
import json, os, asyncio
from playwright.async_api import async_playwright

SKILLS_DIR = r"C:\Users\user\.openclaw\workspace\skills"

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

async def main():
    async with async_playwright() as p:
        print("Connecting to Chrome via CDP...")
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:18793")
        
        # Find the Claude.ai tab
        contexts = browser.contexts
        page = None
        for ctx in contexts:
            for pg in ctx.pages:
                if "claude.ai/chat/9b766c00" in pg.url:
                    page = pg
                    break
            if page:
                break
        
        if not page:
            print("ERROR: Could not find Claude.ai chat tab")
            # Try to list all pages
            for ctx in contexts:
                for pg in ctx.pages:
                    print(f"  Found: {pg.url[:80]}")
            return
        
        print(f"Found tab: {page.url[:60]}...")
        
        # Extract ALL blocks at once
        all_indices = sorted(FILE_MAP.keys())
        total = 0
        total_bytes = 0
        
        # Do it in batches to avoid JS memory issues
        batches = [all_indices[i:i+8] for i in range(0, len(all_indices), 8)]
        
        for batch in batches:
            js = f"""
            (() => {{
                const blocks = document.querySelectorAll('pre code, code[class*="language"]');
                const r = {{}};
                {json.dumps(batch)}.forEach(i => {{
                    if(blocks[i]) r[i] = blocks[i].innerText;
                }});
                return r;
            }})()
            """
            result = await page.evaluate(js)
            
            for idx_str, content in result.items():
                idx = int(idx_str)
                if idx in FILE_MAP:
                    filepath = os.path.join(SKILLS_DIR, FILE_MAP[idx])
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    total += 1
                    total_bytes += len(content.encode('utf-8'))
                    print(f"  ✓ {FILE_MAP[idx]} ({len(content):,} chars)")
        
        print(f"\nDone! {total} files, {total_bytes:,} bytes")
        browser.close()

asyncio.run(main())
