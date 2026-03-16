# Paper2Poster4Harness

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Backend](https://img.shields.io/badge/AI-Claude%20CLI-green.svg)](https://github.com/anthropics/claude-code)

Generate academic posters from papers using Claude Code — no API keys needed.

## What This Repo Changes

This repository adapts the original Paper2Poster pipeline to run all AI calls through local Claude CLI (`claude -p`) instead of CAMEL + OpenAI APIs.

- Replaces `ChatAgent`/`ModelFactory` calls with `HarnessAgent` (`harness/agent.py`)
- Removes CAMEL/OpenAI/vLLM from runtime dependencies
- Replaces vision-model overflow critic with heuristic overflow detection (`harness/vision.py`)
- Keeps deterministic layout and PPTX generation flow from the original project

## Prerequisites

- Python 3.10+
- Claude Code CLI (`claude`) or OpenCode CLI installed and authenticated
- LibreOffice (`soffice`) for PPTX -> image conversion
- poppler for PDF/image processing

## Installation

```bash
git clone <your-repo-url>
cd Paper2Poster4Harness
pip install -r requirements.txt
```

Verify Claude CLI:

```bash
which claude
```

## Usage

Place a paper as:

```text
data/{paper_name}/paper.pdf
```

Run:

```bash
python run.py --paper_path data/my_paper/paper.pdf
```

Custom poster size:

```bash
python run.py \
  --paper_path data/my_paper/paper.pdf \
  --poster_width_inches 48 \
  --poster_height_inches 36
```

Add conference logo search hint:

```bash
python run.py --paper_path data/my_paper/paper.pdf --conference_venue "NeurIPS"
```

## Output

Generated assets are saved under:

```text
<{model_t}_{model_v}>_generated_posters/data/{paper_name}/
```

Typical files:

- `{paper_name}.pptx`
- `slide_0001.jpg`
- `log.json`

## Pipeline Architecture

```text
PDF paper
  |
  v
[1] Parse (Docling -> markdown -> Claude JSON sections)
  |
  v
[2] Filter figures/tables (Claude)
  |
  v
[3] Plan sections + figure assignment (Claude)
  |
  v
[4] Layout (deterministic tree split, no AI)
  |
  v
[5] Generate content (Claude) + heuristic overflow checks
  |
  v
[6] Render poster (python-pptx)
```

## Claude Code Skill

This repo includes a local skill at:

- `.claude/skills/paper2poster/SKILL.md`

It provides a ready workflow for running poster generation inside Claude Code/OpenCode.

## Attribution

This project is based on the original Paper2Poster implementation:

- https://github.com/Paper2Poster/Paper2Poster

Credit for the base architecture, prompts, and layout approach belongs to the original authors.

## License

This repository is distributed under the MIT License. See `LICENSE`.
