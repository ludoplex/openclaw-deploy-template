# Regex & Grep Mastery

The definitive guide to extended regular expressions and grep-family tools.

## Quick Reference

```bash
# Most common patterns
grep -E 'pattern' file              # Extended regex
grep -P 'pattern' file              # Perl-compatible (GNU only)
grep -r --include='*.py' 'def ' .   # Recursive with file filter
rg 'pattern' .                      # ripgrep (fastest, smart defaults)
```

---

## 1. Regex Flavors: BRE vs ERE vs PCRE

### POSIX Basic Regular Expressions (BRE)

Default for `grep`, `sed`, `ed`. Metacharacters must be escaped to activate.

| Character | BRE Meaning | Must escape to use as metachar |
|-----------|-------------|-------------------------------|
| `.` | Any character | ✓ active |
| `*` | Zero or more | ✓ active |
| `^` | Start anchor | ✓ active |
| `$` | End anchor | ✓ active |
| `[...]` | Character class | ✓ active |
| `\(...\)` | Grouping | Escaped form required |
| `\{n,m\}` | Quantifier | Escaped form required |
| `+` `?` `\|` | Literal | Not metacharacters in BRE |

```bash
# BRE: Match "color" or "colour"
grep 'colou\?r' file           # WRONG - \? not valid BRE
grep 'colou*r' file            # Matches "color", "colour", "colouur"...
grep 'colo\(u\)\{0,1\}r' file  # Correct BRE for optional 'u'
```

### POSIX Extended Regular Expressions (ERE)

Used by `grep -E`, `egrep`, `awk`, `sed -E`. Metacharacters active by default.

| Character | ERE Meaning |
|-----------|-------------|
| `.` | Any character |
| `*` | Zero or more |
| `+` | One or more |
| `?` | Zero or one |
| `{n,m}` | Range quantifier |
| `(...)` | Grouping/capturing |
| `\|` | Alternation |
| `^` `$` | Anchors |

```bash
# ERE: Much cleaner
grep -E 'colou?r' file                    # "color" or "colour"
grep -E 'https?://[^ ]+' file             # HTTP or HTTPS URLs
grep -E '^(error|warn|fatal):' file       # Log levels
```

### Perl-Compatible Regular Expressions (PCRE/PCRE2)

Used by `grep -P` (GNU), `pcregrep`, `ripgrep`, most programming languages.

**Additional features over ERE:**

| Feature | Syntax | Example |
|---------|--------|---------|
| Non-greedy | `*?` `+?` `??` | `<.*?>` matches `<a>` not `<a><b>` |
| Lookahead | `(?=...)` `(?!...)` | `foo(?=bar)` matches "foo" only if followed by "bar" |
| Lookbehind | `(?<=...)` `(?<!...)` | `(?<=@)\w+` matches domain after @ |
| Named groups | `(?P<name>...)` | `(?P<year>\d{4})` |
| Non-capturing | `(?:...)` | Groups without capturing |
| Atomic groups | `(?>...)` | Prevents backtracking |
| Possessive | `*+` `++` `?+` | Like atomic, no giveback |
| Word boundary | `\b` | `\bword\b` exact word |
| Unicode props | `\p{L}` `\p{N}` | Unicode letter, number |
| Backreferences | `\1` `\2` | Match same text again |
| Conditionals | `(?(1)yes\|no)` | If group 1 matched... |

```bash
# PCRE examples
grep -P '\d{3}-\d{3}-\d{4}' file          # Phone number (shorthand)
grep -P '(?<=password[=:]\s?)\S+' file    # Password values only
grep -P 'error(?!.*ignore)' file           # "error" not followed by "ignore"
grep -P '(\w+)\s+\1' file                  # Repeated words
```

### Comparison Table

| Feature | BRE | ERE | PCRE |
|---------|-----|-----|------|
| `+` one or more | ❌ | ✓ | ✓ |
| `?` optional | ❌ | ✓ | ✓ |
| `\|` alternation | ❌ | ✓ | ✓ |
| `{n,m}` quantifier | `\{n,m\}` | ✓ | ✓ |
| `(...)` grouping | `\(...\)` | ✓ | ✓ |
| Non-greedy `*?` | ❌ | ❌ | ✓ |
| Lookahead/behind | ❌ | ❌ | ✓ |
| `\d` `\w` `\s` | ❌ | ❌ | ✓ |
| Word boundary `\b` | ❌ | ❌ | ✓ |
| Backreferences | `\1`-`\9` | varies | ✓ |
| Unicode `\p{}` | ❌ | ❌ | ✓ |

