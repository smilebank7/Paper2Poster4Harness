# 05 - Generate Poster Title Block

## Goal
Format paper title, authors, and affiliations into poster title JSON.

## Input
- A `title_string` containing paper title + author/affiliation information.

## Instructions
1. Extract paper title, authors, and affiliations.
2. Keep title faithful to source text.
3. Format authors in one centered line, with superscript numerals linking affiliations.
4. Format affiliations in centered line(s) with matching numerals.
5. Return valid JSON only.

## Required Output Schema
```json
{
  "title": [
    {
      "alignment": "center",
      "bullet": false,
      "level": 0,
      "font_size": 72,
      "runs": [
        {
          "text": "Full Paper Title",
          "bold": true
        }
      ]
    }
  ],
  "textbox1": [
    {
      "alignment": "center",
      "bullet": false,
      "level": 0,
      "font_size": 36,
      "runs": [
        {
          "text": "Author A1, Author B2, Author C1"
        }
      ]
    },
    {
      "alignment": "center",
      "bullet": false,
      "level": 0,
      "font_size": 32,
      "runs": [
        {
          "text": "1 Institution One; 2 Institution Two"
        }
      ]
    }
  ]
}
```

## Hard Constraints
- Top-level keys must be exactly `title` and `textbox1`.
- `title` must contain exactly one item.
- Return JSON only.
