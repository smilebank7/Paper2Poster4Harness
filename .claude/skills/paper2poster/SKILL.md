---
name: paper2poster
description: "Generate academic posters from research papers. Triggers: 'poster', 'make poster', '포스터', '포스터 만들어', 'generate poster', 'paper to poster'"
---

# Paper2Poster Skill

## Trigger
User wants to generate a poster from a PDF paper in `input/`.

## Prerequisites
```bash
# Check dependencies
.venv/bin/python3 -c "import docling; import pptx; import yaml; print('OK')"
which claude
```

## Workflow

### 1. Find the input PDF
```bash
ls input/*.pdf
```
If multiple PDFs, ask user which one.

### 2. Run the full pipeline
```bash
PAPER_PATH=$(ls input/*.pdf | head -1)
.venv/bin/python3 PosterAgent/new_pipeline.py \
    --paper_path "$PAPER_PATH" \
    --poster_width_inches 48 \
    --poster_height_inches 36 \
    --tmp_dir workspace/tmp
```

### 3. Report results
The poster is saved to `<harness_harness>_generated_posters/` directory.
Tell the user where to find the PPTX and preview images.

## Notes
- Pipeline takes 10-30 minutes (many AI calls via claude -p)
- Each AI call goes through Claude CLI subscription (no API key)
- Tree-split layout uses learned model from 60+ real poster examples
- Overflow detection runs up to 10 refinement rounds
- For custom poster size: adjust `--poster_width_inches` and `--poster_height_inches`
