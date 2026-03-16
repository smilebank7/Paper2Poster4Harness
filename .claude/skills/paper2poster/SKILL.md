---
name: paper2poster
description: Generate academic posters from research papers. Use when user wants to create a poster from a PDF paper. Trigger phrases: "generate poster", "create poster", "paper to poster", "make poster", "poster from paper".
---

# Paper2Poster Skill

## When to Use
- User wants to create an academic poster from a research paper (PDF)
- User mentions "poster", "paper2poster", "generate poster"

## Steps

### 1. Verify Setup
```bash
# Check claude CLI
which claude

# Check Python deps
python -c "import pptx; import docling; print('Dependencies OK')"
```

### 2. Prepare Input
Ensure the paper PDF is placed in the correct structure:
```
data/{paper_name}/paper.pdf
```

### 3. Run Pipeline
```bash
python run.py \
    --paper_path "data/{paper_name}/paper.pdf" \
    --poster_width_inches 48 \
    --poster_height_inches 36
```

### 4. Output
The poster will be saved as:
- `harness_generated_posters/data/{paper_name}/poster.pptx`
- `harness_generated_posters/data/{paper_name}/slide_0001.jpg`

### Notes
- No API keys needed — uses Claude Code subscription
- Pipeline takes 5-15 minutes depending on paper length
- Can customize styling via `config/poster.yaml`
- For conference logos: add `--conference_venue "NeurIPS"`
