# Compaction Recovery Protocol

## When You Notice Compaction Occurred

If you notice your context has been compacted (conversation feels reset, you have a summary instead of full history), follow this protocol:

### Step 1: Read the Pre-Compaction Snapshot

```
Read: ~/.openclaw/workspace/memory/compaction-review.md
```

This file contains:
- The last 30 messages from before compaction
- The compaction summary for comparison
- A checklist for verification

### Step 2: Verify Critical Information

Check that the compaction summary accurately captured:
1. **Active tasks** - What were we working on?
2. **File paths** - Any files being edited/created?
3. **User preferences** - Any stated preferences or decisions?
4. **Pending items** - What was left to do?
5. **Context** - Why were we doing this?

### Step 3: Correct Any Mis-summarization

If the summary missed or misrepresented something important:
1. Note the discrepancy to the user
2. Incorporate the correct information into your working context
3. Continue the task with accurate context

### Step 4: Clean Up (Optional)

After verifying, you can delete the snapshot:
```
Delete: ~/.openclaw/workspace/memory/compaction-review.md
```

## Why This Matters

Compaction summarization can:
- Lose nuanced context
- Hallucinate details that weren't there
- Miss implicit user preferences
- Drop important file paths or task details

This protocol ensures continuity despite context limitations.
