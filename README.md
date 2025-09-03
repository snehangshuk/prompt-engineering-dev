## Prompt Engineering for Developers
A lightweight collection of notebooks and examples to practice effective prompt engineering as a developer. Use these notebooks to explore patterns, anti-patterns, and practical workflows.

### What's inside
- **coding-examples.ipynb**: Hands-on examples exploring prompts, iteration, and evaluation.
- **getting_started.ipynb**: A gentle introduction and guided tour.
- **requirements.txt**: Python dependencies for running the notebooks.

### Quickstart
- **Prerequisites**: Python 3.10+ and pip installed; access to Claude Code; VS Code or Cursor recommended.
- **Set up a virtual environment and install deps**:

```bash
cd prompt-eng-for-devs
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- **Configure environment variables**:

```bash
cp .env-default .env
$EDITOR .env
```

Rename `.env-default` to `.env` and edit the values to match your environment (e.g., API keys or tokens required by your workflow). Ensure `.env` is present before running notebooks that depend on environment variables.

- **Launch the notebooks**:

```bash
jupyter lab
# or
jupyter notebook
```

You can also open the folder directly in VS Code or Cursor and use their built-in notebook support. When prompted for a kernel, select the interpreter from `.venv`.

### Using the notebooks
- **Kernel**: Choose the `.venv` Python interpreter as the notebook kernel.
- **Execution order**: Run cells top-to-bottom the first time; then iterate.
- **Saving work**: Keep experiments in new cells; avoid overwriting baseline examples.
 - **Running in VS Code/Cursor**: Open the folder, trust the workspace, use the built-in notebook UI, and select the `.venv` interpreter as the kernel. Run cells via the play buttons or "Run All". Make sure your `.env` is configured so any environment-dependent cells work.

### Contributing
- Issues and pull requests are welcome. Please keep examples minimal, reproducible, and well-labeled.


