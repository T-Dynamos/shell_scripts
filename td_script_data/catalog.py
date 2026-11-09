#!/usr/bin/env python3
"""
td_script_data.catalog - Central registry of all T-Dynamos (td_*) shell scripts.
Provides descriptions, categories, command examples, and metadata.
"""

SCRIPTS = {
    "td_math2img": {
        "title": "LaTeX Math to Image (PNG/SVG) & Clipboard",
        "summary": "Render LaTeX math expressions to high-res images (PNG/SVG), copy to Wayland clipboard with wl-copy, and preview in swayimg.",
        "example": "td_math2img --save formula.png '\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}'",
        "category": "Graphics & Math",
    },
    "td_battery_info": {
        "title": "Battery Diagnostics & Health",
        "summary": "Display battery health percentage, full/design capacity in mAh, and CC phase charging current estimate.",
        "example": "td_battery_info --short",
        "category": "System & Hardware",
    },
    "td_battery_watch": {
        "title": "Live Terminal Battery Monitor",
        "summary": "Real-time dashboard tracking battery charge, charge/discharge rate in mA/W, progress bar, and time remaining.",
        "example": "td_battery_watch -i 1.0",
        "category": "System & Hardware",
    },
    "td_tmp_clean": {
        "title": "Temp Image Cleaner",
        "summary": "Clean temporary images and math renders from /tmp with dry-run and age filters.",
        "example": "td_tmp_clean --dry-run",
        "category": "Maintenance & Cleanup",
    },
    "td_script_info": {
        "title": "Scripts Catalog & Quick Help",
        "summary": "Summarize all td_* scripts with one-line descriptions, categories, and command examples.",
        "example": "td_script_info",
        "category": "Meta & Help",
    },
    "td_fish_completions": {
        "title": "Fish Shell Completions Generator",
        "summary": "Dynamically inspect, generate, and install smart Fish shell completions for all td_* scripts.",
        "example": "td_fish_completions",
        "category": "Shell & Completion",
    },
    "td_exif_summary": {
        "title": "Photo EXIF Scanner & Statistics",
        "summary": "Scan images and summarize photographic EXIF metadata (ISO, Shutter, Aperture, Lenses, Camera models).",
        "example": "td_exif_summary -r /path/to/photos",
        "category": "Photography & Media",
    },
    "td_astro_stack": {
        "title": "Astrophotography RAW & Image Stacker",
        "summary": "Stack photos with sub-pixel star alignment (Astroalign / Homography) and ISO normalization to reduce noise.",
        "example": "td_astro_stack -s 32s --crop --preview",
        "category": "Photography & Media",
    },
    "td_template": {
        "title": "Starter Skeleton Template",
        "summary": "Starter template with argparse, colors, JSON output, and error handling for creating new td_* scripts.",
        "example": "td_template 'hello world' --json",
        "category": "Meta & Template",
    },
}


def get_script_catalog() -> dict[str, dict[str, str]]:
    """Return a dictionary of all registered scripts and their metadata."""
    return SCRIPTS.copy()


def get_script_info(name: str) -> dict[str, str] | None:
    """Return metadata for a specific script name, or None if not found."""
    clean = name.strip()
    if clean in SCRIPTS:
        return SCRIPTS[clean]
    if not clean.startswith("td_") and f"td_{clean}" in SCRIPTS:
        return SCRIPTS[f"td_{clean}"]
    return None
