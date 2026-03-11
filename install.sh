#!/bin/bash
# Full Pack Generator — Install Script
# Sets up everything needed to run the skill in Claude Code

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMMANDS_DIR="$HOME/.claude/commands"
UTILS_DIR="$HOME/.claude/utils"

echo "╔══════════════════════════════════════════╗"
echo "║   Full Pack Generator — Installer        ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── Step 1: Check prerequisites ──────────────────────────────────────────────

echo "Step 1/4: Checking prerequisites..."
echo ""

MISSING=0

# Claude Code
if command -v claude &>/dev/null; then
    echo "  ✓ Claude Code: $(claude --version 2>/dev/null || echo 'installed')"
else
    echo "  ✗ Claude Code: NOT FOUND"
    echo "    Install: npm install -g @anthropic-ai/claude-code"
    echo "    Then run 'claude' once to authenticate"
    MISSING=1
fi

# Node.js
if command -v node &>/dev/null; then
    echo "  ✓ Node.js: $(node --version)"
else
    echo "  ✗ Node.js: NOT FOUND"
    echo "    Install: brew install node (macOS) or https://nodejs.org"
    MISSING=1
fi

# Python 3
if command -v python3 &>/dev/null; then
    echo "  ✓ Python 3: $(python3 --version 2>&1 | cut -d' ' -f2)"
else
    echo "  ✗ Python 3: NOT FOUND"
    echo "    Install: brew install python3 (macOS) or https://python.org"
    MISSING=1
fi

# requests
if python3 -c "import requests" 2>/dev/null; then
    echo "  ✓ Python requests: installed"
else
    echo "  ✗ Python requests: NOT FOUND"
    echo "    Installing now..."
    pip3 install requests --quiet
    if python3 -c "import requests" 2>/dev/null; then
        echo "  ✓ Python requests: installed"
    else
        echo "    FAILED — run manually: pip3 install requests"
        MISSING=1
    fi
fi

# Playwright Chromium
if npx playwright --version &>/dev/null 2>&1; then
    echo "  ✓ Playwright: installed"
else
    echo "  ⚠ Playwright: not found — installing Chromium browser..."
    npx playwright install chromium 2>/dev/null || {
        echo "    FAILED — run manually: npx playwright install chromium"
        MISSING=1
    }
    echo "  ✓ Playwright Chromium: installed"
fi

# Playwright MCP
if command -v claude &>/dev/null; then
    # Check if playwright MCP is already configured
    if claude mcp list 2>/dev/null | grep -q "playwright"; then
        echo "  ✓ Playwright MCP: already configured"
    else
        echo "  ⚠ Playwright MCP: not configured"
        echo "    Adding Playwright MCP server to Claude Code..."
        claude mcp add playwright -- npx @playwright/mcp@latest 2>/dev/null && {
            echo "  ✓ Playwright MCP: configured"
        } || {
            echo "    Could not auto-configure. Add manually:"
            echo "    claude mcp add playwright -- npx @playwright/mcp@latest"
        }
    fi
fi

# Replicate API key
if [ -n "$REPLICATE_API_TOKEN" ]; then
    echo "  ✓ Replicate API key: set (env var)"
elif grep -q "Replicate" "$HOME/.claude/secrets.md" 2>/dev/null; then
    echo "  ✓ Replicate API key: found in ~/.claude/secrets.md"
else
    echo "  ⚠ Replicate API key: NOT CONFIGURED"
    echo "    Option A: export REPLICATE_API_TOKEN=\"r8_your_token_here\""
    echo "    Option B: Add to ~/.claude/secrets.md:"
    echo "      ## APIs - Replicate"
    echo "      - API Token: \`r8_your_token_here\`"
    echo "    Get your key at: https://replicate.com/account/api-tokens"
fi

echo ""

if [ "$MISSING" -eq 1 ]; then
    echo "⚠  Some prerequisites are missing (see above)."
    echo "   The skill will be installed, but may not work until they're resolved."
    echo ""
fi

# ── Step 2: Create directories ───────────────────────────────────────────────

echo "Step 2/4: Creating directories..."
mkdir -p "$COMMANDS_DIR"
mkdir -p "$UTILS_DIR"
echo "  ✓ $COMMANDS_DIR"
echo "  ✓ $UTILS_DIR"
echo ""

# ── Step 3: Copy files ───────────────────────────────────────────────────────

echo "Step 3/4: Installing skill files..."

cp "$SCRIPT_DIR/full-pack-generator.md" "$COMMANDS_DIR/full-pack-generator.md"
echo "  ✓ Skill    → $COMMANDS_DIR/full-pack-generator.md"

cp "$SCRIPT_DIR/utils/replicate_gen.py" "$UTILS_DIR/replicate_gen.py"
chmod +x "$UTILS_DIR/replicate_gen.py"
echo "  ✓ Utility  → $UTILS_DIR/replicate_gen.py"
echo ""

# ── Step 4: Verify ───────────────────────────────────────────────────────────

echo "Step 4/4: Verifying installation..."

if [ -f "$COMMANDS_DIR/full-pack-generator.md" ] && [ -f "$UTILS_DIR/replicate_gen.py" ]; then
    echo "  ✓ All files installed successfully"
else
    echo "  ✗ Something went wrong — check file permissions"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Installation complete!                 ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "Usage:"
echo "  1. Open a terminal and run: claude"
echo "  2. Type: /full-pack-generator https://play.google.com/store/apps/details?id=com.example.app"
echo ""
echo "Output goes to: ~/Desktop/full-pack-generator-runs/"
echo ""
