## Activities Design Guide

This guide outlines the learner-facing activities for each module, with clear objectives, tasks, deliverables, and assessment criteria. Use this as a blueprint to design, facilitate, and evaluate learning. Hands-on execution lives in the activities notebook; reference solutions live in the solutions notebook.

- Activities notebook: `course-activities.ipynb`
- Solutions notebook: `course-activities-solutions.ipynb`

---

## How to Use This Guide

- Align each activity with its objective before learners begin.
- Provide only the hints in `course-activities.ipynb`; keep full solutions in `course-activities-solutions.ipynb`.
- Encourage learners to write prompts themselves, compare against solutions, and reflect on differences.
- Assess using the provided “Assessment Criteria” checklists.

---

## Module 1: Course Introduction

### Activity 1.1: Environment Setup — Email Improvement
- Objective: Verify setup and practice a minimal prompt workflow.
- Learner Tasks:
  - Create messages with a system persona for writing assistance.
  - Request: tone assessment, three improvement suggestions, and a revised email.
  - Call the chat completion and inspect output.
- Deliverables:
  - A prompt that produces a structured response with the three sections.
- Assessment Criteria:
  - Output contains all requested parts and matches the intended format.
  - API connection works without errors.

### Activity 1.1 Task 3: Improve a Code Comment
- Objective: Practice targeting technical documentation improvements via prompts.
- Learner Tasks:
  - Set a documentation persona in the system message.
  - Provide context, the existing comment, and ask for assessment, three suggestions, and a revised comment.
  - Execute and review changes.
- Deliverables:
  - A revised, high-quality code comment and rationale.
- Assessment Criteria:
  - Suggestions are specific and actionable; revised comment is clear and accurate.

### Activity 1.2: Prompt Structure Analysis
- Objective: Identify the four core elements (instructions, context, input data, output indicator).
- Learner Tasks:
  - For three sample prompts, mark which elements are present and which are missing.
- Deliverables:
  - Notes identifying missing elements per prompt.
- Assessment Criteria:
  - Each of the four elements is correctly identified across all prompts.

### Activity 1.2: Create a Complete 4-Element Prompt (Code Documentation)
- Objective: Compose a complete prompt using all four elements.
- Learner Tasks:
  - Define an expert documentation persona (system message).
  - Provide context, input code, and exact output requirements (user message).
  - Execute and evaluate the response quality.
- Deliverables:
  - A full prompt and a generated docstring with requested sections.
- Assessment Criteria:
  - Output adheres to format, covers Args/Returns/Raises, and includes a usable example.

---

## Module 2: Prompting Fundamentals

### Activity 2.1: Convert Vague to Specific
- Objective: Transform a vague request into a specific, testable prompt.
- Learner Tasks:
  - Draft a detailed prompt specifying constraints, edge cases, types, and output format.
  - Optionally compare the vague vs specific outputs.
- Deliverables:
  - A “specific” prompt string and optional comparison outputs.
- Assessment Criteria:
  - Specific prompt yields higher-quality, more deterministic results.

### Activity 2.2: Persona Adoption Workshop
- Objective: Apply multiple engineering personas to the same code and compare insights.
- Learner Tasks:
  - Create message sets for Security Engineer, Performance Engineer, and QA Engineer.
  - Run all three, then summarize differences.
- Deliverables:
  - Three reviews and a brief comparison summary.
- Assessment Criteria:
  - Each persona produces distinct, relevant findings aligned with its focus area.

### Activity 2.3: Delimiter Mastery — Multi-File Refactoring
- Objective: Organize complex inputs using headers and XML-like tags.
- Learner Tasks:
  - Compose a user message combining requirements, original code (multiple files), and target architecture.
  - Provide a system message establishing an architecture refactoring role.
- Deliverables:
  - Structured input with clear sections and a refactoring response.
- Assessment Criteria:
  - Response addresses all requirements and demonstrates separation of concerns.

### Activity 2.4: Step-by-Step Reasoning — Systematic Code Review
- Objective: Guide the model through explicit steps to analyze code thoroughly.
- Learner Tasks:
  - Draft a system message listing ordered review steps.
  - Embed code in the user message and request prioritized recommendations.
- Deliverables:
  - A reasoned review with stepwise findings and prioritized fixes.
- Assessment Criteria:
  - Output follows the steps and provides actionable, prioritized improvements.

---

## Module 3: Software Engineering Applications

### Activity 3.1: Code Refactoring Project
- Objective: Apply fundamentals to modernize legacy code.
- Learner Tasks:
  - Write comprehensive refactoring requirements and success criteria.
  - Use delimiter strategies for organizing input vs output.
  - Use personas for architecture review; generate tests for the refactor.
- Deliverables:
  - Refactoring plan, refactored code, and a basic test suite.
- Assessment Criteria:
  - Requirements are met; architecture and code quality are improved; tests pass.

### Activity 3.2: Production Debugging Simulation
- Objective: Use prompt engineering to investigate and solve a critical incident.
- Learner Tasks:
  - Create prompts for root cause analysis; chain queries as needed.
  - Produce inner-monologue guided technical notes and an executive summary.
- Deliverables:
  - Investigation log, root cause, proposed fix, and executive summary.
- Assessment Criteria:
  - Root cause is plausible and supported; summary is concise and actionable.

### Activity 3.3: API Integration Workshop
- Objective: Build a production-ready API client from documentation.
- Learner Tasks:
  - Use reference text to derive endpoints, schemas, and error handling.
  - Implement rate limiting and retries; create a test suite.
- Deliverables:
  - API client code, tests, and usage documentation.
- Assessment Criteria:
  - Correct endpoint coverage; robust error handling; tests validate common paths and edge cases.

---

## Module 4: Custom Assistant Integration

### Activity 4.1: Command Creation Challenge
- Objective: Author first custom commands for recurring engineering tasks.
- Learner Tasks:
  - Identify three frequent tasks; create commands with variables and usage examples.
  - Test and iterate based on results.
- Deliverables:
  - Three commands with documentation and example invocations.
- Assessment Criteria:
  - Commands are structured, reusable, and produce consistent results.

### Activity 4.2: Team Implementation Plan
- Objective: Design a rollout plan for team adoption.
- Learner Tasks:
  - Create templates, training materials, quality standards, and a review process.
  - Define success metrics and a realistic timeline.
- Deliverables:
  - Implementation plan, training outline, and success metrics.
- Assessment Criteria:
  - Plan is complete, actionable, and aligned to team needs.

### Activity 4.3: Advanced Command Patterns
- Objective: Design complex, chained command workflows.
- Learner Tasks:
  - Implement a multi-step feature development flow with conditional logic.
  - Document how commands interoperate and build a knowledge base.
- Deliverables:
  - Workflow commands and a brief team-oriented knowledge base.
- Assessment Criteria:
  - Workflow handles complex scenarios; commands integrate cleanly and add value.

---

## Capstone: Final Competency Assessment

### End-to-End Feature Implementation — User Authentication
- Objective: Apply the full toolkit across design, implementation, testing, and rollout.
- Learner Tasks:
  - Architecture design and review; refactor for maintainability; write tests.
  - Perform a security audit, optimize performance, document APIs, and plan deployment.
- Deliverables:
  - Architecture notes, code, tests, audit findings, performance notes, docs, and deployment plan.
- Assessment Criteria:
  - Uses appropriate tactics per phase; creates reusable commands; code and docs are production-ready.


