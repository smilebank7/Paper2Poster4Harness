# Paper2Poster4Harness

Generate academic posters from research papers. Drop a PDF in `input/`, tell me to make a poster.

## How It Works

This is a faithful adaptation of [Paper2Poster](https://github.com/Paper2Poster/Paper2Poster).
All AI calls are routed through `claude -p` CLI (your subscription, no API key needed).

The full original pipeline is preserved:
- **Tree-split layout** — learned from 60+ real poster examples
- **Overflow detection loop** — iterative content refinement (up to 10 rounds)
- **PPTX code generation** — AI writes python-pptx code directly
- **Theme & style** — automated color/font/border styling

## Quick Start

1. Place your paper PDF in `input/`
2. Tell me: "포스터 만들어줘" or "Generate a poster"

## What I Do

When you ask me to generate a poster, I run:

```bash
.venv/bin/python3 PosterAgent/new_pipeline.py \
    --paper_path input/{paper}.pdf \
    --poster_width_inches 48 \
    --poster_height_inches 36 \
    --tmp_dir workspace/tmp
```

This executes the full 6-stage pipeline:

1. **Parse** — Docling extracts text + figures from PDF
2. **Filter** — AI selects relevant figures/tables
3. **Outline & Layout** — AI plans sections → tree-split algorithm computes panel bounding boxes
4. **Content** — AI generates bullet points with overflow detection loop
5. **Style** — Theme, colors, fonts applied from config/poster.yaml
6. **Render** — AI generates python-pptx code → executes → PPTX + PNG

Each AI call goes through `harness/agent.py` → `claude -p` CLI → your Claude subscription.

## Output
- `<harness_harness>_generated_posters/{paper}/` — poster.pptx + slide images
- Or `output/{paper}/` if manually specified

## Prerequisites
- Python 3.10+ with: `pip install -r requirements.txt`
- Claude Code CLI (`claude`) or OpenCode CLI installed and authenticated
- LibreOffice (`soffice`) for PPTX → PNG conversion
