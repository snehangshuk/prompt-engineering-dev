# Module 1: Foundation - Prompt Templates

> **📋 For Circuit Users (No API Access Required)**
>
> This guide extracts the key prompts from `module1.ipynb` into copy-paste templates for use in web-based AI chat interfaces like Cisco's internal Circuit.

| **Aspect** | **Details** |
|-------------|-------------|
| **Goal** | Learn the 4 core elements of effective prompts and apply them to real coding scenarios |
| **Time** | ~20 minutes |
| **Prerequisites** | Access to AI chat web interface (internal Cisco Circuit, ChatGPT Plus, etc.) |
| **Next Steps** | Continue to Module 2: Core Prompt Engineering Techniques |

---

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- ✅ Understand why prompt engineering matters for software engineers
- ✅ Identify the 4 core elements of effective prompts
- ✅ Create complete prompts with Instructions, Context, Input Data, and Output Format
- ✅ Apply prompt engineering to code review scenarios
- ✅ Analyze incomplete prompts to identify missing elements

---

## 🤔 Why Prompt Engineering for Software Engineers?

### What is Prompt Engineering?

**Prompt Engineering** is the fastest way to harness the power of large language models. By interacting with an LLM through well-structured questions, statements, or instructions, you can dramatically improve output quality based on the specific context you provide.

### Two Ways to Influence LLM Behavior

**1. Fine-tuning (Traditional Approach)**
- Adjust model weights/parameters using training data
- **Expensive** - requires significant computation time and cost
- **Limited flexibility** - model locked into specific behavior patterns
- **Problem:** Still produces vague results without proper context

**2. Prompt Engineering (Modern Approach)**
- Write better instructions and provide better context
- **Fast** - immediate results, no training needed
- **Flexible** - adapt on-the-fly for different tasks
- **Effective:** Proper prompts transform generic AI into specialized experts

### The Impact of Context

| **Without Context** | **With Context** |
|---------------------|------------------|
| ❌ "Fix this code" → AI asks clarifying questions | ✅ "Fix this code: [code]. Context: Python e-commerce function. Requirements: Add type hints, handle edge cases, maintain backward compatibility" → AI provides specific fixes |
| ❌ "Make it better" → Generic suggestions | ✅ "Improve this security function for critical system. Check for: SQL injection, XSS, authentication bypass. Provide specific fixes." → Targeted security improvements |
| ❌ "Help me debug" → AI needs more information | ✅ "Debug this error: [error message]. Context: Production system, 10K users. Expected: [behavior]. Use step-by-step troubleshooting." → Systematic debugging |

**The difference:** Context transforms AI from a "helpful chatbot" into a reliable development partner.

---

## 📋 The 4 Core Elements of Effective Prompts

Every effective prompt contains some or all of these elements:

### **1. Instructions**
The task or role you want the AI to perform.

**Example:** "You are a senior software engineer conducting a code review. Analyze the provided code and identify potential issues."

### **2. Context**
External information to guide the model.

**Example:** "Code context: This is a utility function for user registration in a web application."

### **3. Input Data**
The specific content you want analyzed or transformed.

**Example:** "Code to review: `def register_user(email, password): ...`"

### **4. Output Format**
The structure or format you want for the response.

**Example:** "Please provide your response in this format: 1) Security Issues, 2) Code Quality Issues, 3) Recommended Improvements, 4) Overall Assessment"

---

## 📝 Example: Complete Code Review Prompt

Let's see all 4 elements working together in a software engineering scenario.

**Copy this to Circuit:**

```
SYSTEM INSTRUCTIONS:
You are a senior software engineer conducting a code review. Analyze the provided code and identify potential issues.

USER REQUEST:
Context: This is a utility function for user registration in a web application.

Code to review:
```python
def register_user(email, password):
    if email and password:
        user = {"email": email, "password": password}
        return user
    return None
```

Output Format:
Please provide your response in this format:
1. Security Issues (if any)
2. Code Quality Issues (if any)
3. Recommended Improvements
4. Overall Assessment
```

