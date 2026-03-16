# 03 - Plan Section To Figure Assignment

## Goal
Assign at most one figure or one table to each section.

## Input
- `json_content` from `raw_content.json`
- filtered `image_information`
- filtered `table_information`

## Instructions
1. Read section titles and section content themes.
2. For each section, choose the single best supporting visual:
   - either one image
   - or one table
   - or none
3. Match by semantic relevance between section content and caption.
4. Do not reuse the same image/table across multiple sections.
5. Skip sections with no strong visual match.
6. Include a brief reason for each assignment.
7. Output valid JSON only.

## Required Output Schema
```json
{
  "<section title>": {
    "type": "image",
    "id": "<image id>",
    "image_path": "<path>",
    "caption": "<caption>",
    "reason": "<why this visual fits this section>"
  },
  "<another section title>": {
    "type": "table",
    "id": "<table id>",
    "image_path": "<path>",
    "caption": "<caption>",
    "reason": "<why this table fits this section>"
  }
}
```

## Hard Constraints
- Include only sections that receive an assignment.
- Use `image_path` key for both figures and tables so downstream scripts can consume uniformly.
- No visual asset can be assigned more than once.
- Return JSON only.
