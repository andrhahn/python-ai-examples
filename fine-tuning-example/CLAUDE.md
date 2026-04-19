# fine-tuning-example

Demonstrates fine-tuning a model on a custom dataset and evaluating the result.

## Entry Points
- `prepare_data.py` — validates and formats the training dataset
- `train.py` — submits or runs the fine-tuning job
- `evaluate.py` — compares base vs. fine-tuned model outputs

## Env Vars
- `OPENAI_API_KEY` (for hosted fine-tuning API)

## Run
```bash
source .venv/bin/activate
python prepare_data.py
python train.py
python evaluate.py
```
