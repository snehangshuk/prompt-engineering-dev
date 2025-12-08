# Module 2: Core Prompting Techniques

## Core Techniques

This module teaches six essential prompt engineering techniques to get consistent, high-quality results from AI coding assistants.

### Learning Objectives
By completing this module, you will be able to:
- Write clear, specific instructions that eliminate ambiguity (foundation)
- Assign AI specialized roles (security engineer, architect, etc.)
- Organize complex inputs with XML tags
- Train AI on your code style with 3-5 examples (few-shot)
- Force step-by-step analysis (chain-of-thought)
- Prevent hallucinations with document citations
- Chain prompts for multi-step tasks (includes self-improvement patterns)
- Explore multiple alternatives before deciding (parallel exploration)

### Getting Started

**First time here?** 
- If you haven't set up your development environment yet, follow the [Quick Setup guide](../../README.md#-quick-setup) in the main README first
- **New to Jupyter notebooks?** Read [About Jupyter Notebooks](../../README.md#-about-jupyter-notebooks) to understand how notebooks work and where code executes

> **⚠️ Important**: You must clone this repository and run notebooks locally. They cannot be executed directly from GitHub/GitLab.

**Ready to start?**
1. **Open the tutorial notebook**: Click on [2.1-setup-and-foundations.ipynb](./2.1-setup-and-foundations.ipynb) to start
2. **Install dependencies**: Run the "Install Required Dependencies" cell in the notebook
3. **Follow the notebooks**: Work through sections 2.1 → 2.5 in order
4. **Complete exercises**: Practice the hands-on activities as you go

### Module Contents
- **[2.1-setup-and-foundations.ipynb](./2.1-setup-and-foundations.ipynb)** — environment setup, breakpoint workflows, and Tactic 0
- **[2.2-roles-and-structure.ipynb](./2.2-roles-and-structure.ipynb)** — role prompting personas and structured input patterns
- **[2.3-patterns-for-reasoning.ipynb](./2.3-patterns-for-reasoning.ipynb)** — few-shot exemplars, chain-of-thought, and reference citations
- **[2.4-advanced-workflows.ipynb](./2.4-advanced-workflows.ipynb)** — prompt chaining and decision support workflows
- **[2.5-hands-on-practice.ipynb](./2.5-hands-on-practice.ipynb)** — unguided practice with automated evaluation and skill tracking

### Automated Evaluation

Section 2.5 includes AI-powered scoring:

1. Complete practice activity
2. Run `evaluate_prompt()` for instant feedback
3. Score ≥ 80 earns skills

**Evaluates:** Tactic usage, structure, completeness, quality

**Skill Tracking:** Each activity maps to specific skills. Score ≥ 80 to check off:
- **Activity 2.1** → Skills #1-4 (Role Prompting & Structured Inputs)
- **Activity 2.2** → Skills #5-8 (Few-Shot & Chain-of-Thought)
- **Activity 2.3** → Skills #9-12 (Reference Citations & Prompt Chaining)
- **Activity 2.4** → Skills #13-14 (Decision Support)

**Tip:** Don't worry about perfect scores on the first try! Use the feedback to iterate and improve your prompts.

### Time Required
Approximately 90-120 minutes (1.5-2 hours)

**Time Breakdown:**
- Setup and introduction: ~10 minutes
- 6 core tactics with examples: ~65 minutes
- Hands-on practice with evaluation: ~20-30 minutes
- Review and iteration: ~10 minutes

**Tip:** You can complete this module in one session or break it into multiple shorter sessions. Each tactic is self-contained, making it easy to pause and resume.

### Prerequisites
- Python 3.8+ installed
- IDE with notebook support (VS Code or Cursor recommended)
- API access to GitHub Copilot, CircuIT, or OpenAI

### Next Steps
After completing this module:
1. Review and refine your solutions to the exercises in this module
2. **(Optional)** Continue to [Module 3: Applications](../module-03-applications/) for advanced production workflows
