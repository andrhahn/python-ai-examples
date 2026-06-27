# agent-example

Demonstrates the Claude Agent SDK (`claude-agent-sdk`) — the high-level SDK that handles the agent loop and tool execution automatically.

Uses `WebSearch` + `WebFetch` tools to research a hardcoded `TOPIC` constant and print a summary. Change `TOPIC` in `main.py` to research anything else.

## Entry Points
- `main.py` — runs the agent

## Env Vars
- `ANTHROPIC_API_KEY`

## Run
```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
