# Paper2Poster4Harness

Generate academic posters from papers using Claude Code - no API keys needed.

## How It Works

1. **Drop** your paper PDF into the `input/` folder
2. **Tell** Claude Code: "포스터 만들어줘" or "Generate a poster"
3. **Get** your poster in `output/` (PPTX + PNG)

Claude Code follows the instructions in `AGENTS.md` to orchestrate the full pipeline:
- **AI tasks** (content structuring, figure selection, bullet generation) - Claude does these directly
- **Non-AI tasks** (PDF parsing, layout math, PPTX rendering) - Python scripts handle these

No API keys. No environment variables. Just your Claude Code subscription.

## What This Repo Changes

This repository replaces the AI backend of Paper2Poster while keeping the **entire original pipeline intact**:

| Component | Original Paper2Poster | This Harness Version |
|---|---|---|
| AI Backend | CAMEL + OpenAI API (requires API key) | `claude -p` CLI (subscription, no key) |
| Layout | Tree-split learned from 60+ posters ✅ | Same ✅ |
| Overflow Detection | VLM (GPT-4o Vision) loop | Heuristic-based loop |
| PPTX Code Generation | LLM generates python-pptx code ✅ | Same ✅ |
| Theme & Style | AI-driven theme selection ✅ | Same ✅ |
| Content Refinement | Multi-round critic loop ✅ | Same ✅ |

## Prerequisites

- [Claude Code](https://github.com/anthropics/claude-code) or [OpenCode](https://github.com/opencode-ai/opencode) installed
- Python 3.10+
- LibreOffice (`soffice`) for PNG preview

## Setup

```bash
git clone https://github.com/smilebank7/Paper2Poster4Harness.git
cd Paper2Poster4Harness
pip install -r requirements.txt
```

## Usage

```bash
# 1. Drop your paper
cp my_paper.pdf input/

# 2. Open Claude Code in this directory
claude  # or opencode

# 3. Tell it to make a poster
> 포스터 만들어줘
> Generate a poster from the paper in input/
```

## Architecture

```text
input/paper.pdf
    |
    v  [Script] parse_pdf.py - Docling extracts text + figures
    |
    v  [Claude AI] Structure content into JSON sections
    |
    v  [Claude AI] Select relevant figures
    |
    v  [Claude AI] Assign figures to sections
    |
    v  [Script] generate_layout.py - Tree-split algorithm
    |
    v  [Claude AI] Generate bullet-point content
    |
    v  [Script] render_poster.py - python-pptx generates PPTX
    |
output/poster.pptx + poster.png
```

## Credits

Based on [Paper2Poster](https://github.com/Paper2Poster/Paper2Poster) (NeurIPS 2025).
Original architecture, prompts, and layout algorithm by the Paper2Poster team.

## License

MIT
