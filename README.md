# Full Pack Generator

Generate a complete ad creative pack from a Google Play Store URL — fully automated by AI.

One command. 20 unique creatives. Ready for Google UAC campaigns.

## What it does

You give it a Google Play URL. It gives you a folder of ready-to-upload ad creatives.

1. **Research** — Scrapes Google Play for app metadata, screenshots, icon, and 5-star reviews. Visits the developer's website for brand colors and assets.
2. **Strategy** — Analyzes the research to generate 2 creative concepts with headlines, visual directions, and prompt keywords.
3. **Banners** — Creates 18 banner ads using 3 different approaches:
   - **Approach A (Mockup):** Generates an HTML mockup → screenshots it → feeds it to AI for enhancement
   - **Approach B (Prompt):** Pure AI generation from text prompts + app icon
   - **Approach C (Assets):** Multi-image fusion combining icon + screenshots
4. **Native Ads** — 2 native in-feed ads with organic, editorial feel
5. **QA** — Every single image is visually inspected immediately after generation. Failures are regenerated automatically until perfect.

### Output sizes (Google UAC compliant)

| Size | Dimensions | Aspect Ratio |
|------|-----------|--------------|
| Landscape | 1200x628 | 1.91:1 |
| Square | 1200x1200 | 1:1 |
| Portrait | 1200x1500 | 4:5 |
| Native | 1200x627 | ~1.91:1 |

### AI Models (3-tier cascade)

| Tier | Model | When |
|------|-------|------|
| 1 | `google/nano-banana-2` | Primary — tried first |
| 2 | `google/nano-banana-pro` | After 10 consecutive Tier 1 failures |
| 3 | `black-forest-labs/flux-2-flex` | After 10 consecutive Tier 2 failures |

Once a tier escalates, it never goes back. If the current model succeeds, the failure counter resets.

---

## Prerequisites

You need 3 things installed on your machine:

### 1. Claude Code (the AI CLI)

Claude Code is Anthropic's official CLI tool. It's what orchestrates the entire pipeline.

```bash
# Install via npm (requires Node.js)
npm install -g @anthropic-ai/claude-code

# Verify it works
claude --version
```

