# tree-sitter Source Manifest

Generated: 2026-02-11
Source: https://github.com/tree-sitter/tree-sitter @ main
Path: `C:\tree-sitter`

## Overview

Tree-sitter is an incremental parsing library written in C. It builds concrete syntax trees for source files and efficiently updates them as the source changes. Used by Aider for repo-map generation and code context selection.

## Core C API (`lib/include/tree_sitter/api.h`)

### Types
| Name | Line | Purpose |
|------|------|---------|
| `TSParser` | ~38 | Opaque parser handle |
| `TSTree` | ~39 | Parsed syntax tree |
| `TSNode` | ~108-112 | Node in the tree |
| `TSQuery` | ~40 | Pattern matching query |
| `TSQueryCursor` | ~41 | Iterator over query matches |
| `TSLanguage` | ~37 | Language grammar definition |
| `TSPoint` | ~63-66 | Row/column position |
| `TSRange` | ~68-73 | Byte and point range |
| `TSInput` | ~75-80 | Input abstraction for parsing |
| `TSInputEdit` | ~101-108 | Edit descriptor for incremental parsing |
| `TSTreeCursor` | ~114-118 | Cursor for tree traversal |

### Parser Functions
| Name | Signature | File | Line | Purpose |
|------|-----------|------|------|---------|
| `ts_parser_new` | `() -> TSParser*` | lib/src/parser.c | ~50 | Create new parser |
| `ts_parser_delete` | `(TSParser*)` | lib/src/parser.c | ~70 | Free parser |
| `ts_parser_set_language` | `(TSParser*, TSLanguage*) -> bool` | lib/src/parser.c | ~90 | Set grammar |
| `ts_parser_parse` | `(TSParser*, TSTree*, TSInput) -> TSTree*` | lib/src/parser.c | ~200 | Parse input |
| `ts_parser_parse_string` | `(TSParser*, TSTree*, char*, uint32_t) -> TSTree*` | lib/src/parser.c | ~250 | Parse string |

### Tree Functions
| Name | Signature | File | Line | Purpose |
|------|-----------|------|------|---------|
| `ts_tree_root_node` | `(TSTree*) -> TSNode` | lib/src/tree.c | ~50 | Get root node |
| `ts_tree_delete` | `(TSTree*)` | lib/src/tree.c | ~40 | Free tree |
| `ts_tree_edit` | `(TSTree*, TSInputEdit*)` | lib/src/tree.c | ~100 | Apply edit for incremental parse |
| `ts_tree_get_changed_ranges` | `(TSTree*, TSTree*, uint32_t*) -> TSRange*` | lib/src/get_changed_ranges.c | ~50 | Get changed ranges |

### Node Functions
| Name | Signature | File | Line | Purpose |
|------|-----------|------|------|---------|
| `ts_node_type` | `(TSNode) -> char*` | lib/src/node.c | ~50 | Get node type name |
| `ts_node_symbol` | `(TSNode) -> TSSymbol` | lib/src/node.c | ~60 | Get symbol ID |
| `ts_node_start_byte` | `(TSNode) -> uint32_t` | lib/src/node.c | ~80 | Start byte offset |
| `ts_node_end_byte` | `(TSNode) -> uint32_t` | lib/src/node.c | ~90 | End byte offset |
| `ts_node_start_point` | `(TSNode) -> TSPoint` | lib/src/node.c | ~100 | Start row/col |
| `ts_node_end_point` | `(TSNode) -> TSPoint` | lib/src/node.c | ~110 | End row/col |
| `ts_node_string` | `(TSNode) -> char*` | lib/src/node.c | ~120 | S-expression string |
| `ts_node_child_count` | `(TSNode) -> uint32_t` | lib/src/node.c | ~140 | Number of children |
| `ts_node_child` | `(TSNode, uint32_t) -> TSNode` | lib/src/node.c | ~150 | Get child by index |
| `ts_node_parent` | `(TSNode) -> TSNode` | lib/src/node.c | ~200 | Get parent node |
| `ts_node_next_sibling` | `(TSNode) -> TSNode` | lib/src/node.c | ~220 | Next sibling |
| `ts_node_prev_sibling` | `(TSNode) -> TSNode` | lib/src/node.c | ~230 | Previous sibling |

