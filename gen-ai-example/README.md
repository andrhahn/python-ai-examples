# Generative AI Example

A simple example demonstrating text generation with a large language model, including basic prompt construction and response handling.

## Concepts Covered

- Calling an LLM API (chat completions)
- System vs. user messages
- Streaming responses
- Token usage and cost awareness

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
