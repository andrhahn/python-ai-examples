# integrate-custom-llm

Demonstrates connecting to a local/self-hosted LLM via Ollama (OpenAI-compatible endpoint).

## Entry Points
- `main.py` — queries the local model

## Env Vars
- `OLLAMA_BASE_URL` (default: http://localhost:11434/v1)
- `OLLAMA_MODEL` (default: llama3)

## Prerequisites
Ollama must be running locally with the target model pulled:
```bash
ollama pull llama3
```

## Run
```bash
source .venv/bin/activate
python main.py
```
