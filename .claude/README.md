# Claude Slash Commands

This directory contains custom slash commands for Claude Code.

## Installation

### Option 1: Project-Specific (Recommended)
Copy the `.claude` directory to your project root:
```bash
cp -r .claude /your/project/root/
```

### Option 2: Global (All Projects)
Copy the command files to your user directory:
```bash
# Create the global commands directory if it doesn't exist
mkdir -p ~/.claude/commands/

# Copy the command files
cp .claude/commands/*.md ~/.claude/commands/
```

## Available Commands

### `/code:review <branch>`
Performs a comprehensive code review of the specified git branch.

**Usage:**
```bash
/code:review feature/my-branch
/code:review bugfix/critical-fix
/code:review refactor/performance
```

**Features:**
- ✅ Auto-fetches latest git changes
- 📊 Analyzes branch metrics and file changes  
- 🔍 Reviews code for security, performance, quality issues
- 🚨 Categorizes findings by priority
- 📋 Generates comprehensive review report

## How It Works

1. Place `.md` files in the `commands/` directory
2. The filename (without extension) becomes the slash command name
3. Commands become available immediately in Claude Code

## File Structure

```
.claude/
├── README.md              # This file
└── commands/
    └── code/
        └── review.md      # Creates the /code:review command
```

## Creating New Commands

To create a new slash command:

1. Create a new `.md` file in the `commands/` directory
2. The filename becomes the command name (e.g., `deploy.md` → `/deploy`)
3. Write your prompt instructions in the file
4. The command becomes available immediately

## Notes

- Commands are automatically available once the files are in place
- No restart or reload required
- Commands work in any project with this directory structure