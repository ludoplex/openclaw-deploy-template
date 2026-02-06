# Subagent Transcript Capture Hook

## Purpose
Automatically capture human-readable transcripts of all spawned subagent sessions, including:
- Full reasoning (thinking blocks)
- Tool calls and outputs
- Inter-agent discourse
- Final deliverables

## Trigger
- `sessions_spawn` completion (when subagent announces back to main)
- Can also be invoked manually via handler

## Output
Creates `memory/agent-transcripts/{agentId}-{sessionId}-{timestamp}.md` with:
1. Session metadata (agent, task, duration)
2. Full thinking/reasoning blocks (extracted from JSONL)
3. All tool calls with results
4. Final output/findings

## Configuration
- `transcriptDir`: Where to save transcripts (default: `memory/agent-transcripts/`)
- `includeThinking`: Include thinking blocks (default: true)
- `includeToolCalls`: Include tool calls/results (default: true)