**✅ Self-Check: Your response should include:**
- [ ] Identified security issues (plaintext password storage, no validation)
- [ ] Code quality issues (no error handling, weak validation)
- [ ] Specific improvements (password hashing, email validation, error messages)
- [ ] Overall assessment (needs significant security improvements)

**💡 Key Insight:** Notice how all 4 elements work together to produce a thorough, structured code review!

---

## 🎯 Activity 1: Analyze Incomplete Prompts

**Goal:** Identify which of the 4 core elements are missing from incomplete prompts.

### Prompt 1 - What's Missing?

**Copy this to Circuit:**

```
Fix this code:
def calculate(x, y):
    return x + y
```

**Your Task:** Before looking at the answer below, identify which elements are present and which are missing.

<details>
<summary><strong>📋 Click to reveal analysis</strong></summary>

**Missing elements:**
- ❌ **Instructions/Role** - No clear task or role definition (fix what? improve how?)
- ❌ **Context** - What is this function supposed to do? What's wrong with it?
- ❌ **Output Format** - No specification for how the fixed code should be presented
- ✅ **Input Data** - Has the code

**Why this matters:** Without context and clear instructions, AI might:
- Add unnecessary complexity
- Misunderstand the function's purpose
- Provide fixes that don't match your needs

</details>

---

### Prompt 2 - What's Missing?

**Copy this to Circuit:**

```
You are a Python developer.
Make this function better.
```

**Your Task:** Identify the missing elements.

<details>
<summary><strong>📋 Click to reveal analysis</strong></summary>

**Missing elements:**
- ✅ **Instructions/Role** - Has a role ("Python developer")
- ❌ **Context** - What function? What makes it need improvement?
- ❌ **Input Data** - No function provided
- ❌ **Output Format** - "Better" is vague (better performance? readability? security?)

**Why this matters:** The AI has no concrete input to work with and no definition of "better"!

</details>

---

### Prompt 3 - What's Missing?

**Copy this to Circuit:**

```
Review the following function and provide feedback.
Return your response as a list of improvements.
```

**Your Task:** Identify the missing elements.

<details>
<summary><strong>📋 Click to reveal analysis</strong></summary>

**Missing elements:**
- ❌ **Instructions/Role** - No clear role definition (code reviewer? security expert? performance specialist?)
- ❌ **Context** - What's the function's purpose? What domain?
- ❌ **Input Data** - Says "following function" but none is provided
- ✅ **Output Format** - Has format ("list of improvements")

**Why this matters:** Without the function and context, AI can't provide meaningful feedback!

</details>

---

## 🎯 Activity 2: Build a Complete Prompt

**Goal:** Create a complete prompt with all 4 elements to generate documentation.

### The Function to Document

```python
def process_transaction(user_id, amount, transaction_type):
    if transaction_type not in ['deposit', 'withdrawal']:
        raise ValueError("Invalid transaction type")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    balance = get_user_balance(user_id)

    if transaction_type == 'withdrawal' and balance < amount:
        raise InsufficientFundsError("Insufficient funds")

    new_balance = balance + amount if transaction_type == 'deposit' else balance - amount
    update_user_balance(user_id, new_balance)
    log_transaction(user_id, amount, transaction_type)

    return new_balance
```

### Your Task

Before looking at the solution, try writing a complete prompt that includes:
1. **Instructions** - Define the AI's role and task
2. **Context** - Explain what this function does and where it's used
3. **Input Data** - Include the function code
4. **Output Format** - Specify the documentation structure you want

**Try writing it yourself, then check the solution below!**

---

### Solution: Complete Documentation Prompt

**Copy this to Circuit:**