If you don't have Node.js yet:
- **macOS:** `brew install node` (or download from https://nodejs.org)
- **Windows:** Download from https://nodejs.org
- **Linux:** `curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs`

After installing Claude Code, authenticate. Your workshop instructor will provide an OAuth code:
```bash
claude auth login --oauth-code YOUR_CODE_HERE
```

Or if you have your own Anthropic account, just run `claude` and it will open a browser to log in.

### 2. Replicate API key

The image generation uses Replicate's API. You need an account and API token.

1. Go to https://replicate.com and sign up
2. Go to https://replicate.com/account/api-tokens
3. Create a new token and copy it

You'll configure this during installation (see below).

### 3. Python 3 + requests library

```bash
# Check if Python 3 is installed
python3 --version

# Install requests (the only Python dependency)
pip3 install requests
```

### 4. Playwright (Node.js package + MCP Server)

The skill needs Playwright for two things:
- **Node.js package** — to screenshot HTML mockups (Approach A)
- **MCP Server** — for Claude to scrape Google Play and developer websites

```bash
# Install the Node.js package (for HTML screenshots)
npm install -g playwright

# Install the Chromium browser
npx playwright install chromium
```

Then configure the MCP server so Claude Code can use browser automation:

**Option A: Use the official Playwright MCP (recommended)**

Add this to your Claude Code MCP settings. You can do this by running:

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

This registers a Playwright MCP server that Claude Code can use for browser automation.

**Option B: Manual configuration**

Create or edit `~/.claude.json` and add:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**For better parallelism** (optional): The skill launches 3 research agents simultaneously. Each agent needs its own browser. If you want true parallelism, add multiple Playwright MCP servers:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "playwright-2": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "playwright-3": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

With 1 MCP, the agents run sequentially (still works, just slower). With 3, they run in true parallel.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/jannafta/full-pack-generator.git
cd full-pack-generator

# 2. Run the installer
chmod +x install.sh
./install.sh
```

The installer copies 2 files into your Claude Code configuration:
- `~/.claude/commands/full-pack-generator.md` — the skill definition (slash command)
- `~/.claude/utils/replicate_gen.py` — the Replicate API wrapper

### Configure your Replicate API key

Choose one of these options:

**Option A: Environment variable (recommended for quick setup)**
```bash
export REPLICATE_API_TOKEN="r8_your_token_here"
```
Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent.

**Option B: Claude Code secrets file (recommended for persistent setup)**

Create or edit `~/.claude/secrets.md`:
```markdown
## APIs - Replicate
- API Token: `r8_your_token_here`
```

The skill reads this file automatically during execution.

---

## Usage

### Important: Permission mode

This skill launches many agents, runs bash commands, reads/writes files, and uses browser automation. In normal mode, Claude Code will ask for permission on **every single action** — which makes it unusable for this workflow.

You need to run Claude Code with **bypass permissions** enabled:

```bash
claude --dangerously-skip-permissions
```

This lets Claude execute all tools without asking for confirmation. The terminal prompt changes from `>` to `⏵⏵` to indicate you're in bypass mode.

> **Warning**: This flag gives Claude full access to your system (files, terminal, browser). Only use it if you understand and accept the risks. The skill only writes to `~/Desktop/full-pack-generator-runs/` and `~/.claude/`.

### Running the skill

```bash
# 1. Start Claude Code with bypass permissions
claude --dangerously-skip-permissions

# 2. Run the skill with a Google Play URL
/full-pack-generator https://play.google.com/store/apps/details?id=com.example.app
```

That's it. Claude will:
1. Launch parallel agents to research the app
2. Upload the icon and screenshots to Replicate
3. Generate a creative strategy brief
4. Launch 4 parallel agents to produce images across all approaches
5. QA every image in real-time (regenerating any that fail)
6. Package everything in a clean `all-creatives/` folder on your Desktop

### Where do the files go?

All output goes to your Desktop:
```
~/Desktop/full-pack-generator-runs/{app-name}/v{N}/
```

Each run gets an auto-incremented version number, so you never overwrite previous work.

---

## Output structure

```
v1/
├── research/
│   ├── app-data.json          # All Google Play metadata
│   ├── icon.png               # App icon (high-res)
│   ├── screenshots/           # All Play Store screenshots
│   │   ├── screenshot-01.jpg
│   │   ├── screenshot-02.jpg
│   │   └── ...
│   ├── branding/
│   │   └── brand-analysis.json
│   ├── reviews-analysis.md
│   └── creative-brief.md      # The 2 creative concepts
├── banners/
│   ├── approach-a-mockup/
│   │   ├── html/              # HTML mockup files
│   │   ├── mockups/           # Screenshots of the mockups
│   │   └── final/
│   │       ├── landscape/
│   │       ├── square/
│   │       └── portrait/
│   ├── approach-b-prompt/
│   │   └── final/
│   │       ├── landscape/
│   │       ├── square/
│   │       └── portrait/
│   └── approach-c-assets/
│       └── final/
│           ├── landscape/
│           ├── square/
│           └── portrait/
├── native/
├── all-creatives/             # <<< THE DELIVERABLE — all 20 approved images
│   ├── A_hero-app-name_1200x628.jpg
│   ├── A_hero-app-name_1200x1200.jpg
│   ├── A_hero-app-name_1200x1500.jpg
│   ├── B_social-proof-5-stars_1200x628.jpg
│   └── ...
└── summary.md                 # Run report with QA results
```

The `all-creatives/` folder is what you upload directly to Google Ads.

---

## How the QA works

Every image goes through this pipeline immediately after generation:

1. **Generate** via Replicate API
2. **Resize** to exact UAC dimensions (`sips -z HEIGHT WIDTH`)
3. **Visual inspection** — Claude reads the image and checks:
   - No artifacts or distortions
   - No gibberish/illegible text
   - Correct anatomy (5 fingers on hands)
   - Devices right-side up (notch at top)
   - No "Download"/"Install" text (Google policy)
   - Brand colors match
   - Real app icon visible (not AI-invented)
   - Professional composition
4. **PASS** → Renamed and copied to `all-creatives/`
5. **FAIL** → Prompt adjusted, regenerated, re-inspected. No retry limit — iterates until perfect.

---

## Google UAC Compliance

All generated images follow Google Ads App Campaign policies:
- No "Download" or "Install" text
- No fake buttons or UI elements
- Content centered in safe zone (center 80%)
- Text overlay under 25%
- JPG format, under 5MB
- Every image is 100% unique (proper A/B testing)

---

## Model cascade behavior

The generator uses a 3-tier model cascade:

1. **Tier 1:** `google/nano-banana-2` — the default. Fast, good quality.
2. **Tier 2:** `google/nano-banana-pro` — higher quality, slightly slower.
3. **Tier 3:** `black-forest-labs/flux-2-flex` — last resort, different style.

How it works:
- Starts on Tier 1 and stays there as long as it works
- Each failure increments a counter. After **10 consecutive failures**, it escalates to the next tier
- If the current model succeeds at any point, the counter resets to 0 (but it stays on the current tier)
- Once escalated, it **never goes back** to a previous tier
- You can force a specific model with `--model nano`, `--model nano-pro`, or `--model flux`

---

## Troubleshooting

### "REPLICATE_API_TOKEN not set"
Set the environment variable: `export REPLICATE_API_TOKEN="r8_..."` or add it to `~/.claude/secrets.md`.

### "playwright" not found
Run `npx playwright install chromium` to install the browser.

### Images look wrong or low quality
The QA system catches most issues automatically. If you see consistent problems, try forcing the flux model: edit the skill or pass `--model flux` to the utility script.

### "sips" command not found
`sips` is a macOS-only tool (comes preinstalled on all Macs). On Linux/Windows, install ImageMagick and replace `sips -z H W file` with `convert file -resize WxH! file`.

### Models keep failing
This usually means models are overloaded on Replicate. The system auto-escalates through 3 tiers (nano-banana-2 → nano-banana-pro → flux-2-flex), giving each 10 attempts. You can also force a specific model: `--model nano`, `--model nano-pro`, or `--model flux`.

---

## Powered by

- **[Claude Code](https://claude.ai/claude-code)** — orchestration, strategy, HTML mockups, QA
- **[Replicate](https://replicate.com)** — AI image generation (nano-banana-2 → nano-banana-pro → flux-2-flex)
- **[Playwright](https://playwright.dev)** — web scraping and HTML screenshots

---

Built for the Copenhagen Workshop: AI-Powered Creative Production at Scale.
