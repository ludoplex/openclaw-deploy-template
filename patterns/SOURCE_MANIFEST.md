# Source Manifest Methodology

**Purpose:** Prevent agents from hallucinating APIs, reimplementing existing functionality, or writing code that never touches the actual tech stack.

## When to Apply

- Before using any unfamiliar library/framework
- Before integrating with any external system
- When onboarding to an existing codebase
- When source code is available (use BINARY_MANIFEST.md when it isn't)

## Process

### 1. Obtain Actual Source
```bash
# Clone repo
git clone <repo-url>

# Or fetch via GitHub API
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
```

**Not acceptable:** Documentation, examples, blog posts, memory. Only implementation source.

### 2. Enumerate Public Interfaces

For each module/file, extract:
- Exported functions
- Public classes/types
- Constants and enums
- Macros and preprocessor directives
- Header declarations

### 3. Map to Source Locations

For each interface, record:
| Field | Description |
|-------|-------------|
| Name | Function/type/variable name |
| Signature | Full type signature |
| File | Relative path from repo root |
| Line | Line number of definition |
| Purpose | One-line description |

### 4. Document What Does NOT Exist

Explicitly list:
- Functions you might expect but aren't there
- Features implied by docs but not implemented
- APIs from similar libraries that don't exist here
- Deprecated interfaces that were removed

### 5. Compile Reference Manifest

Output file: `{project}-source-manifest.md`

```markdown
# {Project} Source Manifest

Generated: {date}
Source: {repo-url} @ {commit-hash}

## Features

### Feature: {name}
- **Implementing function:** `function_name()`
- **File:** `src/module/file.ts`
- **Line:** 142
- **Signature:** `(param: Type) => ReturnType`

## What Does NOT Exist

- ❌ `fictional_function()` — Not implemented despite documentation
- ❌ `assumed_api()` — Does not exist in this codebase
```

## Validation

Before writing any code that uses a dependency:

1. Check the manifest for the function you intend to call
2. Verify the signature matches your usage
3. Confirm the file/line reference is current
4. If not in manifest, DO NOT USE — research first

## Example

See: `C:\Users\user\openclaw-features-reference.md`

---

*This methodology exists because LLMs hallucinate APIs. The manifest is ground truth.*
