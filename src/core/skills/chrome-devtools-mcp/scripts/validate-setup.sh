#!/usr/bin/env bash
# Validate Chrome DevTools MCP setup

set -e

echo "🔍 Chrome DevTools MCP Setup Validator"
echo "========================================"
echo

# Check Node.js version
echo "✓ Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "   Install from: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    echo "❌ Node.js version must be >= 20 (current: $(node --version))"
    echo "   Upgrade from: https://nodejs.org/"
    exit 1
fi
echo "   Node.js $(node --version) ✓"
echo

# Check npm
echo "✓ Checking npm..."
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi
echo "   npm $(npm --version) ✓"
echo

# Check Chrome installation
echo "✓ Checking Chrome installation..."
CHROME_FOUND=0

if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    CHROME_FOUND=1
elif command -v google-chrome &> /dev/null; then
    CHROME_PATH=$(which google-chrome)
    CHROME_FOUND=1
elif command -v google-chrome-stable &> /dev/null; then
    CHROME_PATH=$(which google-chrome-stable)
    CHROME_FOUND=1
elif command -v chrome &> /dev/null; then
    CHROME_PATH=$(which chrome)
    CHROME_FOUND=1
elif [ -f "C:/Program Files/Google/Chrome/Application/chrome.exe" ]; then
    CHROME_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe"
    CHROME_FOUND=1
fi

if [ $CHROME_FOUND -eq 0 ]; then
    echo "❌ Chrome is not installed"
    echo "   Install from: https://www.google.com/chrome/"
    exit 1
fi
echo "   Chrome found at: $CHROME_PATH ✓"
echo

# Check if chrome-devtools-mcp is accessible
echo "✓ Checking chrome-devtools-mcp package..."
if npx --yes chrome-devtools-mcp@latest --help &> /dev/null; then
    echo "   chrome-devtools-mcp@latest accessible ✓"
else
    echo "❌ Failed to access chrome-devtools-mcp@latest"
    echo "   Check your internet connection and npm registry access"
    exit 1
fi
echo

# Check MCP configuration file
echo "✓ Checking MCP configuration..."
MCP_CONFIG=""

# Check common MCP config locations
if [ -f "$HOME/.config/claude-code/mcp.json" ]; then
    MCP_CONFIG="$HOME/.config/claude-code/mcp.json"
elif [ -f "$HOME/.claude/mcp.json" ]; then
    MCP_CONFIG="$HOME/.claude/mcp.json"
elif [ -f "$HOME/Library/Application Support/Claude/mcp.json" ]; then
    MCP_CONFIG="$HOME/Library/Application Support/Claude/mcp.json"
elif [ -f "$HOME/.config/Code/User/globalStorage/claude-code/mcp.json" ]; then
    MCP_CONFIG="$HOME/.config/Code/User/globalStorage/claude-code/mcp.json"
fi

if [ -z "$MCP_CONFIG" ]; then
    echo "⚠️  MCP configuration file not found"
    echo "   This is normal if you haven't set up MCP servers yet"
    echo "   To add chrome-devtools MCP server, run:"
    echo "   claude mcp add chrome-devtools npx chrome-devtools-mcp@latest"
else
    echo "   Found MCP config: $MCP_CONFIG ✓"

    # Check if chrome-devtools is configured
    if grep -q "chrome-devtools" "$MCP_CONFIG" 2>/dev/null; then
        echo "   chrome-devtools server configured ✓"
    else
        echo "   chrome-devtools server not configured"
        echo "   To add, run: claude mcp add chrome-devtools npx chrome-devtools-mcp@latest"
    fi
fi
echo

# Check for common issues
echo "✓ Checking for common issues..."

# Check user-data-dir permissions
PROFILE_DIR="$HOME/.cache/chrome-devtools-mcp"
if [ -d "$PROFILE_DIR" ]; then
    if [ -w "$PROFILE_DIR" ]; then
        echo "   Profile directory writable ✓"
    else
        echo "⚠️  Profile directory not writable: $PROFILE_DIR"
        echo "   Run: chmod -R u+w $PROFILE_DIR"
    fi
else
    echo "   Profile directory will be created on first use ✓"
fi
echo

# Summary
echo "========================================"
echo "✅ Setup validation complete!"
echo
echo "Next steps:"
echo "1. Configure MCP server (if not done):"
echo "   claude mcp add chrome-devtools npx chrome-devtools-mcp@latest"
echo
echo "2. Test with Claude Code:"
echo '   Ask: "Check the performance of https://developers.chrome.com"'
echo
echo "3. View configuration options:"
echo "   npx chrome-devtools-mcp@latest --help"
echo

exit 0
