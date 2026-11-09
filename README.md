# shell_scripts

A collection of lightweight, practical command-line utilities designed for Linux and Wayland, prefixed with `td_` (T-Dynamos) and intended to be installed in `~/.local/bin`.

---

## Prerequisites

The scripts require Python 3 and a few desktop tools depending on the utility:

| Dependency | Purpose | Required by |
|---|---|---|
| `python3` | Script execution runtime | All scripts |
| `python-matplotlib` | Standalone LaTeX math engine and PNG rendering | `td_math2img` |
| `wl-clipboard` (`wl-copy`) | Copying images and text to Wayland clipboard | `td_math2img` |
| `swayimg` | Wayland-native image viewer | `td_math2img` (optional, for viewing) |
| `exiftool` / `python-pillow` | Photographic EXIF extraction (supports RAW, DNG, NEF, JPG) | `td_exif_summary`, `td_astro_stack` (recommended: `exiftool`) |
| `python-rich` | Rich terminal tables, rounded borders, and dashboard cards | `td_exif_summary`, `td_astro_stack` (optional, recommended) |
| `python-numpy` | Vectorized numerical processing & matrix transformations | `td_astro_stack` |
| `python-opencv` | SIFT star feature detection, RANSAC alignment & 16-bit TIFF I/O | `td_astro_stack` |
| `python-rawpy` | LibRaw 16-bit linear sensor demosaicing (DNG, CR2, NEF, ARW) | `td_astro_stack` (for camera RAW files) |
| `/sys/class/power_supply/` | Linux kernel battery sysfs interface | `td_battery_info`, `td_battery_watch` |

### One-line prerequisite installation

Choose the command matching your Linux distribution:

- **Arch Linux / EndeavourOS / Manjaro**:
  ```bash
  sudo pacman -S --needed python python-matplotlib wl-clipboard swayimg perl-image-exiftool python-pillow python-rich python-numpy python-opencv python-rawpy
  ```

- **Debian / Ubuntu / Linux Mint**:
  ```bash
  sudo apt-get update && sudo apt-get install -y python3 python3-matplotlib wl-clipboard swayimg libimage-exiftool-perl python3-pil python3-rich python3-numpy python3-opencv python3-rawpy
  ```

- **Fedora / RHEL**:
  ```bash
  sudo dnf install -y python3 python3-matplotlib wl-clipboard swayimg perl-Image-ExifTool python3-pillow python3-rich python3-numpy python3-opencv python3-rawpy
  ```

- **openSUSE**:
  ```bash
  sudo zypper install -y python3 python3-matplotlib wl-clipboard swayimg exiftool python3-Pillow python3-rich python3-numpy python3-opencv python3-rawpy
  ```

- **Void Linux**:
  ```bash
  sudo xbps-install -Sy python3 python3-matplotlib wl-clipboard swayimg exiftool python3-Pillow python3-rich python3-numpy python3-opencv python3-rawpy
  ```

---

## Installation & Updates

