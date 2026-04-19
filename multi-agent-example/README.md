# Multi-Agent Example

An example demonstrating how to orchestrate multiple AI agents working together to solve a problem, with each agent handling a specialized role.

## Concepts Covered

- Defining specialized sub-agents (e.g. researcher, writer, reviewer)
- Passing context between agents
- Orchestrator / worker patterns

## Setup

> Requires [pyenv](https://github.com/pyenv/pyenv). See the root [README](../README.md) for installation instructions.

```bash
pyenv version          # should show 3.12.4
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY or OPENAI_API_KEY
```

## Run

```bash
python main.py
```
