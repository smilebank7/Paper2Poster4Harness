#!/usr/bin/env python3
"""
Parse a PDF paper into markdown text + extracted figures/tables.
This is a NON-AI task - uses Docling for document conversion.

Usage (called by Claude Code):
    python scripts/parse_pdf.py input/paper.pdf --output-dir workspace/paper_name/

Output:
    workspace/paper_name/paper.md            - Full paper as markdown
    workspace/paper_name/images/             - Extracted figure/table PNGs
    workspace/paper_name/image_metadata.json - Image captions and dimensions
"""

import argparse
import json
import os
import re
import sys


def parse_pdf(pdf_path, output_dir):
    """Parse PDF using Docling, extract text and images."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)

    try:
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling_core.types.doc import PictureItem, TableItem
    except ImportError:
        print("ERROR: docling not installed. Run: pip install docling docling_core")
        sys.exit(1)

    # Configure Docling
    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = 5.0
    pipeline_options.generate_page_images = True
    pipeline_options.generate_picture_images = True

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    print(f"Parsing PDF: {pdf_path}")
    result = converter.convert(pdf_path)

    # Export markdown
    markdown = result.document.export_to_markdown()
    markdown = re.sub(r"<!--[\s\S]*?-->", "", markdown)

    md_path = f"{output_dir}/paper.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Saved markdown: {md_path} ({len(markdown)} chars)")

    # Extract and save images
    image_metadata = {"images": {}, "tables": {}}

    picture_idx = 0
    for element, _level in result.document.iterate_items():
        if isinstance(element, PictureItem):
            picture_idx += 1
            img_path = f"{output_dir}/images/figure_{picture_idx}.png"
            caption = element.caption_text(result.document)
            pil_img = element.get_image(result.document)
            if pil_img:
                pil_img.save(img_path, "PNG")
                image_metadata["images"][str(picture_idx)] = {
                    "caption": caption,
                    "path": img_path,
                    "width": pil_img.width,
                    "height": pil_img.height,
                }
                print(f"  Figure {picture_idx}: {caption[:60]}...")

    table_idx = 0
    for element, _level in result.document.iterate_items():
        if isinstance(element, TableItem):
            table_idx += 1
            img_path = f"{output_dir}/images/table_{table_idx}.png"
            caption = element.caption_text(result.document)
            pil_img = element.get_image(result.document)
            if pil_img:
                pil_img.save(img_path, "PNG")
                image_metadata["tables"][str(table_idx)] = {
                    "caption": caption,
                    "path": img_path,
                    "width": pil_img.width,
                    "height": pil_img.height,
                }
                print(f"  Table {table_idx}: {caption[:60]}...")

    meta_path = f"{output_dir}/image_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(image_metadata, f, indent=2)
    print(f"Saved metadata: {meta_path}")
    print(f"Done! {picture_idx} figures, {table_idx} tables extracted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse PDF paper into markdown + images")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--output-dir", required=True, help="Output directory for workspace")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print(f"ERROR: PDF not found: {args.pdf_path}")
        sys.exit(1)

    parse_pdf(args.pdf_path, args.output_dir)