```
SYSTEM INSTRUCTIONS:
You are a senior software engineer creating technical documentation. Write clear, comprehensive documentation for Python functions.

USER REQUEST:
Context: This is a financial transaction processing function for a banking application. It handles deposits and withdrawals with validation and error handling.

Function to document:
```python
def process_transaction(user_id, amount, transaction_type):
    if transaction_type not in ['deposit', 'withdrawal']:
        raise ValueError("Invalid transaction type")

    if amount <= 0:
        raise ValueError("Amount must be positive")

    balance = get_user_balance(user_id)

    if transaction_type == 'withdrawal' and balance < amount:
        raise InsufficientFundsError("Insufficient funds")

    new_balance = balance + amount if transaction_type == 'deposit' else balance - amount
    update_user_balance(user_id, new_balance)
    log_transaction(user_id, amount, transaction_type)

    return new_balance
```

Output Format:
Please provide documentation in this format:
1. Function Purpose
2. Parameters (name, type, description for each)
3. Return Value
4. Exceptions/Error Conditions
5. Usage Example
```

**✅ Self-Check: Your response should include:**
- [ ] Clear function purpose (processes financial transactions)
- [ ] All 3 parameters documented (user_id, amount, transaction_type)
- [ ] Return value explained (new_balance after transaction)
- [ ] All exceptions listed (ValueError for invalid input, InsufficientFundsError)
- [ ] Usage example showing how to call the function

**💡 Why This Works:**
- ✅ **Instructions** - "senior software engineer creating technical documentation"
- ✅ **Context** - "financial transaction processing function for a banking application"
- ✅ **Input Data** - The complete function code
- ✅ **Output Format** - Numbered list with specific sections

---

## 🎯 Activity 3: Practice with Your Own Code

**Try this on your own!**

Think of a function from your current project and create a complete prompt to:
- Get a code review
- Generate documentation
- Improve error handling
- Add type hints
- Or any other task you need

**Template to use:**

```
SYSTEM INSTRUCTIONS:
You are a [ROLE]. [TASK DESCRIPTION].

USER REQUEST:
Context: [Where this code is used, what it does, any constraints]

Code to analyze:
```[language]
[YOUR CODE HERE]
```

Output Format:
Please provide:
1. [First section you want]
2. [Second section you want]
3. [Third section you want]
```

---

## 🎖️ Skill Tracker

After completing all activities, check off the skills you've mastered:

### Understanding Prompt Engineering
- [ ] **Skill #1:** I understand why prompt engineering matters for software engineers
- [ ] **Skill #2:** I can explain the difference between fine-tuning and prompt engineering
- [ ] **Skill #3:** I know when to use prompt engineering vs. other approaches

### The 4 Core Elements
- [ ] **Skill #4:** I can identify the Instructions element in a prompt
- [ ] **Skill #5:** I can identify the Context element in a prompt
- [ ] **Skill #6:** I can identify the Input Data element in a prompt
- [ ] **Skill #7:** I can identify the Output Format element in a prompt

### Building Complete Prompts
- [ ] **Skill #8:** I can analyze incomplete prompts to find missing elements
- [ ] **Skill #9:** I can create complete prompts with all 4 elements
- [ ] **Skill #10:** I can apply prompt engineering to real code review scenarios

**🏆 Mastery Level:**
- **10/10 skills** = Expert! Ready for Module 2 ✅
- **7-9/10 skills** = Proficient! Review 1-2 concepts
- **4-6/10 skills** = Good progress! Revisit examples above
- **0-3/10 skills** = Keep practicing! Try each activity again

---

## 💡 Key Takeaways

### The 4-Element Framework

Every effective prompt should include:

| Element | Purpose | Example |
|---------|---------|---------|
| **1. Instructions** | Define role and task | "You are a senior engineer conducting code review" |
| **2. Context** | Provide background | "This is a user registration function for a web app" |
| **3. Input Data** | Give specific content | The actual code to review |
| **4. Output Format** | Specify structure | "1) Security Issues, 2) Code Quality, 3) Improvements" |

### Before vs. After

