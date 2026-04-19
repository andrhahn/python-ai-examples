# Integrate Custom LLM

An example showing how to integrate a custom or self-hosted LLM (e.g. via Ollama or a local OpenAI-compatible endpoint) alongside or instead of a hosted provider.

## Concepts Covered

- Running a local model with Ollama or a compatible server
- Swapping the base URL to point at a custom endpoint
- Comparing local vs. hosted model responses

## Prerequisites

Install [Ollama](https://ollama.com) and pull a model:

```bash
ollama pull llama3
```

## Setup

> Requires [pyenv](https://github.com/pyenv/pyenv). See the root [README](../README.md) for installation instructions.

```bash
pyenv version          # should show 3.12.4
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```
