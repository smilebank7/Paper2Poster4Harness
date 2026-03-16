# Paper2Poster4Harness

Generate academic posters from research papers. Drop a PDF in `input/`, tell me to make a poster.

## How It Works

When you ask me to generate a poster, I follow this pipeline:

1. **Parse** - Extract text and figures from the PDF
2. **Structure** - Organize paper content into poster sections
3. **Filter** - Select the most relevant figures/tables
4. **Plan** - Assign figures to sections
5. **Layout** - Generate spatial layout (deterministic algorithm)
6. **Content** - Write bullet-point text for each section
7. **Render** - Generate the final poster (PPTX + PNG)

## Quick Start

1. Place your paper PDF in `input/`
2. Tell me: "포스터 만들어줘" or "Generate a poster from the paper in input/"

## Pipeline Details

### Step 1: Parse PDF
I run the parsing script to extract text and images:
```bash
python scripts/parse_pdf.py input/{paper}.pdf --output-dir workspace/{paper}/
```
This produces: `workspace/{paper}/paper.md` + `workspace/{paper}/images/`

### Step 2: Structure Content
I read `workspace/{paper}/paper.md` and follow `prompts/01_structure_paper.md` to create:
`workspace/{paper}/raw_content.json`

### Step 3: Filter Figures
I read `workspace/{paper}/image_metadata.json` and follow `prompts/02_filter_figures.md` to create:
`workspace/{paper}/filtered_figures.json`

### Step 4: Plan Section-Figure Assignment
I follow `prompts/03_plan_sections.md` to assign figures to sections:
`workspace/{paper}/figure_plan.json`

### Step 5: Generate Layout
I run the layout algorithm:
```bash
python scripts/generate_layout.py workspace/{paper}/raw_content.json workspace/{paper}/figure_plan.json --output workspace/{paper}/layout.json
```

### Step 6: Generate Content
I follow `prompts/04_generate_bullets.md` and `prompts/05_generate_title.md` to create:
`workspace/{paper}/poster_content.json`

### Step 7: Render Poster
```bash
python scripts/render_poster.py workspace/{paper}/layout.json workspace/{paper}/poster_content.json --output output/{paper}/poster.pptx --config config/poster.yaml
```

## Output
- `output/{paper}/poster.pptx` - Editable PowerPoint poster
- `output/{paper}/poster.png` - Preview image

## Prerequisites
- Python 3.10+ with: `pip install -r requirements.txt`
- LibreOffice (`soffice`) for PNG conversion
