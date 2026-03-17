#!/usr/bin/env python3
"""
PaperBanana integration for Paper2Poster.
Generates academic diagrams for poster sections using Gemini free tier.
"""

import asyncio
import os
from PIL import Image


def select_sections_for_figures(raw_content_json, max_figures=3):
    """
    Heuristic: select which sections should get PaperBanana-generated figures.
    Skip title section (index 0) and conclusion-like sections.
    Pick sections with the most content (longest text = most material for diagrams).
    """
    sections = raw_content_json.get("sections", [])
    candidates = []

    skip_keywords = ["title", "author", "conclusion", "reference", "acknowledgment"]

    for i, section in enumerate(sections):
        title_lower = section.get("title", "").lower()
        if i == 0:  # skip poster title section
            continue
        if any(kw in title_lower for kw in skip_keywords):
            continue
        candidates.append((i, section))

    # Sort by content length (most content = most interesting for diagrams)
    candidates.sort(key=lambda x: len(x[1].get("content", "")), reverse=True)

    return candidates[:max_figures]


async def generate_figures_async(raw_content_json, output_dir, max_figures=3):
    """
    Generate academic diagrams for selected sections using PaperBanana + Gemini.

    Returns:
        dict mapping section_title -> {"image_path": str, "width": int, "height": int, ...}
    """
    try:
        import importlib

        paperbanana_module = importlib.import_module("paperbanana")
        config_module = importlib.import_module("paperbanana.core.config")
        PaperBananaPipeline = getattr(paperbanana_module, "PaperBananaPipeline")
        GenerationInput = getattr(paperbanana_module, "GenerationInput")
        DiagramType = getattr(paperbanana_module, "DiagramType")
        Settings = getattr(config_module, "Settings")
    except ImportError:
        print("⚠️  PaperBanana not installed. Run: pip install paperbanana[google]")
        print("   Skipping figure generation. Poster will be text-only.")
        return {}

    if not os.environ.get("GOOGLE_API_KEY"):
        print(
            "⚠️  GOOGLE_API_KEY not set. Get free key at https://makersuite.google.com/app/apikey"
        )
        print("   Skipping figure generation. Poster will be text-only.")
        return {}

    os.makedirs(output_dir, exist_ok=True)

    settings = Settings(
        vlm_provider="gemini",
        vlm_model="gemini-2.5-flash",
        image_provider="google_imagen",
        image_model="gemini-2.5-flash-image",
        refinement_iterations=1,
        output_dir=output_dir,
        output_format="png",
        num_retrieval_examples=3,
    )

    pipeline = PaperBananaPipeline(settings=settings)
    selected = select_sections_for_figures(raw_content_json, max_figures)

    results = {}

    for _, section in selected:
        title = section["title"]
        content = section["content"]

        print(f"🎨 Generating figure for section: {title}...")

        try:
            result = await pipeline.generate(
                GenerationInput(
                    source_context=content[:3000],  # Trim to avoid token limits
                    communicative_intent=f"Academic diagram illustrating: {title}",
                    diagram_type=DiagramType.METHODOLOGY,
                )
            )

            if result.image_path and os.path.exists(result.image_path):
                # Copy to our output directory with clean name
                import shutil

                clean_name = title.replace(" ", "_").replace("/", "_")[:30]
                dest_path = os.path.join(output_dir, f"paperbanana_{clean_name}.png")
                shutil.copy2(result.image_path, dest_path)

                img = Image.open(dest_path)
                results[title] = {
                    "image_path": dest_path,
                    "caption": f"Generated diagram for {title}",
                    "width": img.width,
                    "height": img.height,
                    "figure_size": img.width * img.height,
                    "figure_aspect": img.width / max(img.height, 1),
                }
                print(f"   ✅ Generated: {dest_path} ({img.width}x{img.height})")
            else:
                print(f"   ❌ No output for section: {title}")

        except Exception as e:
            print(f"   ❌ Error generating figure for '{title}': {e}")
            continue

    return results


def generate_figures(raw_content_json, output_dir, max_figures=3):
    """Synchronous wrapper for generate_figures_async."""
    return asyncio.run(
        generate_figures_async(raw_content_json, output_dir, max_figures)
    )


def inject_figures_into_pipeline(panels, figure_results, images_dict, tables_dict):
    """
    Inject PaperBanana-generated figures into the Paper2Poster pipeline data structures.

    Modifies `panels` in-place to add gp (graphic proportion) and figure_size.
    Returns `figures` dict mapping section_name -> figure assignment.

    Args:
        panels: list of panel dicts from gen_outline_layout_v2 (or built from raw_content)
        figure_results: dict from generate_figures() {section_title -> {image_path, ...}}
        images_dict: existing images dict from parse_raw
        tables_dict: existing tables dict from parse_raw

    Returns:
        figures: dict mapping section_name -> {"image": id, "reason": "..."}
    """
    del tables_dict
    figures = {}

    if not figure_results:
        return figures

    # Add PaperBanana figures to images_dict with high IDs to avoid conflicts
    pb_id_start = 900

    total_figure_area = sum(f.get("figure_size", 0) for f in figure_results.values())
    if total_figure_area == 0:
        total_figure_area = 1

    for i, (section_title, fig_info) in enumerate(figure_results.items()):
        img_id = str(pb_id_start + i)
        images_dict[img_id] = {
            "caption": fig_info.get("caption", ""),
            "image_path": fig_info["image_path"],
            "width": fig_info.get("width", 800),
            "height": fig_info.get("height", 600),
            "figure_size": fig_info.get("figure_size", 480000),
            "figure_aspect": fig_info.get("figure_aspect", 1.33),
        }

        # Create figure assignment
        figures[section_title] = {
            "image": img_id,
            "reason": f"PaperBanana-generated diagram for {section_title}",
        }

    # Update panels with graphic proportions
    for panel in panels:
        section_name = panel.get("section_name", "")
        if section_name in figure_results:
            fig_info = figure_results[section_name]
            panel["gp"] = fig_info.get("figure_size", 0) / total_figure_area
            panel["figure_size"] = fig_info.get("figure_size", 480000)
            panel["figure_aspect"] = fig_info.get("figure_aspect", 1.33)
        else:
            panel["gp"] = 0
            panel["figure_size"] = 0
            panel["figure_aspect"] = 1.0

    return figures
