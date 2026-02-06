# Transcript Integrity Check Hook

## Purpose
Prevents unauthorized modification or deletion of agent transcripts.

## Enforcement
1. **SHA256 Manifest**: Every transcript has its hash recorded in `.manifest.json` at capture time
2. **Verification**: Run `node scripts/capture-subagent-transcripts.js --verify` to check integrity
3. **Git Protection**: Transcripts are committed immediately after capture

## Usage

**Capture new transcript:**
```bash
node scripts/capture-subagent-transcripts.js <agentId>
```

**Verify all transcripts:**
```bash
node scripts/capture-subagent-transcripts.js --verify
```

## Audit Trail
The manifest contains:
- SHA256 hash of each transcript
- Capture timestamp
- Agent ID
- Session ID  
- File size

If anyone modifies a transcript, verification will fail and show the discrepancy.
