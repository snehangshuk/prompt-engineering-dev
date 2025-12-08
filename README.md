# Advanced Prompt Engineering for Developers

Master prompting techniques for software development with structured tutorials, hands-on exercises, and real-world examples.

## 🚀 Get Started

**1. Clone the repository:**
```bash
git clone git@cd.splunkdev.com:eng-enablement/prompteng-devs.git
cd prompteng-devs
```

**2. Begin learning:**
- **[Start Module 1: Foundations](./01-course/module-01-foundations/)** ← Read README.md, then open the `.ipynb` notebook
- **[View All Modules](./01-course/)** ← Browse the complete course

> **💡 Note**: Environment setup (Python, API keys, dependencies) is covered in the [Quick Setup](#-quick-setup) section below and in Module 1.

---

## 🎯 How to Use This Course

**For each module:**
1. Read the `README.md` (objectives & setup)
2. Open the `.ipynb` notebook
3. Run cells top to bottom
4. Complete exercises
5. Move to next module

Track your progress with the Skills Checklist in each notebook.

---

## ⚡ Quick Setup

**Prerequisites**:
- Python 3.8+
- IDE with notebook support (VS Code or Cursor)
- API access (GitHub Copilot/CircuIT/OpenAI)
- **Splunk users only**: `okta-artifactory-login` configured (required for pip dependencies)

> **💡 Python Version Note**: This course has been tested with Python 3.14. If you encounter installation issues with newer Python versions, try Python 3.11 or 3.12.

> **⚠️ Important - API Access**: OpenAI access via Cisco does **not** provide API access. You must use your **personal OpenAI or Claude API keys** with an email address **other than Cisco/Splunk** to complete the course exercises.

> **💡 Shell Note**: Setup commands are written for bash/zsh. Fish shell users: use `source .venv/bin/activate.fish` instead of `source .venv/bin/activate`.

> **⚠️ Splunk Users - Artifactory Setup Required**: Run `okta-artifactory-login -t pypi` **before** the setup steps below. Without this, pip install will fail. See [Artifactory PyPI setup guide](https://cloud-automation.splunkdev.page/ci-cd/artifactory/ephemeral-credentials-examples/user-guide/pypi/) for installation instructions.

```bash
# 1. Clone the repository
git clone git@cd.splunkdev.com:eng-enablement/prompteng-devs.git
cd prompteng-devs

# 2. Install dependencies
# Recommended: Using uv (faster, modern Python tooling)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv --seed
source .venv/bin/activate
uv pip install ipykernel

# Alternative: Traditional venv (if uv unavailable)
# python3 -m venv .venv
# source .venv/bin/activate
# pip install ipykernel

# 3. Configure environment
cp .env-example .env
# Edit .env with your API keys, provider, and AI model to use
```


### 🔧 Advanced Configuration

You can customize the AI provider and models using environment variables in your `.env` file:

**Provider Selection:**
```bash
# Module 2
MODULE2_PROVIDER=claude          # Options: openai, claude, circuit

# Module 3
MODULE3_PROVIDER=claude          # Options: openai, claude, circuit
```

**Model Override:**
```bash
# Module 2
MODULE2_OPENAI_MODEL=gpt-5       # For OpenAI/GitHub Copilot
MODULE2_CLAUDE_MODEL=claude-sonnet-4
MODULE2_CIRCUIT_MODEL=gpt-4.1    # Default free tier (also: gpt-4o-mini, or gpt-4o with paid access)

# Module 3
MODULE3_OPENAI_MODEL=gpt-5
MODULE3_CLAUDE_MODEL=claude-sonnet-4
MODULE3_CIRCUIT_MODEL=gpt-4.1    # Default free tier (also: gpt-4o-mini, or gpt-4o with paid access)
```

**Proxy Configuration (for GitHub Copilot):**
```bash
MODULE2_OPENAI_BASE_URL=http://localhost:7711/v1
MODULE2_CLAUDE_BASE_URL=http://localhost:7711
MODULE2_PROXY_API_KEY=dummy-key
```

---

## 📓 About Jupyter Notebooks

> **🆕 First time using Jupyter notebooks?** Read this section before starting the modules.

All course modules use **Jupyter notebooks** (`.ipynb` files) - interactive documents that let you run code directly in your IDE.

### ⚠️ Important Requirements

> **⚠️ Important**: You must clone this repository and run notebooks locally. They cannot be executed directly from GitHub/GitLab.

### 💡 How Notebooks Work

- **Code cells** contain Python code that runs on your local machine
- **Click the ▶️ button** (or press `Shift + Enter`) to execute a cell
- **Output appears** below each cell after you run it
- **To edit cells**: Double-click to edit, make changes (like uncommenting code), then press `Shift + Enter` to run
- **Installation commands** run locally and install packages to your Python environment
- **You don't copy/paste** - just click the run button in each cell
- **Long outputs are truncated**: If you see "Output is truncated. View as a scrollable element" - click that link to see the full response

### 🔒 Where Code Executes

All code runs on your local machine. When you:
- Install packages → They're installed to your Python environment
- Connect to AI services → Your computer sends requests over the internet to those services
- Run API calls → They execute from your machine using your credentials

### 🚀 Getting Started with Notebooks

1. **Open the `.ipynb` file** in your IDE (VS Code or Cursor recommended)
2. **Select the Python kernel**: Choose your `.venv` interpreter when prompted
3. **Run cells sequentially** from top to bottom
4. **Complete exercises** as you go through the modules
5. **Experiment**: Add new cells to try your own code

---

## 📊 Automated Evaluation

Get instant feedback on your prompts with scoring and skill tracking.

### How It Works

1. Complete practice activities
2. Run `evaluate_prompt()` for your score (0-100)
3. Score ≥ 80 unlocks skills
4. Track progress with `view_progress()`

**Scoring:**
- 40% structure (pattern detection)
- 60% quality (AI assessment)
- Pass: 80+

**Example:**
```python
messages = [...]
evaluate_prompt(messages, "Activity 2.1", ["Role Prompting", "XML Tags"])
# Score: 91/100 ✅ Skills unlocked: #1, #2, #3, #4
```

---

## 📚 Learning Path

### 1. **Interactive Course** - Learn the fundamentals
- **[Module 1: Foundations](./01-course/module-01-foundations/)** - Interactive notebook (`.ipynb`) with environment setup & prompt anatomy (20 min)
- **[Module 2: Core Prompting Techniques](./01-course/module-02-fundamentals/)** - Master six essential prompt engineering techniques through hands-on practice and real coding scenarios. Learn clear instructions (foundation), role prompting, structured inputs with XML tags, few-shot examples, chain-of-thought reasoning, reference citations, and prompt chaining including parallel exploration patterns (90-120 min)  
- **[Module 3: Applications](./01-course/module-03-applications/)** ⭐ **Optional** - Interactive notebook (`.ipynb`) with reusable prompt templates for code review, debugging, refactoring, and SDLC workflows (60 min)

### 2. **Practice** - Reinforce learning
- **Hands-on Exercises** - Integrated into each module to reinforce concepts
- **Self-Assessment** - Use the Skills Checklist in each module to track your progress


## 🎯 What You'll Build

- ✅ **Working Development Environment** with AI assistant integration
- ✅ **Prompt Engineering Toolkit** with reusable patterns and commands  
- ✅ **Production-Ready Workflows** for code quality, debugging, and API integration

**Total Time**: ~300 minutes (~4-5 hours)

---

## 📁 Project Structure

```
prompteng-devs/
├── 01-course/                    # Learning modules
└── GitHub-Copilot-2-API/         # Copilot setup
```

**New to notebooks?** See [About Jupyter Notebooks](#-about-jupyter-notebooks) section above.

---

## 🤝 Contributing

Issues and pull requests welcome! Ensure examples are minimal, reproducible, and well-documented.