| Vague ❌ | Complete ✅ |
|----------|-------------|
| "Review my code" | "You are a security expert. Review this authentication function for SQL injection and XSS vulnerabilities. Provide: 1) Vulnerabilities found, 2) Severity ratings, 3) Fix recommendations." |
| "Help with Docker" | "You are a DevOps engineer. Create a Dockerfile for a Node.js 18 Express app that runs on port 3000 and uses environment variables from .env file. Format: Production-ready Dockerfile with comments." |
| "Explain microservices" | "You are a software architect. Explain when to choose microservices over monolithic architecture for a team of 8 developers building a SaaS product with 5 main features. Include: pros, cons, and recommendation." |

### Quick Tips for Better Prompts

1. **Be specific** - "10,000 users" vs "many users"
2. **Name technologies** - "PostgreSQL" vs "a database"
3. **State constraints** - "Cannot change schema" vs assuming flexibility
4. **Specify format** - "Bullet points" vs letting AI choose
5. **Provide context** - "For a startup with 5 developers" vs generic advice

---

## 🎓 Module 1 Complete!

**Congratulations!** You've completed the foundation module and learned:

✅ **Why prompt engineering matters** - Transform AI from chatbot to development partner
✅ **The 4 core elements** - Instructions, Context, Input Data, Output Format
✅ **How to analyze prompts** - Identify missing elements
✅ **How to build complete prompts** - Apply all 4 elements to real scenarios
✅ **Hands-on practice** - Code review, documentation, analysis

### What Makes Effective Prompts Work?

- **Clear role definition** guides the AI's perspective and expertise
- **Specific context** provides domain knowledge the AI needs
- **Concrete input** gives the AI something tangible to work with
- **Structured output format** ensures consistent, actionable results

---

## ⏭️ Next Steps

<div style="background:rgb(12, 88, 160); padding: 16px; border-radius: 8px; border-left: 4px solid #3b82f6;">

**Continue to Module 2: Core Prompt Engineering Techniques**

Master 8 powerful tactics used by professional developers:
- 🎭 **Role prompting** - Transform AI into specialized experts
- 📋 **Structured inputs** - Organize complex scenarios with XML
- 📚 **Few-shot examples** - Teach AI your coding style
- ⛓️ **Chain-of-thought** - Systematic debugging and analysis
- 📖 **Reference citations** - Ground responses in documentation
- 🔗 **Prompt chaining** - Break complex tasks into steps
- 🌳 **Tree of thoughts** - Explore multiple solution approaches
- ⚖️ **LLM-as-judge** - Automated evaluation and self-correction

[View Module 2 README](../module-02-fundamentals/README.md) →

</div>

---

## 🤔 Troubleshooting

**Q: My prompts still get generic responses**
**A:** Check that you've included all 4 elements:
1. Instructions - Clear role and task
2. Context - Domain and purpose
3. Input Data - Specific code or content
4. Output Format - Structured response specification

**Q: How specific should the context be?**
**A:** Include:
- What the code does
- Where it's used (production, internal tool, public API)
- Scale/constraints (10K users, cannot change schema)
- Any relevant business logic or domain knowledge

**Q: What if I don't need all 4 elements?**
**A:** Start with all 4, then remove what's unnecessary. Usually:
- Instructions are ALWAYS needed
- Context is ALMOST ALWAYS needed
- Input Data is ALWAYS needed (unless asking general questions)
- Output Format is HIGHLY RECOMMENDED for consistency

**Q: Can I use this with Cisco's internal Circuit?**
**A:** Yes! All these prompts work with any AI chat interface. Just copy-paste the text between the code blocks.

---

## 📚 Related Resources

- [Claude Documentation - Prompt Engineering Guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI Prompt Engineering Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic's Context Engineering Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Full Interactive Notebook](./module1.ipynb) (requires API access)

---

**📝 Note:** This template guide is a companion to the full Jupyter notebook. If you have API access (GitHub Copilot, OpenAI, Claude), use the interactive notebook for automated evaluation and progress tracking.

**🎉 Great work! You're ready to dive deeper into advanced prompt engineering techniques in Module 2.**
