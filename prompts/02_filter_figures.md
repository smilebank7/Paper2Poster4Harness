# 02 - Filter Figures And Tables

## Goal
Select only figures/tables that are relevant to the planned poster sections.

## Input
- `json_content` (structured poster sections from `raw_content.json`)
- `image_information` (image metadata dict)
- `table_information` (table metadata dict)

## Instructions
1. Read all poster sections in `json_content` and identify key topics.
2. For each image/table entry, evaluate relevance using caption + context.
3. Keep entries that directly support section topics (method, architecture, dataset, results, ablation, qualitative examples, key tables).
4. Remove irrelevant, redundant, or weakly connected entries.
5. Prefer diversity across kept items (avoid near-duplicates).
6. Keep at most 7 total items, typically 5-7.
   - If enough strong candidates exist in both groups, cap each group at 5.
7. Output valid JSON only.

## Required Output Schema
```json
{
  "image_information": {
    "<id>": {
      "caption": "<caption>",
      "path": "<path>",
      "width": 0,
      "height": 0
    }
  },
  "table_information": {
    "<id>": {
      "caption": "<caption>",
      "path": "<path>",
      "width": 0,
      "height": 0
    }
  }
}
```

## Hard Constraints
- Keep exactly two top-level keys: `image_information`, `table_information`.
- Use empty objects when nothing is selected.
- Return JSON only.
