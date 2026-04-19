# Python AI Examples

A collection of hands-on AI projects for building experience across core AI/ML concepts. Each subfolder is a self-contained example with its own dependencies and instructions.

> `CLAUDE.md` files are included in each folder to provide context for [Claude Code](https://claude.ai/code) sessions. If you're using a different AI coding tool (Cursor, Copilot, Codex, etc.), these files can serve as a reference for project context.

## Projects

| Folder | Concept |
|--------|---------|
| [agent-example](./agent-example/) | Building autonomous AI agents |
| [gen-ai-example](./gen-ai-example/) | Generative AI with LLMs |
| [integrate-custom-llm](./integrate-custom-llm/) | Integrating a custom or self-hosted LLM |
| [multi-agent-example](./multi-agent-example/) | Orchestrating multiple agents |
| [prompt-example](./prompt-example/) | Prompt engineering techniques |
| [rag-model-example](./rag-model-example/) | Retrieval-Augmented Generation (RAG) basics |
| [rag-model-library-book](./rag-model-library-book/) | RAG applied to a book/library use case |
| [training-example](./training-example/) | Fine-tuning / training a model |

## Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) — manages the Python version (3.12.4 is pinned in `.python-version`)
- An API key for your chosen LLM provider (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)

### Install pyenv

**macOS**
```bash
brew install pyenv
```

Add to `~/.zshrc` (or `~/.bashrc`):
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

**Linux**
```bash
curl https://pyenv.run | bash
```

Add to `~/.bashrc`:
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

**Windows** — use [pyenv-win](https://github.com/pyenv-win/pyenv-win)
```powershell
# PowerShell (run as Administrator)
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

Restart your terminal, then add `PYENV`, `PYENV_ROOT`, and `PYENV_HOME` to your user environment variables if the installer didn't do so automatically. See the [pyenv-win docs](https://github.com/pyenv-win/pyenv-win#installation) for details.

---

Then install the required Python version (all platforms):

```bash
pyenv install 3.12.4
```

## General Setup

### Running an example

Each subfolder has its own `requirements.txt` and venv:

```bash
# macOS / Linux
cd <project-folder>
pyenv version                      # should show 3.12.4
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```powershell
# Windows (PowerShell)
cd <project-folder>
pyenv version                      # should show 3.12.4
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Then follow the instructions in that folder's `README.md`.

### Dev tooling (ruff, pre-commit)

To use linting and formatting tools, set up a root-level venv once:

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

```powershell
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
```

## Testing

Uses [pytest](https://docs.pytest.org/). Each subfolder has a `tests/` directory. Run from any subfolder or the repo root:

```bash
pytest
```


## Linting & Formatting

Uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting (config in `ruff.toml`). After completing dev tooling setup above, ruff runs automatically on every commit. To run manually, execute from the repo root or any subfolder — ruff finds the config automatically:

```bash
ruff check .          # lint
ruff check --fix .    # lint + auto-fix
ruff format .         # format
```

## Environment Variables

Each project includes a `.env.example` listing the required keys. Copy it to `.env` and fill in your values — `.env` is gitignored and will never be committed.

```bash
cp .env.example .env
# edit .env and set your API keys
```

| Variable | Used by |
|----------|---------|
| `ANTHROPIC_API_KEY` | agent, gen-ai, multi-agent, prompt, rag projects |
| `LLM_MODEL` | rag-model-example, rag-model-library-book |
| `EMBEDDING_MODEL` | rag-model-example, rag-model-library-book |
| `OPENAI_API_KEY` | training-example |
| `OLLAMA_BASE_URL` | integrate-custom-llm |
| `OLLAMA_MODEL` | integrate-custom-llm |

## License

[MIT](LICENSE)
