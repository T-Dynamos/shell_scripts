#!/usr/bin/env python3
"""
td_script_data.common - Shared core utilities for T-Dynamos shell_scripts.
Provides terminal formatting, data size/time formatting, hardware sysfs helpers,
and path discovery.
"""

import os
import re
import sys
import glob
from pathlib import Path
from datetime import timedelta
from typing import Any

DEFAULT_POWER_SUPPLY_DIR = "/sys/class/power_supply"


def get_data_dir() -> Path:
    """Return the absolute Path to the td_script_data directory."""
    # 1. Directory of this file
    this_dir = Path(__file__).resolve().parent
    if this_dir.is_dir() and this_dir.name == "td_script_data":
        return this_dir

    # 2. Check relative to executing script
    main_file = sys.argv[0] if sys.argv and sys.argv[0] else __file__
    cand = Path(main_file).resolve().parent / "td_script_data"
    if cand.is_dir():
        return cand

    # 3. Check ~/.local/bin/td_script_data
    user_cand = Path.home() / ".local" / "bin" / "td_script_data"
    if user_cand.is_dir():
        return user_cand

    return this_dir


def get_data_file(relative_name: str) -> Path:
    """Return the Path to a file or directory located inside td_script_data."""
    return get_data_dir() / relative_name


# ---------------------------------------------------------------------------
# Terminal Colors & Styling
# ---------------------------------------------------------------------------


class Colors:
    """ANSI terminal escape color codes."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Standard colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bold colors
    BOLD_RED = "\033[1;31m"
    BOLD_GREEN = "\033[1;32m"
    BOLD_YELLOW = "\033[1;33m"
    BOLD_BLUE = "\033[1;34m"
    BOLD_MAGENTA = "\033[1;35m"
    BOLD_CYAN = "\033[1;36m"
    BOLD_WHITE = "\033[1;37m"


def supports_color(no_color_flag: bool = False) -> bool:
    """Check if stdout supports ANSI color output and no suppression flags are set."""
    if no_color_flag:
        return False
    if os.environ.get("NO_COLOR") is not None:
        return False
    return sys.stdout.isatty()


def colorize(text: str, color_code: str, enabled: bool = True) -> str:
    """Wrap text in an ANSI color code if enabled is True."""
    if not enabled:
        return text
    return f"{color_code}{text}{Colors.RESET}"


# ---------------------------------------------------------------------------
# Data Size & Time Formatters
# ---------------------------------------------------------------------------


def format_bytes(bytes_count: int | float | None) -> str:
    """Format byte count into human-readable unit (B, KB, MB, GB, TB)."""
    if bytes_count is None or bytes_count < 0:
        return "N/A"
    b = float(bytes_count)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024.0 or unit == "TB":
            return f"{b:.1f} {unit}" if unit in ["MB", "GB", "TB"] else f"{int(round(b))} {unit}"
        b /= 1024.0
    return f"{b:.1f} MB"


def format_size(bytes_num: int | float | None) -> str:
    """Alias for format_bytes."""
    return format_bytes(bytes_num)


def format_time(sec: float | None) -> str:
    """Format seconds into readable duration (e.g. '2h 15m' or '45s')."""
    if sec is None or sec < 0 or sec > 86400 * 365:
        return "N/A"
    total_sec = int(round(sec))
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    if h > 0:
        return f"{h}h {m:02d}m"
    if m > 0:
        return f"{m}m {s:02d}s"
    return f"{s}s"


def format_span(td: timedelta | float | int | None) -> str:
    """Format a timedelta or second duration into human-readable span."""
    if td is None:
        return "N/A"
    if isinstance(td, (int, float)):
        total_sec = int(td)
    else:
        total_sec = int(td.total_seconds())

    if total_sec < 60:
        return f"{total_sec}s"
    minutes = total_sec // 60
    if minutes < 60:
        rem_sec = total_sec % 60
        return f"{minutes}m {rem_sec}s" if rem_sec else f"{minutes}m"
    hours = minutes // 60
    rem_min = minutes % 60
    if hours < 24:
        return f"{hours}h {rem_min}m" if rem_min else f"{hours}h"
    days = hours // 24
    rem_hours = hours % 24
    return f"{days}d {rem_hours}h" if rem_hours else f"{days}d"


def parse_duration(s: str) -> float:
    """Parse a duration string like '30m', '2h', '1d', '60s' into seconds."""
    match = re.match(r"^(\d+(?:\.\d+)?)\s*([smhd]?)$", s.strip().lower())
    if not match:
        raise ValueError(f"Invalid duration format: '{s}'. Use e.g. '30m', '2h', '1d', '60s'.")
    val, unit = match.groups()
    multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}.get(unit or "s", 1)
    return float(val) * multiplier


# ---------------------------------------------------------------------------
# Progress Bar Renderers
# ---------------------------------------------------------------------------


def make_bar(ratio: float, width: int = 15) -> str:
    """Render a horizontal progress bar using Unicode block characters (ratio: 0.0 to 1.0)."""
    clamped = max(0.0, min(1.0, float(ratio)))
    filled = int(round(clamped * width))
    empty = width - filled
    return "█" * filled + "░" * empty


def make_progress_bar(percent: float, width: int = 20, use_color: bool = True) -> str:
    """Generate a visual text progress bar for battery or percentage metrics."""
    clamped = max(0.0, min(100.0, float(percent)))
    filled_len = int(round(width * clamped / 100.0))
    empty_len = width - filled_len
    bar_chars = "█" * filled_len + "░" * empty_len

    if not use_color:
        return f"[{bar_chars}]"

    if clamped >= 50.0:
        color = Colors.GREEN
    elif clamped >= 20.0:
        color = Colors.YELLOW
    else:
        color = Colors.RED

    return f"[{color}{bar_chars}{Colors.RESET}]"


# ---------------------------------------------------------------------------
# Hardware & Sysfs Helpers
# ---------------------------------------------------------------------------


def find_batteries(power_supply_dir: str = DEFAULT_POWER_SUPPLY_DIR) -> list[str]:
    """Find all battery device names available in sysfs."""
    paths = glob.glob(os.path.join(power_supply_dir, "BAT*"))
    if not paths:
        # Fallback search for any power supply of type Battery
        for p in glob.glob(os.path.join(power_supply_dir, "*")):
            type_file = os.path.join(p, "type")
            if os.path.isfile(type_file):
                try:
                    with open(type_file) as f:
                        if f.read().strip().lower() == "battery":
                            paths.append(p)
                except OSError:
                    pass
    return sorted([os.path.basename(p) for p in paths])


def read_sysfs_int(path: Path | str) -> int | None:
    """Read an integer value from a sysfs file, or None if unavailable."""
    p = Path(path)
    if not p.is_file():
        return None
    try:
        return int(p.read_text().strip())
    except (ValueError, OSError):
        return None


def read_sysfs_str(path: Path | str) -> str | None:
    """Read a string value from a sysfs file, or None if unavailable."""
    p = Path(path)
    if not p.is_file():
        return None
    try:
        return p.read_text().strip()
    except OSError:
        return None
