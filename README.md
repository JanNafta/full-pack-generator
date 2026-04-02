<div align="center">

# Full Pack Generator

### AI-Powered Ad Creative Production for Google UAC

Give it a Google Play link. Get 20 ready-to-upload ad creatives back.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Anthropic-191919?style=for-the-badge&logo=anthropic&logoColor=white)](https://claude.ai/claude-code)
[![Replicate](https://img.shields.io/badge/Replicate-AI_Models-FF6B6B?style=for-the-badge)](https://replicate.com)
[![Status](https://img.shields.io/badge/Status-Active-00C853?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)]()

---

**One command** &rarr; Research &rarr; Strategy &rarr; Generation &rarr; QA &rarr; **20 creatives on your Desktop**

</div>

---

## What is this?

Full Pack Generator takes any Google Play Store app link and automatically produces a complete set of advertising images ready to upload to Google Ads. No Photoshop. No design team. No manual work.

You run one slash command inside [Claude Code](https://claude.ai/claude-code). A few minutes later, you have a folder on your Desktop with 20 professionally crafted, policy-compliant ad creatives across multiple formats and visual approaches -- each one individually inspected by AI and regenerated if it doesn't meet the quality bar.

```
/full-pack-generator https://play.google.com/store/apps/details?id=com.example.app
```

That's it. The entire pipeline -- from research to final deliverable -- runs autonomously.

---

## Why this exists

Media buyers running Google UAC (Universal App Campaigns) need a constant stream of fresh creatives. The typical workflow looks like this:

1. Research the app manually -- screenshots, reviews, competitor landscape
2. Brief a designer or design agency
3. Wait days (or weeks) for deliverables
4. Discover half the creatives violate Google Ads policies
5. Request revisions, wait again
6. Upload, test, repeat

**Full Pack Generator collapses this entire process into a single command.** It handles the research, develops the creative strategy, generates the images using AI, validates every single one against Google's policies, and packages the final output. What used to take days now takes minutes.

---

## Pipeline

The system runs in 5 phases with aggressive parallelism at every stage:

```
                         Google Play URL
                              |
                              v
              +-------------------------------+
              |     PHASE 1: RESEARCH         |
              |   (3 parallel agents)         |
              +-------------------------------+
              |               |               |
              v               v               v
         App Data        Branding        Reviews
       (metadata,      (colors,        (5-star,
        icon,           logo,          selling
        screenshots)    tone)          points)
              |               |               |
              v               v               v
              +-------------------------------+
              |   PHASE 1.5: ASSET UPLOAD     |
              |  (starts as soon as icon is   |
              |   ready -- doesn't wait)      |
              +-------------------------------+
                              |
                              v
              +-------------------------------+
              |   PHASE 2: CREATIVE STRATEGY  |
              |  2 concepts x angles/hooks    |
              +-------------------------------+
                              |
                              v
              +-------------------------------+
              |   PHASE 3: GENERATION         |
              |   (4 parallel agents)         |
              +-------------------------------+
              |         |         |           |
              v         v         v           v
          Approach  Approach  Approach    Native
             A         B         C         Ads
          (HTML     (Pure     (Asset      (2 in-feed
          Mockup)   Prompt)   Reference)   images)
           6 imgs    6 imgs    6 imgs     2 imgs
              |         |         |           |
              +----+----+----+----+----+------+
                   |              |
                   v              v
            Inline QA        Inline QA
          (per image)      (per image)
                   |              |
                   v              v
              +-------------------------------+
              |   PHASE 5: SUMMARY            |
              |  Report + open all-creatives/ |
              +-------------------------------+
                              |
                              v
                    ~/Desktop/full-pack-
                    generator-runs/{app}/v1/
                        all-creatives/
                        (20 approved images)
```

Every image goes through **inline QA** immediately after generation. There is no separate review phase -- generation and quality control are a single loop that iterates until the image passes inspection.

---

## Features

### Research (Phase 1)
- Scrapes full app metadata from Google Play (name, developer, rating, downloads, description)
- Downloads the high-res app icon and all Play Store screenshots
- Visits the developer's website to extract brand colors, logos, and visual tone
- Analyzes 30-50 five-star reviews to identify top selling points and emotional hooks
- All 3 research agents run in parallel

### Strategy (Phase 2)
- Selects the 2 strongest creative angles from 10 proven ad frameworks (Hero Screenshot, Social Proof, Feature Spotlight, Lifestyle, Urgency, etc.)
- Generates headlines (max 30 chars), descriptions (max 90 chars), visual directions, and prompt keywords for each concept
- Produces a full creative brief saved as Markdown

### Generation (Phase 3)
- **Approach A -- HTML Mockup**: Builds a pixel-level HTML/CSS mockup of each ad, screenshots it with Playwright, then uses AI to transform it into a polished banner. Gives the most layout control.
- **Approach B -- Pure Prompt**: Generates directly from text prompts + the app icon. Pure AI creativity with brand guardrails.
- **Approach C -- Asset Reference**: Combines the icon + real app screenshots as multi-image input. Produces the most authentic-looking results.
- **Native Ads**: 2 editorial-style in-feed images designed to blend with organic content.
- All 4 generation streams run as parallel agents

### QA (Inline)
- Every image is visually inspected by Claude immediately after generation
- Checks for: artifacts, gibberish text, wrong anatomy, upside-down devices, policy violations, brand consistency, correct app icon, professional composition
- Failed images get their prompt automatically adjusted and are regenerated
- No retry limit -- iterates until perfect
- Quality bar: "If you have to look twice at something, it's a FAIL"

### Google UAC Compliance
- No "Download" or "Install" text (policy violation)
- No fake buttons or UI elements
- Content centered in safe zone (center 80%)
- Text overlay under 25%
- JPG format, under 5MB per image
- Every image is 100% unique for proper A/B testing

---

## What you get

Each run produces **20 ad creative images** in the exact sizes Google Ads requires:

| Format | Dimensions | Aspect Ratio | Count |
|--------|-----------|--------------|-------|
| Landscape | 1200 x 628 | 1.91:1 | 6 |
| Square | 1200 x 1200 | 1:1 | 6 |
| Portrait | 1200 x 1500 | 4:5 | 6 |
| Native | 1200 x 627 | ~1.91:1 | 2 |
| | | **Total** | **20** |

The 18 banners come from 3 different generation approaches (A, B, C) x 2 creative concepts x 3 sizes. This gives you maximum visual diversity for A/B testing.

All approved images land in a single `all-creatives/` folder with descriptive filenames:

```
all-creatives/
  A_hero-your-photos-reimagined_1200x628.jpg
  A_hero-your-photos-reimagined_1200x1200.jpg
  A_hero-your-photos-reimagined_1200x1500.jpg
  A_social-proof-1m-users_1200x628.jpg
  B_feature-ai-photo-magic_1200x628.jpg
  B_feature-ai-photo-magic_1200x1200.jpg
  C_lifestyle-create-anywhere_1200x1500.jpg
  native_photo-restoration_1200x627.jpg
  ...
```

Upload the entire folder to Google Ads. Done.

---

## Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| Orchestrator | [Claude Code](https://claude.ai/claude-code) | Runs the full pipeline, launches parallel agents, makes creative decisions, performs visual QA |
| Image Generation | [Replicate API](https://replicate.com) | Three-tier model cascade for AI image generation |
| Primary Model | `google/nano-banana-2` | Fast, high-quality image generation (Tier 1) |
| Fallback Model | `google/nano-banana-pro` | Higher quality fallback (Tier 2) |
| Last Resort Model | `black-forest-labs/flux-2-flex` | Different architecture, final fallback (Tier 3) |
| Web Scraping | [Playwright MCP](https://github.com/playwright-community/playwright-mcp) | Browser automation for Google Play and developer websites |
| HTML Screenshots | [Playwright (Node.js)](https://playwright.dev) | Renders HTML mockups to JPG for Approach A |
| Image Processing | `sips` (macOS built-in) | Resizes generated images to exact UAC dimensions |
| Language | Python 3 | Replicate API wrapper with cascade logic |

---

## Quick Start

### Prerequisites

| Requirement | Install |
|-------------|---------|
| **Claude Code** | `npm install -g @anthropic-ai/claude-code` |
| **Node.js** (18+) | `brew install node` or [nodejs.org](https://nodejs.org) |
| **Python 3** (3.8+) | `brew install python3` or [python.org](https://python.org) |
| **Replicate account** | Sign up at [replicate.com](https://replicate.com/account/api-tokens) |

### Install

```bash
# Clone the repository
git clone https://github.com/JanNafta/full-pack-generator.git
cd full-pack-generator

# Run the installer (checks prerequisites, copies files to Claude Code config)
chmod +x install.sh
./install.sh
```

The installer copies two files into your Claude Code configuration:
- `~/.claude/commands/full-pack-generator.md` -- the skill (slash command)
- `~/.claude/utils/replicate_gen.py` -- the Replicate API wrapper

### Configure the Replicate API key

**Option A: Environment variable**
```bash
export REPLICATE_API_TOKEN="r8_your_token_here"

# Make it permanent:
echo 'export REPLICATE_API_TOKEN="r8_your_token_here"' >> ~/.zshrc
```

**Option B: Claude Code secrets file**

Create or edit `~/.claude/secrets.md`:
```markdown
## APIs - Replicate
- API Token: `r8_your_token_here`
```

### Set up Playwright MCP

Claude Code needs a Playwright MCP server for browser automation:

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

For true parallel research (optional, but recommended):
```bash
claude mcp add playwright-2 -- npx @playwright/mcp@latest
claude mcp add playwright-3 -- npx @playwright/mcp@latest
```

### Run

```bash
# Start Claude Code with permissions bypass (required for autonomous operation)
claude --dangerously-skip-permissions

# Run the skill
/full-pack-generator https://play.google.com/store/apps/details?id=com.example.app
```

> **Note on `--dangerously-skip-permissions`**: The skill launches parallel agents, runs shell commands, reads/writes files, and automates browsers. Without this flag, Claude Code asks for permission on every single action, making the workflow unusable. The skill only writes to `~/Desktop/full-pack-generator-runs/` and `~/.claude/`.

---

## Configuration

### Model selection

The Replicate wrapper (`replicate_gen.py`) defaults to auto-cascade mode. You can override this:

```bash
# Auto cascade (default) -- starts with nano-banana-2, escalates on failures
python3 replicate_gen.py generate "your prompt" -o output.jpg

# Force a specific model
python3 replicate_gen.py generate "your prompt" -o output.jpg --model nano
python3 replicate_gen.py generate "your prompt" -o output.jpg --model nano-pro
python3 replicate_gen.py generate "your prompt" -o output.jpg --model flux

# Check current cascade status
python3 replicate_gen.py status
```

### Cascade behavior

| Tier | Model | Escalation Trigger |
|------|-------|--------------------|
| 1 | `google/nano-banana-2` | Default starting point |
| 2 | `google/nano-banana-pro` | After 10 consecutive Tier 1 failures |
| 3 | `black-forest-labs/flux-2-flex` | After 10 consecutive Tier 2 failures |

- If the current model succeeds, the failure counter resets to 0
- Once escalated to a higher tier, the system **never goes back** to a lower one
- Each image is retried if it returns `None` (model failed but threshold not reached)

### Output location

All runs go to `~/Desktop/full-pack-generator-runs/{app-name}/v{N}/`. Version numbers auto-increment, so previous runs are never overwritten.

---

## Usage Examples

### Basic usage -- generate creatives for any app

```bash
/full-pack-generator https://play.google.com/store/apps/details?id=com.spotify.music
```

### Using the utility script directly

```bash
# Upload an image to Replicate (returns a URL for use in generation)
python3 ~/.claude/utils/replicate_gen.py upload ./my-icon.png

# Generate a single image
python3 ~/.claude/utils/replicate_gen.py generate \
  "Professional app ad banner, premium quality, vibrant colors" \
  -o banner.jpg -a 16:9 -r 1K \
  -i "https://replicate.delivery/..." \
  --uac landscape

# Generate with forced model
python3 ~/.claude/utils/replicate_gen.py generate \
  "Minimalist app showcase" \
  -o showcase.jpg -a 1:1 --model flux

# Batch generate from a JSON spec
python3 ~/.claude/utils/replicate_gen.py batch jobs.json
```

### Batch generation JSON format

```json
[
  {
    "prompt": "Professional app banner with phone mockup",
    "filepath": "./output/banner-1.jpg",
    "aspect_ratio": "16:9",
    "resolution": "1K",
    "image_input": ["https://replicate.delivery/icon-url"],
    "uac_size": "landscape"
  },
  {
    "prompt": "Square ad with feature spotlight",
    "filepath": "./output/banner-2.jpg",
    "aspect_ratio": "1:1",
    "resolution": "1K",
    "uac_size": "square"
  }
]
```

---

## Project Structure

```
full-pack-generator/
|-- full-pack-generator.md     # The skill definition (Claude Code slash command)
|-- utils/
|   +-- replicate_gen.py       # Replicate API wrapper with 3-tier cascade
|-- install.sh                 # One-command installer
|-- README.md                  # This file
+-- .gitignore
```

### Output directory structure (generated per run)

```
~/Desktop/full-pack-generator-runs/{app-name}/v{N}/
|-- research/
|   |-- app-data.json              # Full Google Play metadata
|   |-- icon.png                   # High-res app icon
|   |-- screenshots/               # All Play Store screenshots
|   |   |-- screenshot-01.jpg
|   |   |-- screenshot-02.jpg
|   |   +-- ...
|   |-- branding/
|   |   +-- brand-analysis.json    # Colors, fonts, tone
|   |-- reviews-analysis.md        # Top selling points from 5-star reviews
|   +-- creative-brief.md          # 2 concepts with headlines and visual directions
|-- banners/
|   |-- approach-a-mockup/
|   |   |-- html/                  # HTML/CSS mockup source files
|   |   |-- mockups/               # Playwright screenshots of the mockups
|   |   +-- final/                 # AI-enhanced versions (landscape/square/portrait)
|   |-- approach-b-prompt/
|   |   +-- final/                 # Pure prompt generations
|   +-- approach-c-assets/
|       +-- final/                 # Multi-image fusion generations
|-- native/                        # 2 native in-feed ad images
|-- all-creatives/                 # >>> THE DELIVERABLE -- all 20 approved images <<<
|   |-- A_hero-app-name_1200x628.jpg
|   |-- A_hero-app-name_1200x1200.jpg
|   |-- B_social-proof-5-stars_1200x628.jpg
|   +-- ...
+-- summary.md                     # Run report with QA results and model usage
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `REPLICATE_API_TOKEN not set` | Set the env var: `export REPLICATE_API_TOKEN="r8_..."` or add it to `~/.claude/secrets.md` |
| `playwright not found` | Run `npx playwright install chromium` |
| `sips command not found` | macOS only. On Linux, install ImageMagick and replace `sips -z H W file` with `convert file -resize WxH! file` |
| Models keep failing | The cascade auto-escalates through 3 tiers. If all fail, Replicate may be overloaded -- wait and retry. |
| Images look wrong | The inline QA catches most issues. For persistent problems, force the flux model: `--model flux` |
| Agents running sequentially | Add multiple Playwright MCP servers (see Quick Start) for true parallel browser automation |
| Permission prompts interrupt flow | Run Claude Code with `--dangerously-skip-permissions` |

---

## Contributing

Contributions are welcome. Here are some areas where help would be valuable:

- **Linux/Windows support** -- replace macOS-specific `sips` with cross-platform image processing
- **New generation approaches** -- additional creative strategies beyond the current A/B/C
- **Additional ad networks** -- Meta Ads, TikTok Ads, Unity Ads creative specs
- **iOS App Store support** -- extend research phase to scrape App Store data
- **Prompt engineering** -- better prompts for higher quality generations

To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-improvement`)
3. Make your changes
4. Test with a real Google Play URL
5. Open a pull request

---

## Author

**Jan Naftanaila** -- Media Buyer & AI Automation Specialist

Building tools that turn hours of manual creative production into single commands.

- GitHub: [@JanNafta](https://github.com/JanNafta)
- LinkedIn: [Jan Naftanaila](https://www.linkedin.com/in/jannafta/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Built with [Claude Code](https://claude.ai/claude-code) + [Replicate](https://replicate.com) + [Playwright](https://playwright.dev)

**Star this repo if you find it useful** -- it helps others discover it.

</div>
