# Paper2Poster4Harness

## Overview
This project generates academic posters from research papers using Claude Code/OpenCode as the AI backend.
No API keys needed — uses your Claude subscription through the CLI harness.

## How It Works
Original Paper2Poster uses CAMEL framework + OpenAI API. This version replaces ALL AI calls with
`claude -p` CLI subprocess calls, so your Claude Code subscription handles the AI workload.

## Pipeline (6 stages)
1. **Parse** — Docling extracts PDF -> Markdown, Claude structures into JSON sections
2. **Filter** — Claude selects relevant figures/tables from extracted images
3. **Plan** — Claude assigns figures to sections, computes layout ratios
4. **Layout** — Deterministic tree-split algorithm generates bounding boxes (no AI)
5. **Content** — Claude generates bullet-point content per section, with heuristic overflow detection
6. **Render** — python-pptx generates the final poster.pptx

## Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt
sudo apt install libreoffice  # or download soffice

# 2. Prepare your paper
mkdir -p data/my_paper
cp my_paper.pdf data/my_paper/paper.pdf

# 3. Generate poster
python run.py --paper_path data/my_paper/paper.pdf --poster_width_inches 48 --poster_height_inches 36
```

## For Claude Code Users
When using this repo with Claude Code, you can simply say:
> "Generate a poster from the paper at data/my_paper/paper.pdf"

Claude Code will read this AGENTS.md and follow the pipeline automatically.

## Prerequisites
- Claude Code CLI (`claude`) or OpenCode CLI installed and authenticated
- Python 3.10+
- LibreOffice (for PPTX -> image conversion)
- poppler (for PDF processing)

## Architecture
- `harness/` — Claude CLI adapter (replaces CAMEL framework)
- `PosterAgent/` — Main pipeline modules
- `utils/` — PPTX utilities, prompt templates, styling
- `config/` — Poster YAML configuration
- `assets/` — Training data for layout algorithm
