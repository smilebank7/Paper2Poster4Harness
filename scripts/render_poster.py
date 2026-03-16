#!/usr/bin/env python3
"""
Render the final poster as PPTX + PNG.
This is a NON-AI task - uses python-pptx for generation.

Usage (called by Claude Code):
    python scripts/render_poster.py \
        workspace/paper_name/layout.json \
        workspace/paper_name/poster_content.json \
        --output output/paper_name/poster.pptx \
        --config config/poster.yaml

Output:
    output/paper_name/poster.pptx - Editable PowerPoint poster
    output/paper_name/poster.png  - Preview image (requires soffice)
"""

import argparse
import json
import os
import subprocess
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pptx_utils import (
    add_blank_slide,
    add_image,
    add_textbox,
    create_poster,
    fill_textframe,
    save_presentation,
    set_slide_background_color,
)


def render_poster(layout_path, content_path, output_pptx, config_path=None):
    """Render a poster from layout + content."""
    with open(layout_path, "r", encoding="utf-8") as f:
        layout = json.load(f)
    with open(content_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    # Load config
    config = {}
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    width = layout["poster_width_inches"]
    height = layout["poster_height_inches"]

    # Create presentation
    prs = create_poster(width_inch=width, height_inch=height)
    slide = add_blank_slide(prs)

    # Set background
    bg_color = config.get("background_color", [255, 255, 255])
    set_slide_background_color(slide, tuple(bg_color))

    # Place textboxes with content
    content_list = []
    for section in content:
        if "title" in section:
            content_list.append(section["title"])
        for key in ["textbox1", "textbox2"]:
            if key in section:
                content_list.append(section[key])

    for i, tb in enumerate(layout["textboxes"]):
        shape = add_textbox(
            slide,
            tb.get("textbox_name", f"tb_{i}"),
            tb["x"],
            tb["y"],
            tb["width"],
            tb["height"],
            text="",
            word_wrap=True,
            font_size=24,
        )
        if i < len(content_list):
            fill_textframe(shape, content_list[i])

    # Place figures
    for fig in layout["figures"]:
        fig_path = fig.get("figure_path")
        if fig_path and os.path.exists(fig_path):
            add_image(
                slide,
                fig.get("figure_name", "fig"),
                fig["x"],
                fig["y"],
                fig["width"],
                fig["height"],
                image_path=fig_path,
            )

    # Save PPTX
    os.makedirs(os.path.dirname(output_pptx), exist_ok=True)
    save_presentation(prs, output_pptx)
    print(f"Poster saved: {output_pptx}")

    # Convert to PNG
    output_dir = os.path.dirname(output_pptx)
    try:
        subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "png",
                "--outdir",
                output_dir,
                output_pptx,
            ],
            capture_output=True,
            timeout=60,
            check=False,
        )
        png_name = os.path.splitext(os.path.basename(output_pptx))[0] + ".png"
        png_path = os.path.join(output_dir, png_name)
        if os.path.exists(png_path):
            print(f"Preview saved: {png_path}")
        else:
            print(
                "Warning: PNG conversion failed. Install LibreOffice for image preview."
            )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("Warning: soffice not found. Install LibreOffice for PNG preview.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render poster from layout + content")
    parser.add_argument("layout", help="Path to layout.json")
    parser.add_argument("content", help="Path to poster_content.json")
    parser.add_argument("--output", required=True, help="Output PPTX path")
    parser.add_argument(
        "--config", default="config/poster.yaml", help="Poster config YAML"
    )
    args = parser.parse_args()

    render_poster(args.layout, args.content, args.output, args.config)
