# Prompt Engineering for Developers

Master prompting techniques for software development with structured tutorials, hands-on exercises, and real-world examples.

## 🚀 Get Started

**1. Clone the repository:**
```bash
git clone https://cd.splunkdev.com/eng-enablement/prompteng-devs.git
cd prompteng-devs
```

**2. Begin learning:**
- **[Start Module 1: Foundations](./01-course/module-01-foundations/)** ← Read README.md, then open the `.ipynb` notebook
- **[View All Modules](./01-course/)** ← Browse the complete course
- **[Implementation Examples](./02-implementation-examples/)** ← Production patterns

---

## 🎯 Recommended Learning Workflow

> **📚 For Each Module:**

#### **Step 1: 📖 Read the Module**
- Open the module's `README.md` file to understand learning objectives and prerequisites

#### **Step 2: 🚀 Launch the Notebook** 
- Open the `.ipynb` notebook file to begin the interactive tutorial

#### **Step 3: 💻 Complete All Cells**
- Run through each cell sequentially from top to bottom

#### **Step 4: 🏃‍♀️ Practice Exercises**
- Complete the hands-on exercises to reinforce learning

#### **Step 5: 📊 Self-Assess**
- Use the Skills Checklist in the notebook to track your progress

#### **Step 6: ➡️ Next Module**
- Move to the next module and repeat the process

**📈 Track Progress**: Use the Skills Checklist in each notebook to mark skills as you master them
**🚀 Apply Skills**: Use real-world examples after completing all modules

💡 **Tip**: Each module directory contains a `README.md` file explaining what you'll learn and how to get started.

---

## ⚡ Quick Setup

**Prerequisites**: Python 3.8+, IDE with notebook support, API access (GitHub Copilot/CircuIT/OpenAI)

> **⚠️ Important - API Access**: OpenAI access via Cisco does **not** provide API access. You must use your **personal OpenAI or Claude API keys** with an email address **other than Cisco/Splunk** to complete the course exercises.

```bash
# 1. Clone the repository
git clone https://cd.splunkdev.com/eng-enablement/prompteng-devs.git
cd prompteng-devs

# 2. Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install ipykernel

# Alternative: Using uv (faster)
# curl -LsSf https://astral.sh/uv/install.sh | sh
# uv venv .venv --seed
# source .venv/bin/activate
# uv pip install ipykernel

# 3. Configure environment
cp .env-example .env
# Edit .env with your API keys
```

**Splunk users**: Run `okta-artifactory-login -t pypi` before installing dependencies. See [Artifactory PyPI setup guide](https://cloud-automation.splunkdev.page/ci-cd/artifactory/ephemeral-credentials-examples/user-guide/pypi/) for installation instructions and access to Splunk's internal PyPI packages.

---

## 📓 About Jupyter Notebooks

> **🆕 First time using Jupyter notebooks?** Read this section before starting the modules.

All course modules use **Jupyter notebooks** (`.ipynb` files) - interactive documents that let you run code directly in your IDE.

### ⚠️ Important Requirements

<div style="padding:12px; background:#fee2e2; border-left:4px solid #ef4444; color:#991b1b;">

**You must clone this repository and run notebooks locally.** They cannot be executed directly from GitHub.

</div>

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

## 📊 Tracking Your Progress

Module 2 includes **automated evaluation** that scores your prompts and tracks your skill mastery.

### How It Works

**Write Your Prompt → Get Instant Feedback → Unlock Skills**

1. **Complete practice activities** in the hands-on notebooks
2. **Run `evaluate_prompt()`** to get your score (out of 100)
3. **Score ≥ 80?** You've unlocked the skills for that activity! 🎉
4. **View your progress** anytime with `view_progress()`

### Your Score Breakdown

- **40%** - Structure Check (automated pattern detection)
- **60%** - Quality Assessment (AI evaluates how well you applied tactics)
- **Pass threshold:** 80 or higher

Each tactic also includes a **confidence score** (e.g., 85%) showing how certain the AI is about its feedback. Use this to prioritize which suggestions to trust most.

### Example

```python
# Write your prompt
messages = [...]

# Get evaluated
evaluate_prompt(
    messages=messages,
    activity_name="Activity 2.1",
    expected_tactics=["Role Prompting", "Structured Inputs"]
)

# Score: 91/100 ✅
# Skills unlocked: #1, #2, #3, #4
```

💡 **Tip**: Your scores are saved automatically. You can retry activities to improve your score and watch yourself get better!

---

## 📚 Learning Path

### 1. **Interactive Course** - Learn the fundamentals
- **[Module 1: Foundations](./01-course/module-01-foundations/)** - Interactive notebook (`.ipynb`) with environment setup & prompt anatomy (20 min)
- **[Module 2: Core Techniques](./01-course/module-02-fundamentals/)** - Interactive notebooks (`.ipynb`) covering role prompting, structured inputs, few-shot examples, chain-of-thought reasoning, reference citations, prompt chaining, and evaluation techniques (90-120 min)  
- **[Module 3: Applications](./01-course/module-03-applications/)** - Interactive notebook (`.ipynb`) with reusable prompt templates for code review, debugging, refactoring, and SDLC workflows (60 min)
- **[Module 4: Integration](./01-course/module-04-integration/)** - Interactive notebook (`.ipynb`) with custom commands & AI assistants (30 min)

### 2. **Practice** - Reinforce learning
- **Hands-on Exercises** - Integrated into each module to reinforce concepts
- **Self-Assessment** - Use the Skills Checklist in each module to track your progress

### 3. **Apply** - Real-world patterns
- **[Code Quality](./02-implementation-examples/code-quality/)** - Refactoring & modernization
- **[Debugging](./02-implementation-examples/debugging/)** - Incident investigation & resolution
- **[API Integration](./02-implementation-examples/api-integration/)** - Client generation & error handling
- **[Custom Commands](./02-implementation-examples/custom-commands/)** - Reusable templates


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
├── 02-implementation-examples/   # Real-world patterns
└── GitHub-Copilot-2-API/         # Copilot setup
```

**New to notebooks?** See [About Jupyter Notebooks](#-about-jupyter-notebooks) section above.

---

## 🤝 Contributing

Issues and pull requests welcome! Ensure examples are minimal, reproducible, and well-documented.