---

## 2. Grep Family Tools

### grep vs egrep vs grep -E vs grep -P

```bash
grep 'pattern'      # BRE mode (default)
grep -E 'pattern'   # ERE mode
egrep 'pattern'     # Equivalent to grep -E (deprecated)
grep -F 'string'    # Fixed string (no regex, fastest)
fgrep 'string'      # Equivalent to grep -F (deprecated)
grep -P 'pattern'   # PCRE mode (GNU grep only)
```

**Recommendation:** Use `grep -E` for portable ERE, `grep -P` when you need PCRE features on Linux.

### Essential grep Options

```bash
# Matching control
-i              # Case insensitive
-v              # Invert match (lines NOT matching)
-w              # Whole word only
-x              # Whole line only
-e PATTERN      # Multiple patterns: -e 'foo' -e 'bar'
-f FILE         # Patterns from file

# Output control
-c              # Count matches only
-l              # List filenames with matches
-L              # List filenames without matches
-o              # Print only matched parts
-n              # Print line numbers
-H              # Print filename (default for multi-file)
-h              # Suppress filename

# Context
-A NUM          # Lines after match
-B NUM          # Lines before match
-C NUM          # Lines before and after

# File selection
-r, -R          # Recursive (with/without symlink follow)
--include=GLOB  # Only files matching glob
--exclude=GLOB  # Skip files matching glob
--exclude-dir=DIR  # Skip directories

# Performance
-m NUM          # Stop after NUM matches
--mmap          # Use mmap (sometimes faster)
```

### Modern Alternatives

#### ripgrep (rg) — Recommended

```bash
# Smart defaults: ignores .git, respects .gitignore, recursive
rg 'pattern'                      # Search current directory
rg 'pattern' -t py                # Only Python files
rg 'pattern' -T js                # Exclude JavaScript
rg 'pattern' -g '*.log'           # Glob pattern
rg -l 'pattern'                   # List files only
rg -c 'pattern'                   # Count per file
rg --json 'pattern'               # JSON output for parsing
rg -U 'multi\nline'               # Multiline mode
rg -P '(?<=foo)\w+'               # PCRE2 mode
rg --pcre2-version                # Check PCRE2 availability
```

**ripgrep vs grep performance:** 2-10x faster on large codebases due to:
- Parallel search
- Memory-mapped files
- Smart filtering (skips binary files, respects .gitignore)
- Finite automaton-based matching (no backtracking for most patterns)

#### ag (The Silver Searcher)

```bash
ag 'pattern'                      # Similar to ripgrep
ag 'pattern' --ignore-dir=vendor  # Skip directory
ag 'pattern' -G '\.py$'           # File pattern
```

#### pcregrep

```bash
pcregrep -M 'start.*?\nend' file  # Multiline PCRE
pcregrep -o1 'key=(\w+)' file     # Output capture group 1 only
```

### Platform Differences

| Feature | GNU grep | BSD grep (macOS) | ripgrep |
|---------|----------|------------------|---------|
| `-P` PCRE | ✓ | ❌ | `-P` (PCRE2) |
| `--include` | ✓ | ✓ | `-g` glob |
| `--exclude-dir` | ✓ | ✓ | Automatic |
| `-o` output matched | ✓ | ✓ | ✓ |
| `-Z` null separator | ✓ | ✓ | `--null` |
| Word boundary `\b` | `-P` only | ❌ | ✓ |
| Colored output | `--color` | `--color` | Default |
| Parallel search | ❌ | ❌ | ✓ |

**Portability tip:** For scripts that must work on macOS + Linux:
```bash
# Use grep -E for ERE (works everywhere)
# Avoid grep -P (GNU only)
# Consider bundling ripgrep for complex needs
```

---

## 3. Performance Considerations

### Catastrophic Backtracking

**The Problem:** Exponential time complexity from nested quantifiers.

```bash
# DANGEROUS patterns - avoid these!
(a+)+              # Nested quantifiers
(a|aa)+            # Overlapping alternations
(.*a){10}          # Greedy with required character
\d+\d+             # Adjacent greedy quantifiers matching same chars
```

**Example of catastrophic backtracking:**
```
Pattern: (a+)+b
Input: "aaaaaaaaaaaaaaaaaaaaaaaaaaX"
```
The engine tries every possible way to divide the 'a's between the inner and outer groups, leading to 2^n combinations.

