---
name: cybersecurity-reality
description: Analytical framework distinguishing cybersecurity industry narrative from empirical reality. Activates when processing cybersecurity news, vendor claims, breach reports, AI/ML security promises, compliance discussions, or threat intelligence. Cross-references marketing claims against breach post-mortems, insurance actuarial data, and practitioner surveys. Designed for integration with web-reconnaissance and advanced-search skills for time-sensitive analysis.
---

# Cybersecurity: Narrative vs Reality

## Purpose

Provide grounded analysis when cybersecurity topics arise. The $215B security industry systematically overpromises prevention while delivering detection. This skill identifies gaps between vendor narratives and empirical outcomes.

## Core Framework

### The Spending-Breach Paradox
```
INPUT:  $215B annual spend, 130+ tools per enterprise, 59% budget increases
OUTPUT: 61% breach rate, 11-day median dwell time (rising), 57% external detection

Conclusion: Investment ≠ outcomes. Configuration, integration, operations fail.
```

### Narrative-Reality Decoder

When encountering claims, apply:

| Claim Pattern | Reality Check |
|---------------|---------------|
| "AI-powered prevention" | AI reduces cost $1.9M, lifecycle 80 days—does NOT prevent intrusion |
| "Zero Trust architecture" | 2024: MITRE, Change Healthcare, AT&T all breached despite ZT |
| "EDR visibility" | 66% malware hits devices WITH endpoint security installed |
| "Real-time detection" | 57% breaches detected by external parties, not internal tools |
| "Autonomous SOC" | Gartner 2025: "There Will Never Be an Autonomous SOC" |
| "Compliant = Secure" | 0% of breached orgs were fully compliant at breach time |

### Time-Sensitivity Protocol

Cybersecurity information decays rapidly:

| Intelligence Type | Half-Life | Implication |
|-------------------|-----------|-------------|
| CVE to exploit | 5 days | Monthly patching = window closed |
| IP/domain IOCs | 48 hours | 80% gone from telemetry in 10 days |
| Ransomware brand | 9-24 months | Group names obsolete quickly |
| Threat intel report | 33 days avg | Infrastructure abandoned before publication |

**When analyzing security news: ALWAYS search for current state.** Historical context from this skill + real-time search = complete picture.

## Integration Protocol

This skill is designed for chained activation:

```
1. web-reconnaissance detects security content/entity
2. → triggers cybersecurity-reality lens
3. → advanced-search queries for:
   - CVE disclosures affecting entity (last 30 days)
   - Breach disclosures (last 90 days)
   - Vendor M&A/financial status
   - Regulatory enforcement
   - Ransomware group activity
4. → synthesize: narrative claim + empirical reality + current intel
```

## Reference Files

- `references/breach-empirics.md` — Verizon DBIR, Mandiant M-Trends, insurance data
- `references/vendor-reality.md` — Tool effectiveness, shelfware rates, incentive structures
- `references/ai-security-hype.md` — Gartner positioning, autonomous SOC myth, adversarial ML
- `references/compliance-theater.md` — PCI failures, training ineffectiveness, annual testing gaps

## Analysis Triggers

Activate this framework when encountering:
- Breach announcements (apply empirics, search for current details)
- Vendor capability claims (decode against reality matrix)
- "AI security" discussions (apply Gartner hype cycle position)
- Compliance certifications (note: 0% correlation with breach prevention)
- Threat intelligence (apply decay rates, search for current IOCs)
- Security spending discussions (apply shelfware data: 28-60% unused)

## Output Format

When applying this skill, structure analysis as:

```
NARRATIVE: [What is being claimed]
REALITY: [What empirical data shows]
CURRENT: [What search reveals now]
IMPLICATION: [What this means for the entity/situation]
```