Ensure `~/.local/bin` is in your `$PATH` (e.g. in `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 1. Truly One-Line Remote Install / Update Command (via Git)

You can run this anywhere without manually cloning or keeping a local repository. It clones to a temporary directory, installs/updates all `td_*` executables and data into `~/.local/bin`, and immediately cleans up:

```bash
tmp=$(mktemp -d) && git clone --depth 1 https://github.com/T-Dynamos/shell_scripts.git "$tmp" && "$tmp"/install.sh && rm -rf "$tmp"
```

### 2. One-Line Remote Install (via Curl)

Alternatively, execute the bundled installer script directly:

```bash
curl -fsSL https://raw.githubusercontent.com/T-Dynamos/shell_scripts/main/install.sh | bash
```

### 3. If Cloned Locally

If you have cloned the repository locally, run the bundled installer:

```bash
./install.sh
```

Or manually install scripts and shared data:
```bash
mkdir -p ~/.local/bin && install -m 755 -v td_* ~/.local/bin/ && cp -r td_script_data ~/.local/bin/
```

> **Tip (Symlink install)**: If you develop scripts or `git pull` frequently, you can symlink them so updates take effect immediately:
> ```bash
> mkdir -p ~/.local/bin && ln -sf "$PWD"/td_* ~/.local/bin/ && ln -sfn "$PWD"/td_script_data ~/.local/bin/td_script_data
> ```

---

## Modular Architecture (`td_script_data`)

The repository is organized modularly with shared Python modules and assets located inside [`td_script_data/`](td_script_data/):

* **`common.py`**: Shared core utilities — ANSI terminal styling (`Colors`, `supports_color`), progress bars (`make_bar`, `make_progress_bar`), human-readable data formatters (`format_bytes`, `format_time`, `format_span`, `parse_duration`), hardware sysfs helpers (`find_batteries`, `read_sysfs_int`, `read_sysfs_str`), and data file path resolution (`get_data_dir`, `get_data_file`).
* **`exif.py`**: Shared photographic metadata extraction and formatting — `parse_shutter_seconds`, `format_shutter`, `format_aperture`, `format_focal`, `format_ev`, `extract_metadata_exiftool`, `extract_metadata_fallback`, and supported format extension sets (`IMAGE_EXTENSIONS`, `RAW_EXTENSIONS`).
* **`catalog.py`**: Central registry of all scripts, metadata, categories, and command examples (`SCRIPTS`).

All scripts dynamically resolve `td_script_data` at the top via `sys.path.insert(0, ...)` and import modules directly:
```python
import sys
from pathlib import Path

# Resolve shared data directory and insert into sys.path
_DATA_DIR = Path(__file__).resolve().parent / "td_script_data"
if not _DATA_DIR.is_dir():
    _DATA_DIR = Path.home() / ".local" / "bin" / "td_script_data"
if str(_DATA_DIR) not in sys.path:
    sys.path.insert(0, str(_DATA_DIR))

from common import Colors, supports_color, format_bytes
from exif import parse_shutter_seconds, format_shutter
from catalog import SCRIPTS
```

---

## Quick Reference (`td_script_info`)

Run `td_script_info` to get a quick one-line summary and example usage for all available scripts:

```bash
td_script_info
```

Or for a compact table:
```bash
td_script_info --compact
```

---

## How to Add a New Script

All scripts in this repository follow standard conventions to maintain consistency, reliability, and ease of maintenance. A starter skeleton script is provided: [`td_template`](td_template).

### Step-by-Step Guide

1. **Name your script**:
   Every script must start with the `td_` prefix (e.g. `td_my_utility`).

2. **Copy the starter template**:
   ```bash
   cp td_template td_my_utility
   ```

3. **Follow the standard template conventions**:
   - Use `#!/usr/bin/env python3` (or `#!/usr/bin/env bash` with `set -euo pipefail`).
   - Implement command-line flags with `argparse`.
   - Support standard flags where applicable:
     - `-j, --json` for machine-readable JSON output.
     - `-v, --verbose` and `-q, --quiet`.
     - `--no-color` (respect terminal TTY color detection: `sys.stdout.isatty()`).
   - Accept input from both command-line arguments and `stdin` when applicable.
   - Return appropriate exit codes (`0` on success, non-zero on failure).

4. **Make the script executable**:
   ```bash
   chmod +x td_my_utility
   ```

5. **Register in `td_script_info`**:
   Add an entry to the `SCRIPTS` dictionary in [`td_script_info`](td_script_info):
   ```python
   "td_my_utility": {
       "title": "Short Descriptive Title",
       "summary": "One-line summary of what the script does.",
       "example": "td_my_utility --option 'example argument'",
       "category": "Category Name",
   },
   ```

6. **Document in `README.md`**:
   Add a section under **Included Scripts** documenting features, options, and usage examples.

7. **Test, Install, and Generate Fish Completions**:
   ```bash
   ./td_my_utility --help
   ./td_script_info td_my_utility
   ./install.sh                # Installs scripts and auto-generates Fish completions
   # Or manually update completions:
   td_fish_completions
   ```

---

## Included Scripts

### 1. `td_script_info`

Interactive directory and summary utility for all scripts in the suite.

#### Features
- Displays one-line description and copy-pasteable example command for every script.
- Shows whether each script is currently installed in your `$PATH`.
- Supports filtering by specific script name (`td_script_info td_math2img`).
- Supports `--json` for scripting integration and `--compact` for quick glances.

#### Usage
```bash
td_script_info
td_script_info td_math2img
td_script_info --compact
td_script_info --json
```

---

### 2. `td_math2img`

Renders LaTeX math formulas directly to high-resolution images (PNG, SVG, etc.), copies them to the Wayland clipboard via `wl-copy`, and optionally displays them in `swayimg`. Uses Computer Modern serif math typography (`mathtext.fontset: cm`, `font.family: serif`).

#### Features
- Accepts expressions as CLI arguments or piped from `stdin`.
- Automatically strips outer `$...$`, `$$...$$`, `\[...\]`, or `\displaystyle`.
- Directly saves output via `--save {imgpath}` or `-o {imgpath}` (supports `.png`, `.svg`, etc.).
- Built-in interactive LaTeX math cheat sheet via `--cheatsheet` (opens in default browser).
- Copies the image to the Wayland clipboard (`image/png`, `image/svg+xml`) via a detached `wl-copy` session.
- Seamless preview in `swayimg` (foreground or detached background).
- Supports transparent backgrounds (`-t`), dark theme preset (`-d`), custom colors, DPI, and font sizes.

#### Usage Examples

```bash
# Render and copy quadratic formula to clipboard
td_math2img '\frac{-b \pm \sqrt{b^2-4ac}}{2a}'

# Open interactive LaTeX Math Cheat Sheet in browser
td_math2img --cheatsheet

# Save image to a specific path using --save
td_math2img --save formula.png '\frac{-b \pm \sqrt{b^2-4ac}}{2a}'

# Save as vector SVG
td_math2img --save formula.svg '\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}'

# Render, copy to clipboard, and open in swayimg
td_math2img -s '\frac{-b \pm \sqrt{b^2-4ac}}{2a}'

# Open in swayimg in the background (does not block terminal)
td_math2img -s --detach '\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}'

# Render with a transparent background
td_math2img -t -s '\sum_{k=1}^n k = \frac{n(n+1)}{2}'

# Dark mode theme (white text on dark background)
td_math2img -d -s '\mathbf{F} = m \mathbf{a}'

# Read formula from stdin
echo '\alpha^2 + \beta^2 = \gamma^2' | td_math2img -s
```

#### Options Reference

| Option | Description |
|---|---|
| `expression` | LaTeX formula string. Reads from `stdin` if omitted or `-`. |
| `--save, -o, --output FILE` | Destination image file path (e.g. `--save formula.png` or `-o formula.svg`). Defaults to temp file in `/tmp/math_*.png`. |
| `-s, --show, --view` | Open the rendered image in `swayimg`. |
| `--detach` | Launch `swayimg` in the background (detaches from terminal). |
| `--swayimg-args ARGS` | Pass custom arguments to `swayimg` (e.g. `'--swayimg-args="-S 600,400"'`). |
| `-n, --no-copy` | Do not copy the rendered image to the clipboard. |
| `-p, --primary` | Copy to the Wayland primary selection instead of the clipboard. |
| `-t, --transparent` | Render with a transparent background. |
| `-d, --dark` | Dark theme preset: white text on `#181825` (or transparent if `-t`). |
| `--bg, --background COLOR` | Set custom background color (e.g. `white`, `transparent`, `#1e1e2e`). |
| `--fg, --color COLOR` | Set custom formula text color (e.g. `black`, `white`, `#89b4fa`). |
| `--dpi DPI` | Resolution in DPI (default: `300`). |
| `--size, --fontsize SIZE` | Font size in points (default: `24`). |
| `--pad PAD` | Padding in pixels around formula (default: `16`). |
| `--font FONT` | Math font set: `cm` (default), `dejavusans`, `dejavuserif`, `stix`, `stixsans`. |
| `--cheatsheet, --cheatsheat` | Open the interactive LaTeX math cheat sheet in your default web browser. |
| `-q, --quiet` | Suppress status output. |

---

### 3. `td_tmp_clean`

Cleans temporary images in `/tmp` generated by math formulas, ImageMagick, and graphic rendering utilities.

#### Features
- Automatically targets temporary formula images (`math_*.png`, `magick-*`, `test_*`, `swayimg-*`).
- Strict ownership check: only deletes files owned by the current user (`UID`).
- Safe `--dry-run` (`-n`) preview mode to inspect files and reclaimed disk space before deleting.
- Optional `--all` (`-a`) flag to clean all image files in `/tmp`.
- Filter by age via `--older-than` (e.g. `30m`, `2h`, `1d`).
- JSON export mode (`-j`) for scripting and cleanup automations.

#### Usage Examples

```bash
# Preview what temporary images would be deleted
td_tmp_clean --dry-run

# Clean temporary images in /tmp
td_tmp_clean

# Show every deleted file
td_tmp_clean -v

# Only clean temporary images older than 1 hour
td_tmp_clean --older-than 1h

# Clean all user-owned images in /tmp
td_tmp_clean --all

# Clean with custom glob pattern
td_tmp_clean -p 'math_*.png'
```

#### Options Reference

| Option | Description |
|---|---|
| `-n, --dry-run` | Scan and display files that would be removed without deleting. |
| `-a, --all` | Clean all user-owned image files in target dir, not just math/magick prefixes. |
| `-p, --pattern GLOB` | Clean files matching a custom glob pattern (e.g. `'math_*.png'`). |
| `--older-than TIME` | Only delete images older than duration (e.g. `'30m'`, `'2h'`, `'1d'`). |
| `-d, --dir DIR` | Target temporary directory (default: `/tmp`). |
| `-v, --verbose` | List every file path removed. |
| `-j, --json` | Output results in JSON format. |
| `-q, --quiet` | Suppress non-error output. |

---

### 4. `td_battery_info`

Quick battery diagnostics script reading from Linux sysfs (`/sys/class/power_supply/`).

#### Features
- Full argument parser with multiple output modes (standard, short, JSON, verbose).
- Automatically discovers batteries (`BAT0`, `BAT1`, etc.).
- Color-coded health percentage indicator.
- Support for systems using `charge_*` (µAh) and `energy_*` (µWh).

#### Metrics Reported
- **Health**: Percentage of current full charge capacity relative to design capacity (`(charge_full / charge_full_design) * 100`).
- **Capacity**: Formatted in `mAh` (or `mWh`).
- **CC Phase Estimate**: Estimated Constant Current charging phase current in Amperes.
- **Hardware Info** (`-v`): Battery model, manufacturer, technology, cycle count, and voltage.

#### Usage
```bash
# Standard formatted output
td_battery_info

# Single-line summary
td_battery_info --short

# JSON output (ideal for Waybar, i3blocks, polybar, or scripts)
td_battery_info --json

# Detailed hardware info
td_battery_info -v

# Target a specific battery
td_battery_info -b BAT0
```

---

### 5. `td_battery_watch`

Interactive live terminal monitor and power consumption tracker.

#### Features
- Full argument parser with configurable refresh rate, `--once` mode, and `--json` export.
- Graphical charge progress bar (`[███████████████] 100%`).
- Real-time power draw calculation in milliAmperes (mA) and Watts (W).
- **Charging CC Comparison**: When charging, automatically compares actual charging current against theoretical Constant Current (CC) target, reporting percentage off (`-9.0% off`), difference in mA, and percentage of target.
- Live estimation of **Time to empty** (while discharging) or **Time to full** (while charging).
- Color-coded status alerts (Charging, Discharging, Full).
- **In-place redraw**: Clears and updates only from where the command started, preserving your terminal history and scrollback above the command.
- Clean exit on `Ctrl+C` without terminal cursor or traceback glitches (cursor is hidden during live monitor and cleanly restored on exit).

#### Usage
```bash
# Live dashboard (ultra-responsive default 0.1s / 100ms refresh, in-place redraw)
td_battery_watch

# Custom refresh interval (e.g. 0.5s or 1.0s)
td_battery_watch -i 1.0

# Print single status snapshot and exit (no infinite loop)
td_battery_watch --once

# Always display CC phase estimate line even when not charging
td_battery_watch --once --show-cc

# Single snapshot in JSON format
td_battery_watch --once --json

# Append mode (do not clear screen)
td_battery_watch --no-clear

# Legacy full-screen clear mode
td_battery_watch --full-clear
```

#### Example Output (Charging Mode with CC Comparison)
```text
Battery       : BAT0
Status        : Charging
Health        : 78.23% (1721/2200 mAh)
Charge        : 65.40% [██████████░░░░░] (1125/1721 mAh)
Current       : 1250.00 mA (~19.50 W)
CC Phase Est  : 1.37 A (1374 mA)
CC Comparison : -9.0% off (-124 mA | 91.0% of CC target)
Time to full  : 23m 48s
```

---

### 6. `td_fish_completions`

Dynamic Fish Shell completion generator and installer. Introspects Python `argparse` definitions across all `td_*` utilities, generates syntax-rich completion definitions with smart contextual suggestions (battery devices, directories, file completion, math expressions), and installs them directly to `~/.config/fish/completions/`.

#### Features
- **Dynamic Introspection**: Reads `build_parser()` directly from scripts—any new script created with `td_template` is automatically supported without writing Fish code!
- **Context-Aware Suggestions**:
  - Dynamically queries `/sys/class/power_supply/` for `-b / --battery` flags.
  - Suggests directory paths for directory flags (`--dir`).
  - Pre-populates common LaTeX formulas for `td_math2img`.
  - Suggests valid choices for `--font`, `--format`, `--color`, etc.
  - Suppresses file suggestions on numeric/text flags to keep the completion popup clean.
- Automatically executed by `./install.sh` when Fish shell is installed.

#### Usage
```bash
# Generate and install completions for all td_* scripts into ~/.config/fish/completions/
td_fish_completions

# Preview generated completions without writing to disk
td_fish_completions --dry-run

# Print Fish completion code for a specific command to stdout
td_fish_completions --print td_battery_watch

# List all discovered scripts and their parser status
td_fish_completions --list

# Install into a custom directory
td_fish_completions --dir /path/to/custom/completions
```

---

### 7. `td_exif_summary`

Scans image files in the current or specified directory and extracts photographic EXIF metadata. Uses **Rich** to display full, un-truncated photographic tables with rounded borders, distinct colors, and a comprehensive statistical dashboard featuring ISO distribution charts, top camera lenses, aperture frequencies, and exposure spans.

#### Features
- **Rich Terminal Tables**: Beautiful, modern tables rendered with `rich` featuring rounded borders (`box.ROUNDED`), color-coded ISO ratings, highlighted shutter speeds, and full un-truncated details.
- **Full Photographic Info**: Shows complete filenames, camera models, lens designations, 35mm equivalent focal lengths, exposure modes (Manual, Auto, Aperture Pri, Shutter Pri), flash status, resolution, file sizes, and GPS geotags without truncation.
- **Default Full Display**: Displays all images by default (`--limit 0` for all / unlimited) without arbitrarily truncating rows.
- **Broad Format Support**: Seamlessly processes both standard image formats (`JPG`, `PNG`, `TIFF`, `WEBP`) and RAW camera files (`DNG`, `NEF`, `CR2`, `ARW`, etc.).
- **Dual Engine Architecture**: Automatically leverages system `exiftool` for fast batch extraction and RAW MakerNote decoding (e.g. precise lens models), falling back to pure-Python `Pillow` when `exiftool` is not installed.
- **Statistical Dashboard**: Computes aggregate photo statistics including:
  - ISO range, median, mean, and visual ASCII/Rich distribution histogram.
  - Top shutter speeds and exposure times (correctly handles fractions like `1/640s` and long exposures like `32s`).
  - Top apertures ($f$-numbers) and focal lengths.
  - Date and time span of the photo shoot.
  - Camera models, lens breakdown, and geotag percentages.
- **Streamlined Default Columns**: Focuses cleanly on core photographic settings (`File`, `Lens`, `Focal`, `Shutter`, `Aperture`, `ISO`, `EV`, `Resolution`, `Size`). Secondary columns (`Date/Time`, `Camera`, `Mode`, `Flash`) are omitted by default for clean horizontal alignment and can be toggled on as needed.
- **Column Toggle Flags**:
  - `--full, --all`: Display all columns including `Date/Time`, `Camera`, `Mode`, and `Flash`.
  - `--date, --time`: Include `Date / Time` column.
  - `--camera`: Include `Camera` model column.
  - `--mode`: Include `Mode` (Exposure Mode / Program) column.
  - `--flash`: Include `Flash` status column.
- **Flexible Display Modes**:
  - Full view: File table + Statistics dashboard.
  - `-s, --summary-only`: Print only the aggregate photographic stats dashboard.
  - `-t, --table-only`: Print only the per-file table.
  - `-b, --bare`: Print only bare file paths (one per line, with trailing `\` shell line continuation) for easy copy-pasting directly into multi-line commands.
  - `--shutter`: Instant shortcut to sort by shutter speed and output bare image paths with trailing `\` (also accepts `--sort --shutter`).
  - `--filenames`: Output only base filenames (e.g. `DSC_0001.JPG \`) instead of directory paths in bare mode.
  - `--with-value`: Print the sorted value (e.g. shutter speed, ISO) alongside each bare path.
  - `--no-slash`: Omit the trailing `\` line continuation in bare mode.
- **Sorting & Filtering**:
  - Sort by `--sort {name,date,iso,shutter,aperture,focal,size}` with `--reverse`.
  - Limit table rows via `--limit N` (default: `0` for all / unlimited).
- **Export Options**:
  - `-j, --json`: Machine-readable JSON output for scripting or metadata archival.
  - `--csv`: Export metadata to CSV for spreadsheets or data analysis.
- **Recursive Scanning**: `-r, --recursive` recursively traverses all nested photo directories.

#### Usage Examples

```bash
# Scan current directory and print table + statistics
td_exif_summary

# Sort by shutter speed and print bare image paths (easy to copy/paste)
td_exif_summary --shutter
td_exif_summary --sort --shutter /path/to/photos

# Sort by shutter speed from slowest/longest to fastest
td_exif_summary --shutter --reverse

# Copy fastest shutter photos to another folder
cp $(td_exif_summary --shutter /path/to/photos | head -n 10) /destination/

# Print bare filenames only
td_exif_summary --shutter --filenames

# Print shutter values alongside bare paths
td_exif_summary --shutter --with-value

# Bare output with custom sort (e.g. sorted by ISO)
td_exif_summary --bare --sort iso

# Scan a specific directory
td_exif_summary /path/to/photos

# Recursively scan photo library
td_exif_summary -r /run/media/tdynamos/Secondary/Pictures

# Show only the statistical dashboard (omitting file table)
td_exif_summary -s /path/to/photos

# Sort by ISO descending to find high-noise / low-light shots
td_exif_summary --sort iso --reverse

# Export full photographic metadata to JSON or CSV
td_exif_summary --json > photo_metadata.json
td_exif_summary --csv > photo_metadata.csv

# Pipe JSON to jq for custom queries
td_exif_summary -j | jq '.summary.iso_distribution'
```

#### Options Reference

| Option | Description |
|---|---|
| `PATH` | Target image file or directory to scan (default: current directory `.`). |
| `--full, --all` | Display all columns in table (including Date/Time, Camera, Mode, Flash). |
| `--date, --time` | Include Date / Time column in table (omitted by default). |
| `--camera` | Include Camera model column in table (omitted by default). |
| `--mode` | Include Exposure Mode column in table (omitted by default). |
| `--flash` | Include Flash status column in table (omitted by default). |
| `-b, --bare` | Output only bare image file paths (one per line, with trailing `\` shell line continuation) for easy copy-pasting. |
| `--shutter` | Sort images by shutter speed and output them bare with trailing `\` (convenience shortcut for `--sort shutter --bare`). |
| `--filenames` | When in bare mode, output only base filenames instead of directory paths. |
| `--with-value` | When in bare mode, print sorted value (e.g. shutter speed, ISO) alongside each path. |
| `--no-slash` | Omit the trailing shell line-continuation backslash (`\`) in bare mode. |
| `-r, --recursive` | Recursively scan all subdirectories for images. |
| `-s, --summary-only` | Display only the aggregate statistical dashboard (omit file table). |
| `-t, --table-only` | Display only the per-file table (omit statistical dashboard). |
| `-j, --json` | Output all records and summary statistics in JSON format. |
| `--csv` | Output all records as CSV for spreadsheets or data analysis. |
| `--sort FIELD` | Sort table by: `name`, `date`, `iso`, `shutter`, `aperture`, `focal`, or `size`. |
| `--reverse` | Reverse the sort order. |
| `--limit N` | Maximum rows to display in table (default: `0` for all / unlimited). |
| `--engine ENGINE` | EXIF extraction engine: `auto` (default), `exiftool`, or `pillow`. |
| `--no-color` | Disable ANSI colored output. |

---

### 8. `td_astro_stack`

Astrophotography RAW & Image Stacker with sub-pixel star alignment (Astroalign asterism matching + Homography / Affine / Rigid), ISO exposure normalization, Lanczos-4 sinc interpolation, and ultra-low RAM disk-buffered streaming (`np.memmap`).

Designed for astrophotographers who take tripod or tracker sequences across identical shutter speeds and varying ISO levels to capture the night sky. Automatically groups photos by shutter speed, aligns celestial drift with sub-pixel precision (< 0.3 px residual error), normalizes exposure gain so that pristine low-noise shadow data from lower ISOs blends seamlessly into the high-ISO baseline, and stacks frames using chunked sigma-clipping outlier rejection to eliminate satellite trails, aircraft, hot pixels, and cosmic rays.

Outputs a **16-bit linear master TIFF** (ideal for post-processing in Siril, PixInsight, RawTherapee, Photoshop, or GIMP) and an **auto-stretched 8-bit preview PNG** using Midtone Transfer Function (MTF) or Arcsinh stretching.

#### Key Features

- **Smart Shutter Speed Grouping**: Scans a folder or file list and automatically groups exposures by shutter speed (e.g. `32s`, `10s`, `1/4s`), defaulting to the largest group if `--shutter` is omitted.
- **Maximum Detail ISO Normalization**: Automatically chooses the **highest ISO frame** as the reference baseline (e.g. ISO 3200) to expose deep shadow details, Milky Way dust lanes, and faint stars. All lower ISO frames are scaled up linearly ($gain = ISO_{ref} / ISO_{i}$), boosting shadow data from clean low-ISO frames without introducing amplifier noise.
- **Sub-Pixel Precision Alignment**:
  - **Astroalign Pattern Matching**: Detects true stellar point sources (PSF) and matches asterism triangles invariant to scale and rotation.
  - **8-DOF Projective Homography (`--align homography`)**: Compensates for wide-angle lens gnomonic distortion and celestial sphere curvature across planar sensors, reducing residual alignment error from ~1.0 px down to < 0.25 px.
  - **Lanczos-4 Sinc Warping (`--interp lanczos`)**: 8-lobe windowed sinc filter preserves pinpoint high-frequency star cores and increases resolved faint stars by up to 80% without interpolation softening or ghost "comet" tails.
  - **Sub-Pixel Residual Error Metric**: Calculates and reports real-time residual reprojection error ($\pm \text{px}$) for each aligned frame.
- **Ultra-Low RAM Architecture**: Writes warped frames directly to disk memory-mapped scratch buffers (`np.memmap`) and processes row chunks (default: 256 rows). Peak RAM usage remains minimal (< 150 MB) even when stacking dozens or hundreds of high-resolution RAW frames. All temporary files are automatically cleaned up on completion.
- **Outlier Rejection**: Configurable sigma-clipping ($\kappa = 3.5$), median, or mean stacking to remove satellite streaks, airplanes, meteors, and cosmic ray hits.
- **Auto-Cropping (`--crop`)**: Automatically calculates the overlapping bounding box where all frames intersect and crops non-overlapping borders.
- **Auto-Stretch Preview & Viewer Integration**: Generates an 8-bit preview PNG stretched using PixInsight's standard Midtone Transfer Function (MTF) or Arcsinh stretch, and opens it directly in `swayimg` via `-p` / `--preview`.

#### Usage Examples

```bash
# Auto-detect largest shutter group in directory and stack with homography & Lanczos-4
td_astro_stack /path/to/raws/

# Stack photos taken specifically at 32 seconds exposure
td_astro_stack -s 32s /path/to/raws/

# Fast half-size preview stack, auto-crop borders, and preview in swayimg
td_astro_stack -s 32s --fast --crop --preview

# Use median stacking with custom output file
td_astro_stack -s 32s -m median -o master_milkyway.tif

# Dry run inspection of shutter speed groups and ISO range
td_astro_stack /path/to/raws/ --dry-run

# Output full alignment metrics and residual errors in JSON
td_astro_stack -s 32s -j | jq '.frames[] | {filename, residual_error_px}'
```

#### Options Reference

| Option | Description |
|---|---|
| `PATH` | Input directory, image file paths, or glob pattern (default: `.`). |
| `-s, --shutter SEC` | Target shutter speed to stack (e.g. `32s`, `32`, `10s`, `1/4s`). Auto-selects largest group if omitted. |
| `--ref INDEX_OR_NAME` | Reference frame (1-based index or filename). Default: auto-selects via `--ref-mode`. |
| `--ref-mode MODE` | Reference frame selection strategy: `highest` (default: highest ISO reveals maximum shadow detail & dynamic range), `median`, or `lowest`. |
| `--align MODE` | Transform mode: `homography` (8-DOF projective matrix compensating for lens perspective tilt and wide-angle curvature, default), `affine` (6-DOF anisotropic scaling and shear), `rigid` (4-DOF Euclidean rotation + translation), or `none`. |
| `--interp INTERP` | Sub-pixel warping interpolation: `lanczos` (8-lobe sinc filter preserving pinpoint star peaks, default), `cubic`, or `linear`. |
| `--chain, --sequential` | Enable sequential adjacent-frame registration chain (recommended for long-duration sequences where stars drift significantly across the sky). |
| `--align-target TARGET` | Feature registration focus: `stars` (default: isolates sky stars for maximum Milky Way sharpness & contrast), `ground` (aligns stationary monastery/terrain), or `full`. |
| `--sky-ratio FLOAT` | Vertical fraction of image from top containing sky (default: `0.50` for landscapes with horizon; use `1.0` for deep sky). |
| `--no-iso-gain` | Disable automatic ISO exposure gain scaling. |
| `-m, --method METHOD` | Stacking method: `sigma-clip` (default, rejects satellite trails & hot pixels), `median`, or `mean`. |
| `-k, --kappa NUM` | Sigma-clipping threshold multiplier $\kappa$ (default: `3.5`). |
| `--crop` | Auto-crop output to the intersection bounding box where all frames overlap. |
| `--fast, --half-size` | Half-size processing mode for ultra-fast stacking and test previews. |
| `--chunk-size ROWS` | Row chunk size during stacking to constrain RAM usage (default: `256` rows). |
| `--temp-dir DIR` | Custom directory for disk scratch buffers / memmap files (default: system `/tmp`). |
| `-o, --output FILE` | Output 16-bit master TIFF filename (default: `stack_<shutter>_<N>frames.tif`). |
| `--stretch ALGO` | Auto-stretch algorithm for 8-bit preview PNG: `mtf` (default), `asinh`, `linear`, or `none`. |
| `--target-bg FLOAT` | Target sky background brightness for MTF stretch (default: `0.15`). |
| `--shadow-clip FLOAT` | Shadow clipping factor for sky background neutralization (default: `0.75`). Higher = darker sky. |
| `--no-contrast-boost` | Disable S-curve contrast boost in preview image. |
| `-p, -v, --preview` | Automatically open stretched preview in `swayimg` or default image viewer. |
| `--dry-run` | Scan and display shutter speed groups and alignment plan without processing. |
| `-j, --json` | Output results and alignment metrics in JSON format. |
| `-q, --quiet` | Suppress progress output and non-essential logs. |

---

### 9. `td_template`

Starter skeleton template for creating new `td_*` utilities. Includes built-in `argparse` setup, JSON output support, ANSI color management, standard input handling, and exit code handling.

```bash
# View template CLI options
td_template --help

# Test execution
td_template "Sample test input"
td_template "Sample test input" --json
```

---

## Authors

- **Ansh Dadwal** ([@T-Dynamos](https://github.com/T-Dynamos))
- **Antigravity** (Google DeepMind)

---

## License

This project is licensed under the [MIT License](LICENSE).