### Solutions

#### 1. Use Possessive Quantifiers (PCRE)
```bash
# Possessive: once matched, never backtrack
grep -P '(a++)+'  # Won't backtrack into inner group
grep -P '\d++\d'  # Will fail fast instead of exponential
```

#### 2. Use Atomic Groups (PCRE)
```bash
# Atomic group: lock match, no backtracking
grep -P '(?>\d+)\d'   # Equivalent to \d++\d
grep -P '(?>foo|foobar)' # Match "foo", never try "foobar"
```

#### 3. Be Specific Instead of Greedy
```bash
# Bad: greedy dot
grep -E '<.*>' file           # May match "<a>...<b>"

# Good: negated character class
grep -E '<[^>]*>' file        # Matches single tags only

# Good: non-greedy (PCRE)
grep -P '<.*?>' file          # Stops at first >
```

#### 4. Anchor When Possible
```bash
# Slow: scans whole line for start
grep -E 'ERROR.*failed'

# Fast: anchored to line start
grep -E '^ERROR.*failed'
```

#### 5. Use Alternation Efficiently
```bash
# Slow: check each alternative from start
grep -E 'error|err|e'

# Fast: longer alternatives first, or factor out common prefix
grep -E 'error|err|e'   # Actually fine, engines optimize
grep -E 'err(or)?|e'    # Explicit factoring
```

### Performance Hierarchy (Fastest to Slowest)

1. **Fixed string (`grep -F`)** — Aho-Corasick or similar
2. **Simple ERE without backrefs** — DFA/NFA, linear time
3. **ERE with backreferences** — Backtracking NFA
4. **PCRE with lookaround** — Extended backtracking
5. **Nested quantifiers** — Potentially exponential

### Benchmarking Tip
```bash
# Time your patterns
time grep -E 'pattern' largefile.log > /dev/null

# Compare with ripgrep
time rg 'pattern' largefile.log > /dev/null

# Hyperfine for proper benchmarks
hyperfine "grep -E 'pattern' file" "rg 'pattern' file"
```

---

## 4. Advanced Features Deep Dive

### Lookahead and Lookbehind (PCRE)

**Zero-width assertions** — they match a position, not characters.

```bash
# Positive lookahead (?=...)
# Match "foo" only if followed by "bar"
grep -P 'foo(?=bar)' file        # Matches "foo" in "foobar"

# Negative lookahead (?!...)
# Match "foo" only if NOT followed by "bar"  
grep -P 'foo(?!bar)' file        # Matches "foo" in "foobaz"

# Positive lookbehind (?<=...)
# Match "bar" only if preceded by "foo"
grep -P '(?<=foo)bar' file       # Matches "bar" in "foobar"

# Negative lookbehind (?<!...)
# Match "bar" only if NOT preceded by "foo"
grep -P '(?<!foo)bar' file       # Matches "bar" in "bazbar"
```

**Practical examples:**
```bash
# Extract values after specific keys
grep -oP '(?<=api_key=)[^\s]+' config.txt
grep -oP '(?<=password:\s)\S+' config.yaml

# Find function calls but not definitions
grep -P 'myFunc\(' --include='*.js' | grep -vP 'function\s+myFunc'

# Match whole word without consuming word boundary
grep -P '(?<![a-zA-Z])error(?![a-zA-Z])' file
```

**Limitations:**
- Lookbehind must be fixed-width in most engines
- `(?<=\w+)` is invalid (variable width)
- `(?<=ab|abc)` is valid (fixed alternatives)
- PCRE2 (ripgrep) supports variable-length lookbehind with `\K`

### The `\K` Escape (PCRE)

Resets the match start, like a variable-width lookbehind:

```bash
# Match only the value, not the key
grep -oP 'password:\s*\K\S+' file    # "secret123"
grep -oP 'user=\K[^&]+' url.txt      # Extract user param value

# ripgrep equivalent
rg -oP 'password:\s*\K\S+' file
```

### Atomic Groups and Possessive Quantifiers

**Atomic group `(?>...)`** — Once the group matches, the engine won't backtrack into it.

```bash
# Without atomic: backtracking possible
grep -P 'a*ab' file          # Can match "aab"

# With atomic: a* consumes all 'a's, no giveback
grep -P '(?>a*)ab' file      # Fails on "aab" (no 'a' left for 'ab')
```

**Possessive quantifiers `*+` `++` `?+`** — Same as atomic, shorter syntax:

