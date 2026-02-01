# Contributing to Mighty House Inc. SOPs

## Overview

This document outlines how to propose changes, add new SOPs, and maintain the standard operating procedures for all Computer Store locations.

---

## Workflow

### 1. Creating a New SOP

1. Copy `templates/SOP-TEMPLATE.md` to the appropriate section folder
2. Rename following pattern: `SOP-XXX-[short-title].md`
3. Fill in all sections completely
4. Submit for review

### 2. Updating an Existing SOP

1. Create a branch: `update/SOP-XXX-description`
2. Make changes to the SOP file
3. Update the revision history table
4. Increment version number
5. Submit pull request

### 3. Adding a New Location

1. Copy `locations/LOCATION-TEMPLATE.md`
2. Rename to `[city]-[state].md` (lowercase, hyphenated)
3. Fill in all location details
4. Update main README.md expansion list
5. Submit for review

---

## Commit Message Format

All commits must follow this format:

```
[TYPE]-[ID]: Brief description

- Change detail 1
- Change detail 2

Signed-off-by: Name <email@example.com>
```

### Types

- `SOP`: Changes to standard operating procedures
- `APPX`: Changes to appendices
- `LOC`: Changes to location profiles
- `TMPL`: Changes to templates
- `DOCS`: Documentation changes
- `FIX`: Corrections to existing content

### Examples

```
SOP-101: Add laptop intake procedure for gaming laptops

- Added step 4.5 for gaming laptop thermal assessment
- Updated checklist to include GPU stress test

Signed-off-by: John Smith <john@mightyhouse.com>
```

```
LOC: Add Cheyenne, WY location profile

- Created cheyenne-wy.md with full location details
- Updated expansion list in README.md

Signed-off-by: Jane Doe <jane@mightyhouse.com>
```

---

## Review Process

1. All changes require review by store manager or above
2. SOPs affecting multiple sections need cross-department review
3. Legal/compliance SOPs require legal team approval
4. Changes go live on the 1st or 15th of each month

---

## Style Guide

### General

- No emojis in any document
- Use American English spelling
- Write in active voice
- Use numbered lists for sequential steps
- Use bullet lists for non-sequential items

### Formatting

- Use Markdown headers (# ## ###) for structure
- Tables for structured data
- Checklists (- [ ]) for actionable items
- Code blocks for commands or scripts

### Naming

- SOP files: `SOP-XXX-[title].md`
- Appendix files: `Appx-[Letter]-[title].md`
- Location files: `[city]-[state].md`
- All lowercase with hyphens (no spaces)

---

## Questions

Contact the operations team for SOP-related questions.
