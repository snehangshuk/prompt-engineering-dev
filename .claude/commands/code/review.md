---
argument-hint: [branch-name]
description: Perform comprehensive code review of a git branch
allowed-tools: Bash(git:*)
---

# Code Review

You are an expert code reviewer. Perform a comprehensive review of the git branch: **$1**

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --porcelain`
- Branch comparison (commits): !`git rev-list --count main..$1 2>/dev/null || git rev-list --count master..$1`
- Files changed: !`git diff --name-status main..$1 2>/dev/null || git diff --name-status master..$1`
- Detailed diff: !`git diff main..$1 2>/dev/null || git diff master..$1`

## Your Task

Analyze the code changes and provide a comprehensive review focusing on:

### Security Issues
- Vulnerabilities, exposed secrets, unsafe operations
- Authentication and authorization flaws
- Input validation and sanitization

### Performance Problems  
- Inefficient algorithms, memory leaks, slow queries
- Resource usage optimization opportunities
- Scalability concerns

### Code Quality
- Code smells, maintainability, readability
- SOLID principles adherence
- Error handling and edge cases

### Best Practices
- Language/framework conventions
- Design patterns implementation
- API design consistency

### Testing
- Test coverage adequacy
- Edge case handling
- Test quality and maintainability

### Documentation
- Missing or outdated comments
- API documentation completeness
- README and setup instructions

## Output Format

Structure your review as follows:

```markdown
# Code Review: $1

## 📊 Branch Overview
- **Commits**: X commits ahead of main/master
- **Files Changed**: X files  
- **Lines**: +X additions, -X deletions

## 🚨 Critical Issues (Must Fix)
[Security vulnerabilities, breaking changes]

## ⚠️ High Priority (Should Fix)  
[Performance issues, logic errors]

## 💡 Medium Priority (Consider Fixing)
[Code quality improvements, refactoring suggestions]

## 📝 Low Priority (Nice to Have)
[Style improvements, documentation enhancements]

## ✅ Positive Feedback
[Well-written code, good practices followed]

## 📋 Summary
[Overall assessment and recommended next steps]
```

## Examples

- `/code:review feature/user-authentication`
- `/code:review bugfix/memory-leak` 
- `/code:review refactor/api-optimization`

Begin by acknowledging the branch name and analyzing the changes.