```bash
grep -P 'a*+ab' file         # Same as (?>a*)ab

# Useful for performance: fail fast
grep -P '"[^"]*+"' file      # String literal, won't backtrack
grep -P '\d++\.\d++' file    # Decimal number, fast failure
```

### Conditional Patterns (PCRE)

Match different things based on whether a group matched:

```bash
# Syntax: (?(condition)yes-pattern|no-pattern)

# Match optional prefix, require suffix only if prefix present
grep -P '(Mr\.\s)?(?(1)[A-Z][a-z]+|[a-z]+)' file
# If "Mr. " matched, expect capitalized name; otherwise lowercase

# With named groups
grep -P '(?P<prefix>0x)?(?(prefix)[0-9a-fA-F]+|\d+)' file
# Hex if "0x" prefix, decimal otherwise
```

### Branch Reset `(?|...)`

All alternatives share the same capture group numbers:

```bash
# Normally: each alternative has separate groups
grep -oP '(a)|(b)' file       # Group 1 or 2

# Branch reset: both alternatives use group 1
grep -oP '(?|(a)|(b))' file   # Always group 1

# Useful for extracting from different formats
grep -oP '(?|(\d{4})-(\d{2})-(\d{2})|(\d{2})/(\d{2})/(\d{4}))' dates.txt
# Groups 1,2,3 contain year,month,day regardless of format
```

### Unicode Support

```bash
# PCRE Unicode properties
grep -P '\p{L}+'          # Unicode letters
grep -P '\p{N}+'          # Unicode numbers
grep -P '\p{Script=Greek}' # Greek script
grep -P '\p{Emoji}'       # Emoji characters

# ripgrep has good Unicode by default
rg '\w+'                  # Matches Unicode word chars
rg '[\p{L}\p{N}]+'       # Explicit Unicode

# Character class shorthands (PCRE)
\d  = [0-9]              # ASCII digits
\w  = [a-zA-Z0-9_]       # ASCII word
\s  = [ \t\n\r\f]        # ASCII space

# With Unicode mode
(?u)\d = \p{Nd}          # Unicode decimal digits
(?u)\w = [\p{L}\p{N}_]   # Unicode word
```

---

## 5. Common Patterns Library

### Network

```bash
# IPv4 address (strict)
grep -E '\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# IPv4 address (simple, may match invalid)
grep -E '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b'

# IPv6 address (simplified)
grep -E '([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}'

# MAC address
grep -Ei '([0-9a-f]{2}:){5}[0-9a-f]{2}'
grep -Ei '([0-9a-f]{2}-){5}[0-9a-f]{2}'

# Email (simplified, RFC 5322 is complex)
grep -E '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# URL
grep -E 'https?://[^\s<>"{}|\\^`\[\]]+'

# Domain name
grep -E '\b([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
```

### Code Patterns

```bash
# Python function definition
grep -E '^\s*def\s+\w+\s*\('

# JavaScript function (multiple styles)
grep -E '(function\s+\w+|const\s+\w+\s*=\s*(async\s+)?(\([^)]*\)|[a-zA-Z_]\w*)\s*=>)'

# TODO/FIXME/XXX comments
grep -Ei '\b(TODO|FIXME|XXX|HACK|BUG)\b'

# Import statements (Python)
grep -E '^(import|from)\s+\w+'

# Require statements (Node.js)
grep -E "require\(['\"][^'\"]+['\"]\)"

# Potential secrets (broad)
grep -Ei '(password|secret|api_key|token|auth)[=:]\s*['\"][^'\"]{8,}'

# Hardcoded IPs in code
grep -E '['\"][0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}['\"]'

# Console.log/print statements
grep -E '(console\.(log|warn|error)|print\()'
```

### Log Patterns

```bash
# ISO 8601 timestamp
grep -E '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'

# Common log timestamp
grep -E '\d{2}/[A-Z][a-z]{2}/\d{4}:\d{2}:\d{2}:\d{2}'

# Syslog timestamp
grep -E '[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}'

# Log levels
grep -Ei '\b(DEBUG|INFO|WARN(ING)?|ERROR|FATAL|CRITICAL)\b'

# HTTP status codes
grep -E '\b[1-5][0-9]{2}\b'

# Stack trace (Java)
grep -E '^\s+at\s+[\w$.]+\([^)]+\)'

# Stack trace (Python)  
grep -E '^\s+File "[^"]+", line \d+'

