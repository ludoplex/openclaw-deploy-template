"""Read JSON files with block content and write to skill directories."""
import json, os, glob

SKILLS_DIR = r"C:\Users\user\.openclaw\workspace\skills"

FILE_MAP = {
    "1": "operational-substrate/SKILL.md",
    "2": "operational-substrate/references/compositions.md",
    "3": "operational-substrate/references/memetics.md",
    "4": "operational-substrate/references/patterns.md",
    "5": "advanced-search/SKILL.md",
    "6": "advanced-search/references/operators-complete.md",
    "7": "advanced-search/references/query-templates.md",
    "8": "web-reconnaissance/SKILL.md",
    "9": "web-reconnaissance/references/markup-taxonomy.md",
    "10": "web-reconnaissance/references/microformats-structured-data.md",
    "11": "web-reconnaissance/references/tech-fingerprints.md",
    "12": "gov-financial-intel/SKILL.md",
    "13": "gov-financial-intel/references/sec-filing-taxonomy.md",
    "14": "gov-financial-intel/references/fec-money-flows.md",
    "15": "gov-financial-intel/references/agency-databases.md",
    "16": "deep-directory-index/SKILL.md",
    "17": "deep-directory-index/references/libraries-archives.md",
    "18": "deep-directory-index/references/govt-contacts.md",
    "19": "deep-directory-index/references/intl-registries.md",
    "20": "deep-directory-index/references/specialized-databases.md",
    "21": "industry-power-map/SKILL.md",
    "22": "industry-power-map/references/naics-21-mining.md",
    "23": "industry-power-map/references/naics-48-49-transport.md",
    "24": "industry-power-map/references/network-infrastructure.md",
    "25": "industry-power-map/references/naics-52-finance.md",
    "26": "industry-power-map/references/naics-51-information.md",
    "27": "industry-power-map/references/naics-31-33-manufacturing.md",
    "28": "industry-power-map/references/activist-investors.md",
    "29": "industry-power-map/references/union-relations.md",
    "30": "industry-power-map/references/foreign-ownership.md",
    "31": "industry-power-map/references/org-charts.md",
    "32": "industry-power-map/references/naics-44-45-retail.md",
    "33": "industry-power-map/references/naics-53-real-estate.md",
    "34": "industry-power-map/references/naics-62-healthcare.md",
    "35": "industry-power-map/references/naics-22-utilities.md",
    "41": "tech-security-analysis/SKILL.md",
    "42": "tech-security-analysis/references/breach-empirics.md",
    "43": "tech-security-analysis/references/ai-security.md",
    "44": "tech-security-analysis/references/vendor-reality.md",
    "45": "tech-security-analysis/references/compliance-theater.md",
}

total = 0
total_bytes = 0

for jf in sorted(glob.glob(r"C:\Users\user\.openclaw\workspace\tmp\blocks_*.json")):
    print(f"Processing {os.path.basename(jf)}...")
    with open(jf, "r", encoding="utf-8") as f:
        data = json.load(f)
    for idx, content in data.items():
        if idx in FILE_MAP:
            filepath = os.path.join(SKILLS_DIR, FILE_MAP[idx])
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            total += 1
            total_bytes += len(content)
            print(f"  ✓ {FILE_MAP[idx]} ({len(content):,} bytes)")

print(f"\nTotal: {total} files, {total_bytes:,} bytes")
