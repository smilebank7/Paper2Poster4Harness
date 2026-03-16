# 04 - Generate Poster Bullet Content

## Goal
Generate poster-ready title and bullet paragraphs for each section.

## Input
- One section from `raw_content.json`:
  - `title`
  - `content`
- `number_of_textboxes` for that section (1 or 2)

## Instructions
1. Summarize the section into concise, informative bullet points.
2. Preserve technical meaning (method names, metrics, key findings).
3. Use clear hierarchy with `level` (0 for primary, 1 for supporting details when needed).
4. Keep tone factual and compact for poster readability.
5. If `number_of_textboxes` is 2:
   - output both `textbox1` and `textbox2`
   - both arrays must have the same number of bullet items
6. Return valid JSON only.

## Required Bullet Object Schema
Each entry in `title`, `textbox1`, or `textbox2` must follow:
```json
{
  "alignment": "left",
  "bullet": true,
  "level": 0,
  "font_size": 30,
  "runs": [
    {
      "text": "Example bullet text",
      "bold": false,
      "italic": false
    }
  ]
}
```

## Required Output Schema
```json
{
  "title": [
    {
      "alignment": "left",
      "bullet": false,
      "level": 0,
      "font_size": 38,
      "runs": [
        {
          "text": "Section Title",
          "bold": true
        }
      ]
    }
  ],
  "textbox1": [
    {
      "alignment": "left",
      "bullet": true,
      "level": 0,
      "font_size": 30,
      "runs": [
        {
          "text": "Key point"
        }
      ]
    }
  ],
  "textbox2": [
    {
      "alignment": "left",
      "bullet": true,
      "level": 0,
      "font_size": 30,
      "runs": [
        {
          "text": "Companion point"
        }
      ]
    }
  ]
}
```

## Hard Constraints
- If one textbox: output keys `title`, `textbox1` only.
- If two textboxes: output keys `title`, `textbox1`, `textbox2` and equal item counts in both textboxes.
- Return JSON only.