# Exception/Error lines
grep -Ei '(exception|error|failure|failed):'
```

### Data Patterns

```bash
# UUID
grep -Ei '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

# ISO date (YYYY-MM-DD)
grep -E '\b\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b'

# US date (MM/DD/YYYY)
grep -E '\b(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}\b'

# Time (HH:MM:SS)
grep -E '\b([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?\b'

# Phone (US formats)
grep -E '\b(\+1[-.\s]?)?(\([0-9]{3}\)|[0-9]{3})[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'

# Credit card (basic, for testing)
grep -E '\b[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}\b'

# MD5 hash
grep -Ei '\b[0-9a-f]{32}\b'

# SHA-256 hash
grep -Ei '\b[0-9a-f]{64}\b'

# Semantic version
grep -E '\bv?[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?\b'

# JSON key-value (simple)
grep -E '"[^"]+"\s*:\s*("[^"]*"|[0-9]+|true|false|null)'
```

---

## 6. Practical Recipes

### Find and Replace with sed

```bash
# Basic substitution
sed 's/old/new/' file
sed 's/old/new/g' file     # All occurrences

# Using ERE (-E or -r)
sed -E 's/https?/ftp/' file

# Capture groups
sed -E 's/([0-9]+)-([0-9]+)/\2-\1/' file   # Swap numbers

# In-place editing
sed -i 's/old/new/g' file           # Linux
sed -i '' 's/old/new/g' file        # macOS

# Delete lines matching pattern
sed '/pattern/d' file

# Print only matching lines (like grep)
sed -n '/pattern/p' file
```

### Multi-file Search and Replace

```bash
# Find files and replace (GNU)
grep -rl 'old' . | xargs sed -i 's/old/new/g'

# With find (safer for filenames with spaces)
find . -name '*.txt' -exec sed -i 's/old/new/g' {} +

# ripgrep + sed
rg -l 'old' | xargs sed -i 's/old/new/g'

# Perl one-liner (powerful)
perl -pi -e 's/old/new/g' *.txt
```

### Extract Specific Data

```bash
# Get only matched portion
grep -oE '[0-9]+\.[0-9]+\.[0-9]+' versions.txt

# Get capture group (Perl/PCRE)
grep -oP 'version=\K[0-9.]+' config

# Count pattern occurrences
grep -oE 'pattern' file | wc -l

# Unique values only
grep -oE 'pattern' file | sort -u

# With frequency count
grep -oE 'pattern' file | sort | uniq -c | sort -rn
```

### Log Analysis

```bash
# Errors in last hour (GNU date)
grep "$(date -d '1 hour ago' '+%Y-%m-%d %H')" app.log | grep -i error

# Top 10 IP addresses
grep -oE '\b[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\b' access.log | sort | uniq -c | sort -rn | head -10

# Requests per hour
grep -oE '\d{2}/\w+/\d{4}:\d{2}' access.log | sort | uniq -c

# Slow requests (>1000ms)
grep -E 'took [0-9]{4,}ms' app.log

# Between timestamps
awk '/2024-01-01 10:00/,/2024-01-01 11:00/' app.log
```

### Code Analysis

```bash
# Find TODO comments with context
grep -rn -A2 -B2 'TODO' --include='*.py'

# Find functions longer than 50 lines
awk '/^def /{start=NR; name=$0} /^def |^class /{if(NR-start>50) print name, start, NR}' *.py

# Find files with more than 100 matches
grep -c 'pattern' *.py | awk -F: '$2 > 100'

# Find duplicate lines
sort file | uniq -d

# Find non-ASCII characters
grep -P '[^\x00-\x7F]' file
```

---

## 7. Tips and Tricks

### Debugging Regular Expressions

1. **Test incrementally** — Build patterns piece by piece
2. **Use regex101.com** — Visual debugging with explanation
3. **Enable verbose mode** (where supported)
   ```bash
   grep -P '(?x)
     \d{4}   # Year
     -       # Separator
     \d{2}   # Month
     -       # Separator
     \d{2}   # Day
   ' file
   ```
4. **Print what matched** — Use `grep -o` to see actual matches

### Escaping Special Characters

```bash
# Characters that need escaping in ERE
. * + ? [ ] ( ) { } | \ ^ $ 

# Escape with backslash
grep -E 'file\.txt' file      # Literal dot
grep -E '\$100' file          # Literal dollar sign
grep -E 'C\+\+' file          # Literal plus signs

