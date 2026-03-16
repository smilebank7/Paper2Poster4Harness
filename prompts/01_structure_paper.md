# 01 - Structure Paper Into Poster JSON

## Goal
Convert full paper markdown into concise JSON for poster generation.

## Input
- Full paper markdown text from `workspace/{paper}/paper.md`

## Instructions
1. Read the full paper and identify its logical sections.
2. Remove noise: headers/footers, revision-marked deletions (`~~...~~`), HTML comments, reference-only boilerplate.
3. Extract paper metadata exactly (do not summarize title):
   - paper title
   - author list
   - affiliations
4. Build section list for poster flow:
   - first section must be a dedicated poster title section
   - remaining sections should cover core paper narrative (problem, method, results, discussion, conclusion)
5. For each non-title section:
   - keep raw technical wording where useful
   - remove inline citation markers like `[12]`, `(Smith et al., 2023)` when possible
   - target around 500 words per section when content allows
   - use short section titles (max 3 words)
6. Prioritize important sections with more content and minor sections with less.
7. Output valid JSON only.

## Required Output Schema
```json
{
  "meta": {
    "poster_title": "<raw paper title>",
    "authors": "<authors as a single string>",
    "affiliations": "<affiliations as a single string>"
  },
  "sections": [
    {
      "title": "Poster Title & Author",
      "content": "<title/author/affiliation text for poster header section>"
    },
    {
      "title": "<max 3 words>",
      "content": "<section content, typically near 500 words>"
    }
  ]
}
```

## Hard Constraints
- Include `meta` and `sections` keys.
- Include a dedicated poster title section as the first item in `sections`.
- Return JSON only, no markdown fences or extra commentary.
