#!/usr/bin/env python3
"""
td_script_data.exif - Shared photographic EXIF extraction and formatting utilities.
Used by td_astro_stack and td_exif_summary.
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

# Supported photographic and RAW image formats
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".png",
    ".webp",
    ".dng",
    ".cr2",
    ".cr3",
    ".nef",
    ".arw",
    ".raw",
    ".orf",
    ".rw2",
    ".pef",
    ".raf",
}

RAW_EXTENSIONS = {
    ".dng",
    ".cr2",
    ".cr3",
    ".nef",
    ".arw",
    ".orf",
    ".rw2",
    ".pef",
    ".raf",
}

# Optional Pillow import for fallback EXIF reading
try:
    from PIL import Image, ExifTags
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


def parse_shutter_seconds(val: Any) -> float | None:
    """Parse shutter speed string or fraction (e.g. '1/50', '32', '1/32s') into float seconds."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val) if val > 0 else None
    s = str(val).strip().rstrip("s")
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 2:
            try:
                num = float(parts[0])
                denom = float(parts[1])
                return (num / denom) if denom != 0 else None
            except ValueError:
                return None
    try:
        f = float(s)
        return f if f > 0 else None
    except ValueError:
        return None


def format_shutter(sec: float | None, orig_str: str | None = None) -> str:
    """Format exposure time in seconds to human readable string (e.g. 32s, 1/50s)."""
    if sec is None:
        if orig_str:
            s = str(orig_str).strip()
            return f"{s}s" if not s.endswith("s") else s
        return "Unknown"
    if sec < 0.3:
        denom = round(1.0 / sec)
        return f"1/{denom}s"
    elif sec == int(sec):
        return f"{int(sec)}s"
    else:
        return f"{sec:.1f}s"


def format_aperture(fnum: float | None) -> str:
    """Format f-number to standard notation (e.g. f/2.8, f/8.0)."""
    if fnum is None or fnum <= 0:
        return "N/A"
    return f"f/{fnum:.1f}" if fnum % 1 != 0 else f"f/{int(fnum)}"


def format_focal(focal: float | None, focal_35mm: int | float | None = None) -> str:
    """Format focal length (e.g. 70mm or 70mm (105mm eq))."""
    if focal is None or focal <= 0:
        return "N/A"
    base = f"{focal:.1f}mm" if (focal % 1 != 0 and focal < 10) else f"{int(round(focal))}mm"
    if focal_35mm and float(focal_35mm) > 0 and abs(float(focal_35mm) - focal) > 1:
        eq_val = int(round(float(focal_35mm)))
        return f"{base} ({eq_val}mm)"
    return base


def format_ev(ev: Any) -> str:
    """Format exposure bias value in EV (e.g. 0.0, -0.7, +1.3)."""
    if ev is None:
        return "0.0"
    if isinstance(ev, (int, float)):
        sign = "+" if ev > 0 else ""
        return f"{sign}{ev:.1f}"
    s = str(ev).strip()
    if s in ["0", "0.0", "0/1", "+0"]:
        return "0.0"
    if "/" in s:
        try:
            parts = s.split("/")
            val = float(parts[0]) / float(parts[1])
            sign = "+" if val > 0 else ""
            return f"{sign}{val:.1f}"
        except Exception:
            return s
    try:
        f = float(s)
        sign = "+" if f > 0 else ""
        return f"{sign}{f:.1f}"
    except Exception:
        return s


def extract_metadata_exiftool(
    file_paths: list[str],
    tags: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Extract EXIF tags using exiftool command line utility."""
    exiftool_bin = shutil.which("exiftool")
    if not exiftool_bin or not file_paths:
        return []

    default_tags = [
        "-SourceFile",
        "-ExposureTime",
        "-ISO",
        "-FNumber",
        "-Model",
        "-DateTimeOriginal",
    ]
    tag_args = [f"-{t.lstrip('-')}" for t in tags] if tags else default_tags

    cmd = [exiftool_bin, "-json", "-n", "-q", "-q"] + tag_args + file_paths

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return json.loads(res.stdout)
    except Exception:
        return []


def extract_metadata_fallback(file_paths: list[str]) -> list[dict[str, Any]]:
    """Extract basic photographic metadata using Pillow if exiftool is unavailable."""
    records = []
    for fp in file_paths:
        rec: dict[str, Any] = {
            "SourceFile": fp,
            "ExposureTime": None,
            "ISO": None,
            "FNumber": None,
            "Model": None,
            "DateTimeOriginal": None,
        }
        if HAS_PILLOW:
            try:
                with Image.open(fp) as img:
                    exif_data = img._getexif() if hasattr(img, "_getexif") else None
                    if exif_data:
                        for tag_id, val in exif_data.items():
                            tag = ExifTags.TAGS.get(tag_id, tag_id)
                            if tag == "ExposureTime":
                                rec["ExposureTime"] = parse_shutter_seconds(val)
                            elif tag == "ISOSpeedRatings":
                                rec["ISO"] = int(val) if isinstance(val, (int, float)) else None
                            elif tag == "FNumber":
                                rec["FNumber"] = float(val) if isinstance(val, (int, float)) else None
                            elif tag == "Model":
                                rec["Model"] = str(val).strip()
                            elif tag == "DateTimeOriginal":
                                rec["DateTimeOriginal"] = str(val).strip()
            except Exception:
                pass
        records.append(rec)
    return records
