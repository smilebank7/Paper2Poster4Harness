---
name: paper2poster
description: "Generate academic posters from research papers. Triggers: 'poster', 'make poster', '포스터', '포스터 만들어', 'generate poster', 'paper to poster', 'create poster from paper'"
---

# Paper2Poster Skill

## Trigger
User wants to generate a poster from a PDF paper.

## Prerequisites Check
Before starting, verify:
```bash
python -c "import docling; import pptx; import yaml; print('OK')"
```
If missing: `pip install -r requirements.txt`

## Workflow

### 1. Find the input PDF
Look in `input/` for PDF files. If multiple, ask the user which one.
```bash
ls input/*.pdf
```

### 2. Create workspace
```bash
PAPER_NAME=$(basename input/*.pdf .pdf | tr ' ' '_')
mkdir -p "workspace/${PAPER_NAME}"
```

### 3. Parse PDF (script)
```bash
python scripts/parse_pdf.py "input/${PAPER_NAME}.pdf" --output-dir "workspace/${PAPER_NAME}/"
```

### 4. Structure content (AI - you do this)
Read `workspace/${PAPER_NAME}/paper.md`
Follow the instructions in `prompts/01_structure_paper.md`
Write the result to `workspace/${PAPER_NAME}/raw_content.json`

### 5. Filter figures (AI - you do this)
Read `workspace/${PAPER_NAME}/image_metadata.json`
Follow `prompts/02_filter_figures.md`
Write to `workspace/${PAPER_NAME}/filtered_figures.json`

### 6. Plan figure assignment (AI - you do this)
Read raw_content.json + filtered_figures.json
Follow `prompts/03_plan_sections.md`
Write to `workspace/${PAPER_NAME}/figure_plan.json`

### 7. Generate layout (script)
```bash
python scripts/generate_layout.py \
    "workspace/${PAPER_NAME}/raw_content.json" \
    "workspace/${PAPER_NAME}/figure_plan.json" \
    --width 48 --height 36 \
    --output "workspace/${PAPER_NAME}/layout.json"
```

### 8. Generate poster content (AI - you do this)
Read raw_content.json + layout.json
Follow `prompts/04_generate_bullets.md` for each section
Follow `prompts/05_generate_title.md` for the title
Combine into `workspace/${PAPER_NAME}/poster_content.json`

### 9. Render poster (script)
```bash
python scripts/render_poster.py \
    "workspace/${PAPER_NAME}/layout.json" \
    "workspace/${PAPER_NAME}/poster_content.json" \
    --output "output/${PAPER_NAME}/poster.pptx" \
    --config config/poster.yaml
```

### 10. Done!
Tell the user:
- Poster saved at `output/${PAPER_NAME}/poster.pptx`
- Preview at `output/${PAPER_NAME}/poster.png` (if soffice available)