### Query Functions
| Name | Signature | File | Line | Purpose |
|------|-----------|------|------|---------|
| `ts_query_new` | `(TSLanguage*, char*, uint32_t, uint32_t*, TSQueryError*) -> TSQuery*` | lib/src/query.c | ~500 | Compile query pattern |
| `ts_query_delete` | `(TSQuery*)` | lib/src/query.c | ~600 | Free query |
| `ts_query_cursor_new` | `() -> TSQueryCursor*` | lib/src/query.c | ~700 | Create cursor |
| `ts_query_cursor_exec` | `(TSQueryCursor*, TSQuery*, TSNode)` | lib/src/query.c | ~750 | Execute query |
| `ts_query_cursor_next_match` | `(TSQueryCursor*, TSQueryMatch*) -> bool` | lib/src/query.c | ~800 | Get next match |
| `ts_query_cursor_next_capture` | `(TSQueryCursor*, TSQueryMatch*, uint32_t*) -> bool` | lib/src/query.c | ~850 | Get next capture |

### Tree Cursor Functions
| Name | Signature | File | Line | Purpose |
|------|-----------|------|------|---------|
| `ts_tree_cursor_new` | `(TSNode) -> TSTreeCursor` | lib/src/tree_cursor.c | ~50 | Create cursor at node |
| `ts_tree_cursor_delete` | `(TSTreeCursor*)` | lib/src/tree_cursor.c | ~70 | Free cursor |
| `ts_tree_cursor_goto_first_child` | `(TSTreeCursor*) -> bool` | lib/src/tree_cursor.c | ~100 | Move to first child |
| `ts_tree_cursor_goto_next_sibling` | `(TSTreeCursor*) -> bool` | lib/src/tree_cursor.c | ~120 | Move to next sibling |
| `ts_tree_cursor_goto_parent` | `(TSTreeCursor*) -> bool` | lib/src/tree_cursor.c | ~140 | Move to parent |
| `ts_tree_cursor_current_node` | `(TSTreeCursor*) -> TSNode` | lib/src/tree_cursor.c | ~160 | Get current node |

## Python Bindings (py-tree-sitter)

Separate package: `pip install tree-sitter`

| Function | Purpose |
|----------|---------|
| `Parser()` | Create parser |
| `parser.set_language(lang)` | Set language |
| `parser.parse(source)` | Parse bytes to tree |
| `tree.root_node` | Get root |
| `node.children` | Child nodes |
| `node.type` | Node type string |
| `node.start_point`, `node.end_point` | Position tuples |
| `Language.build_library(path, [grammars])` | Build language library |

## Language Grammars

Each language has a separate repo: `tree-sitter-{lang}`
- `tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-c`, etc.
- Grammars define `grammar.js` → generates `parser.c`

## Key Files

| Path | Purpose |
|------|---------|
| `lib/include/tree_sitter/api.h` | Public C API header |
| `lib/src/parser.c` | Parser implementation |
| `lib/src/tree.c` | Tree operations |
| `lib/src/node.c` | Node operations |
| `lib/src/query.c` | Query pattern matching |
| `lib/src/tree_cursor.c` | Tree traversal cursor |
| `cli/` | Tree-sitter CLI (Rust) |
| `lib/binding_rust/` | Rust bindings |
| `lib/binding_web/` | WASM bindings |

## What Does NOT Exist

- ❌ No built-in semantic analysis — syntax only
- ❌ No type inference
- ❌ No cross-file analysis
- ❌ No LSP server — use tree-sitter-cli or integrate
- ❌ No diff/patch generation — only tree comparison

## Integration Pattern (Aider Style)

```python
from tree_sitter import Parser, Language
import tree_sitter_python

parser = Parser()
parser.set_language(tree_sitter_python.language())

tree = parser.parse(source_bytes)
root = tree.root_node

# Walk tree for function/class definitions
def walk(node, depth=0):
    if node.type in ('function_definition', 'class_definition'):
        name = node.child_by_field_name('name')
        print(f"{' '*depth}{node.type}: {name.text.decode()}")
    for child in node.children:
        walk(child, depth+1)

walk(root)
```

---

*This manifest is ground truth. Verify before using any function.*