# Or use character class for single chars
grep -E 'file[.]txt' file     # Dot in character class

# For many special chars, use -F
grep -F 'a*b+c?' file         # All literal
```

### Handling Binary Files

```bash
# Force text mode
grep -a 'pattern' binary_file

# Skip binary files
grep -I 'pattern' *

# List binary files (invert text check)
file * | grep -v text
```

### Large File Performance

```bash
# Limit matches
grep -m 100 'pattern' hugefile.log

# Stop at first match per file
grep -l 'pattern' *.log

# Use ripgrep for large searches
rg 'pattern' --stats

# Parallel grep (GNU parallel)
cat hugefile.log | parallel --pipe grep 'pattern'
```

### Common Mistakes

```bash
# WRONG: Unquoted pattern (shell expansion)
grep *.txt file        # * expands to filenames!
grep '*.txt' file      # Correct

# WRONG: Forgetting to escape in BRE
grep 'a+b' file        # Matches literal "a+b"
grep 'a\+b' file       # ERE: one or more 'a's
grep -E 'a+b' file     # Better: use ERE mode

# WRONG: Greedy matching surprise
grep -oE '<.*>' file   # Matches entire line between first < and last >
grep -oE '<[^>]*>' file # Correct: non-greedy via negation

# WRONG: Anchors inside alternation
grep -E '^foo|bar$' file  # Matches "^foo" OR "bar$"
grep -E '^(foo|bar)$' file # Correct: full line must be foo or bar
```

---

## 8. Tool Installation

### ripgrep

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian  
apt install ripgrep

# Arch
pacman -S ripgrep

# Windows
choco install ripgrep
winget install BurntSushi.ripgrep

# Cargo
cargo install ripgrep
```

### pcregrep

```bash
# macOS
brew install pcre

# Ubuntu/Debian
apt install pcregrep

# Arch
pacman -S pcre
```

---

## 9. Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    REGEX QUICK REFERENCE                     │
├─────────────────────────────────────────────────────────────┤
│ BASIC                                                        │
│   .       Any character          ^       Start of line       │
│   *       Zero or more           $       End of line         │
│   +       One or more (ERE)      ?       Optional (ERE)      │
│   {n,m}   Range quantifier       |       Alternation (ERE)   │
├─────────────────────────────────────────────────────────────┤
│ CHARACTER CLASSES                                            │
│   [abc]   Any of a, b, c         [^abc]  Not a, b, c         │
│   [a-z]   Range                  [[:alpha:]] POSIX class     │
│   \d      Digit (PCRE)           \w      Word char (PCRE)    │
│   \s      Whitespace (PCRE)      \b      Word boundary       │
├─────────────────────────────────────────────────────────────┤
│ GROUPS & REFERENCES                                          │
│   (...)   Capturing group        (?:...) Non-capturing       │
│   \1      Backreference          (?P<n>) Named group (PCRE)  │
├─────────────────────────────────────────────────────────────┤
│ PCRE ADVANCED                                                │
│   (?=...) Positive lookahead     (?!...) Negative lookahead  │
│   (?<=..) Positive lookbehind    (?<!..) Negative lookbehind │
│   *?      Non-greedy             *+      Possessive          │
│   (?>...) Atomic group           \K      Reset match start   │
├─────────────────────────────────────────────────────────────┤
│ POSIX CLASSES (use inside [...])                             │
│   [:alnum:]  Alphanumeric        [:alpha:]  Letters          │
│   [:digit:]  Digits              [:lower:]  Lowercase        │
│   [:upper:]  Uppercase           [:space:]  Whitespace       │
│   [:punct:]  Punctuation         [:xdigit:] Hex digits       │
├─────────────────────────────────────────────────────────────┤
│ GREP ESSENTIALS                                              │
│   grep -E    Extended regex      grep -P    PCRE (GNU)       │
│   grep -i    Case insensitive    grep -v    Invert match     │
│   grep -o    Only matched part   grep -c    Count matches    │
│   grep -l    List files          grep -n    Line numbers     │
│   grep -r    Recursive           grep -w    Whole word       │
│   grep -A3   3 lines after       grep -B3   3 lines before   │
└─────────────────────────────────────────────────────────────┘
```

---

## See Also

- Scripts in `./scripts/` for practical tools
- Pattern library in `./patterns.json` for copy-paste patterns
- [regex101.com](https://regex101.com) for interactive testing
- `man grep`, `man pcrepattern` for detailed documentation
