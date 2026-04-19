# Prompt Example

Examples of common prompt engineering techniques and how they affect model output.

## Concepts Covered

- Zero-shot vs. few-shot prompting
- Chain-of-thought (CoT) prompting
- Role prompting and system instructions
- Output formatting (JSON, markdown)

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

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. See the root [README](../README.md#linting--formatting) for setup and usage instructions.
