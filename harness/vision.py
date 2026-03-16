def heuristic_overflow_check(
    text_content, width_inches, height_inches, font_size_pt=24
):
    width_pt = width_inches * 72
    height_pt = height_inches * 72
    avg_char_width = 0.5 * font_size_pt
    line_spacing = 1.5 * font_size_pt

    chars_per_line = max(1, int(width_pt // avg_char_width))
    max_lines = max(1, int(height_pt // line_spacing))
    capacity = chars_per_line * max_lines

    if isinstance(text_content, list):
        total_len = sum(
            sum(len(run.get("text", "")) for run in item.get("runs", []))
            for item in text_content
        )
    elif isinstance(text_content, str):
        total_len = len(text_content)
    else:
        total_len = 0

    ratio = total_len / max(capacity, 1)

    if ratio > 1.15:
        return "1"
    if ratio < 0.3:
        return "2"
    return "3"
