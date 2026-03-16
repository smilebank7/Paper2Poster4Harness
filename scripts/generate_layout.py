#!/usr/bin/env python3
"""
Generate poster layout using tree-split algorithm.
This is a NON-AI task - pure math/algorithm.

Usage (called by Claude Code):
    python scripts/generate_layout.py \
        workspace/paper_name/raw_content.json \
        workspace/paper_name/figure_plan.json \
        --width 48 --height 36 \
        --output workspace/paper_name/layout.json

Output:
    workspace/paper_name/layout.json - Panel/textbox/figure bounding boxes in inches
"""

import argparse
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PosterAgent.tree_split_layout import (
    get_arrangments_in_inches,
    main_inference,
    main_train,
)


def generate_layout(raw_content_path, figure_plan_path, width, height, output_path):
    """Generate layout from structured content and figure assignments."""

    with open(raw_content_path, "r", encoding="utf-8") as f:
        raw_content = json.load(f)
    with open(figure_plan_path, "r", encoding="utf-8") as f:
        figure_plan = json.load(f)

    # Build paper_panels from raw_content + figure_plan
    total_length = sum(len(s.get("content", "")) for s in raw_content.get("sections", []))

    # Compute figure areas
    all_figure_areas = {}
    for section_name, info in figure_plan.items():
        if isinstance(info, dict) and "image_path" in info:
            from PIL import Image

            img = Image.open(info["image_path"])
            all_figure_areas[section_name] = img.width * img.height

    total_figure_area = sum(all_figure_areas.values()) if all_figure_areas else 1

    paper_panels = []
    for i, section in enumerate(raw_content.get("sections", [])):
        title = section.get("title", f"Section {i + 1}")
        content = section.get("content", "")
        panel = {
            "panel_id": i,
            "section_name": title,
            "tp": len(content) / max(total_length, 1),
            "text_len": len(content),
            "gp": all_figure_areas.get(title, 0) / max(total_figure_area, 1),
            "figure_size": all_figure_areas.get(title, 0),
            "figure_aspect": 1.0,
        }

        # Get aspect ratio from figure_plan
        if title in figure_plan and "image_path" in figure_plan[title]:
            from PIL import Image

            img = Image.open(figure_plan[title]["image_path"])
            panel["figure_aspect"] = img.width / img.height if img.height > 0 else 1.0

        paper_panels.append(panel)

    # Train layout model from poster dataset
    print("Training layout model from poster dataset...")
    panel_model, figure_model = main_train()

    # Convert poster dimensions to layout units (72 units per inch)
    poster_w = width * 72
    poster_h = height * 72

    # Generate layout
    print("Generating layout...")
    panels, figures, textboxes = main_inference(
        paper_panels,
        panel_model,
        figure_model,
        poster_width=poster_w,
        poster_height=poster_h,
        shrink_margin=3,
    )

    # Convert to inches
    w_inch, h_inch, panels_inch, figures_inch, textboxes_inch = get_arrangments_in_inches(
        poster_w, poster_h, panels, figures, textboxes
    )

    # Assign figure paths from figure_plan
    for fig in figures_inch:
        panel_id = fig["panel_id"]
        section_name = raw_content["sections"][panel_id]["title"]
        if section_name in figure_plan and "image_path" in figure_plan[section_name]:
            fig["figure_path"] = figure_plan[section_name]["image_path"]

    # Compute num_chars for each textbox
    char_width_px = 7
    for tb in textboxes_inch:
        width_px = tb["width"] * 72
        height_px = tb["height"] * 72
        line_height = 16
        chars_per_line = max(int(width_px / char_width_px), 1)
        num_lines = max(int(height_px / line_height), 1)
        tb["num_chars"] = chars_per_line * num_lines

    layout = {
        "poster_width_inches": w_inch,
        "poster_height_inches": h_inch,
        "panels": panels_inch,
        "figures": figures_inch,
        "textboxes": textboxes_inch,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(layout, f, indent=2)

    print(f"Layout saved: {output_path}")
    print(
        f"  {len(panels_inch)} panels, {len(figures_inch)} figures, {len(textboxes_inch)} textboxes"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate poster layout")
    parser.add_argument("raw_content", help="Path to raw_content.json")
    parser.add_argument("figure_plan", help="Path to figure_plan.json")
    parser.add_argument("--width", type=float, default=48, help="Poster width in inches")
    parser.add_argument("--height", type=float, default=36, help="Poster height in inches")
    parser.add_argument("--output", required=True, help="Output layout.json path")
    args = parser.parse_args()

    generate_layout(args.raw_content, args.figure_plan, args.width, args.height, args.output)
