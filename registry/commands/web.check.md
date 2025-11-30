---
description: Verify Claude Code web configuration and test hook scripts
category: development-setup
allowed-tools: Bash, Read
---

# Claude Command: Web Check

Verify that this repository is properly configured for Claude Code on the web.

## Instructions

### Step 1: Check Configuration Files

Verify `.claude/settings.json` exists and is valid:

```bash
if [ -f ".claude/settings.json" ]; then
    echo "✓ .claude/settings.json exists"
    cat .claude/settings.json
else
    echo "✗ .claude/settings.json not found"
    echo "  Run /web.setup to create it"
fi
```

Validate JSON:

```bash
python3 -c "import json; json.load(open('.claude/settings.json'))" 2>/dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
```

### Step 2: Check Hook Configuration

Verify SessionStart hooks are configured:

```bash
python3 -c "
import json
with open('.claude/settings.json') as f:
    config = json.load(f)
    hooks = config.get('hooks', {}).get('SessionStart', [])
    if hooks:
        print('✓ SessionStart hooks configured')
        for h in hooks:
            for hook in h.get('hooks', []):
                print(f'  - Command: {hook.get(\"command\")}')
                print(f'    Timeout: {hook.get(\"timeout\", 60)}s')
    else:
        print('✗ No SessionStart hooks found')
"
```

### Step 3: Check Setup Script

Verify the setup script exists and is executable:

```bash
SCRIPT=$(python3 -c "
import json
with open('.claude/settings.json') as f:
    config = json.load(f)
    hooks = config.get('hooks', {}).get('SessionStart', [])
    if hooks:
        for h in hooks:
            for hook in h.get('hooks', []):
                cmd = hook.get('command', '')
                if cmd.startswith('./'):
                    print(cmd[2:])
                    break
")

if [ -n "$SCRIPT" ]; then
    if [ -f "$SCRIPT" ]; then
        echo "✓ Script exists: $SCRIPT"
        if [ -x "$SCRIPT" ]; then
            echo "✓ Script is executable"
        else
            echo "✗ Script is not executable"
            echo "  Fix: chmod +x $SCRIPT"
        fi
    else
        echo "✗ Script not found: $SCRIPT"
        echo "  Run /web.setup to create it"
    fi
fi
```

### Step 4: Verify Script Content

Check script has proper structure:

```bash
SCRIPT="scripts/claude-setup.sh"
if [ -f "$SCRIPT" ]; then
    echo ""
    echo "Script analysis:"

    # Check shebang
    if head -1 "$SCRIPT" | grep -q "^#!/bin/bash"; then
        echo "✓ Has bash shebang"
    else
        echo "✗ Missing or incorrect shebang (should be #!/bin/bash)"
    fi

    # Check exit 0
    if grep -q "exit 0" "$SCRIPT"; then
        echo "✓ Has exit 0"
    else
        echo "⚠ Missing 'exit 0' at end (recommended for clarity)"
    fi

    # Check set -e
    if grep -q "set -e" "$SCRIPT"; then
        echo "✓ Has 'set -e' (fail on errors)"
    else
        echo "⚠ Consider adding 'set -e' for fail-fast behavior"
    fi

    # Check for common dependency managers
    echo ""
    echo "Detected setup commands:"
    grep -E "(npm install|pnpm install|yarn install|bun install|pip install|uv sync|poetry install|bundle install|go mod)" "$SCRIPT" 2>/dev/null || echo "  No standard package manager commands found"
fi
```

### Step 5: Check Environment Variable Usage

Verify proper use of environment file:

```bash
SCRIPT="scripts/claude-setup.sh"
if [ -f "$SCRIPT" ]; then
    echo ""
    if grep -q 'CLAUDE_ENV_FILE' "$SCRIPT"; then
        echo "✓ Uses \$CLAUDE_ENV_FILE for environment variables"
        echo "  Variables being set:"
        grep 'CLAUDE_ENV_FILE' "$SCRIPT" | sed 's/.*echo "/  /' | sed 's/" >>.*//'
    else
        echo "ℹ No environment variables being persisted"
        echo "  (Optional: use echo \"VAR=value\" >> \"\$CLAUDE_ENV_FILE\")"
    fi
fi
```

### Step 6: Check for Common Issues

```bash
echo ""
echo "Common issues check:"

# Check for .env files that might be needed
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    echo "⚠ .env.example exists but .env doesn't"
    echo "  Consider copying in your setup script"
fi

# Check for lock files
echo ""
echo "Detected project type:"
if [ -f "package.json" ] && [ -f "requirements.txt" ]; then
    echo "  Full-stack (Node.js + Python)"
elif [ -f "package.json" ]; then
    echo "  Node.js"
    if [ -f "pnpm-lock.yaml" ]; then echo "  Package manager: pnpm"; fi
    if [ -f "yarn.lock" ]; then echo "  Package manager: yarn"; fi
    if [ -f "bun.lockb" ]; then echo "  Package manager: bun"; fi
    if [ -f "package-lock.json" ]; then echo "  Package manager: npm"; fi
elif [ -f "pyproject.toml" ]; then
    echo "  Python (pyproject.toml)"
elif [ -f "requirements.txt" ]; then
    echo "  Python (requirements.txt)"
elif [ -f "Gemfile" ]; then
    echo "  Ruby"
elif [ -f "go.mod" ]; then
    echo "  Go"
else
    echo "  Unknown (customize setup script manually)"
fi
```

### Step 7: Summary

Display overall status:

```
╭─────────────────── Web Configuration Status ───────────────────╮
│                                                                 │
│ Configuration: ✓ / ✗                                           │
│ Setup Script:  ✓ / ✗                                           │
│ Executable:    ✓ / ✗                                           │
│                                                                 │
│ Ready for Claude Code on the web: YES / NO                     │
│                                                                 │
│ If not ready, run: /web.setup                                  │
╰─────────────────────────────────────────────────────────────────╯
```

## Notes

- This command only checks configuration, it does not modify files
- Run `/web.setup` to create or fix configuration
- Test locally with `bash scripts/claude-setup.sh` (set `CLAUDE_ENV_FILE` first)
