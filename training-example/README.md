# Training Example

A simple example of fine-tuning or training a model on a custom dataset, demonstrating the basics of the training loop and evaluation.

## Concepts Covered

- Preparing a training dataset
- Fine-tuning a pre-trained model (e.g. via HuggingFace or OpenAI fine-tuning API)
- Evaluating model performance before/after fine-tuning

## Setup

> Requires [pyenv](https://github.com/pyenv/pyenv). See the root [README](../README.md) for installation instructions.

```bash
pyenv version          # should show 3.12.4
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your API key if using a hosted fine-tuning API:

```bash
cp .env.example .env
```

## Run

```bash
# Step 1: prepare and validate the training dataset
python prepare_data.py

# Step 2: launch fine-tuning
python train.py

# Step 3: evaluate the fine-tuned model
python evaluate.py
```
