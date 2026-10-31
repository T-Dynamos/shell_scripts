# shell_scripts

A collection of lightweight, practical command-line utilities designed for Linux and Wayland, prefixed with `td_` (T-Dynamos) and intended to be installed in `~/.local/bin`.

---

## Prerequisites

The scripts require Python 3 and a few desktop tools depending on the utility:

| Dependency | Purpose | Required by |
|---|---|---|
| `python3` | Script execution runtime | All scripts |
| `python-matplotlib` | Standalone LaTeX math engine and PNG rendering | `td_math2png` |
| `wl-clipboard` (`wl-copy`) | Copying images and text to Wayland clipboard | `td_math2png` |
| `swayimg` | Wayland-native image viewer | `td_math2png` (optional, for viewing) |
| `/sys/class/power_supply/` | Linux kernel battery sysfs interface | `td_battery_info`, `td_battery_watch` |

### One-line prerequisite installation

Choose the command matching your Linux distribution:

- **Arch Linux / EndeavourOS / Manjaro**:
  ```bash
  sudo pacman -S --needed python python-matplotlib wl-clipboard swayimg
  ```

- **Debian / Ubuntu / Linux Mint**:
  ```bash
  sudo apt-get update && sudo apt-get install -y python3 python3-matplotlib wl-clipboard swayimg
  ```

- **Fedora / RHEL**:
  ```bash
  sudo dnf install -y python3 python3-matplotlib wl-clipboard swayimg
  ```

- **openSUSE**:
  ```bash
  sudo zypper install -y python3 python3-matplotlib wl-clipboard swayimg
  ```

- **Void Linux**:
  ```bash
  sudo xbps-install -Sy python3 python3-matplotlib wl-clipboard swayimg
  ```

---

## Installation & Updates

Ensure `~/.local/bin` is in your `$PATH` (e.g. in `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### One-line command to install or update in `~/.local/bin`

Run this single command from within the cloned repository to install or update all `td_*` scripts into `~/.local/bin`:

```bash
mkdir -p ~/.local/bin && install -m 755 -v td_* ~/.local/bin/
```

> **Tip (Symlink install)**: If you develop or pull git changes frequently, you can symlink them so updates reflect immediately without re-copying:
> ```bash
> mkdir -p ~/.local/bin && ln -sf "$PWD"/td_* ~/.local/bin/
> ```

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

## Included Scripts

### 1. `td_script_info`

Interactive directory and summary utility for all scripts in the suite.

#### Features
- Displays one-line description and copy-pasteable example command for every script.
- Shows whether each script is currently installed in your `$PATH`.
- Supports filtering by specific script name (`td_script_info td_math2png`).
- Supports `--json` for scripting integration and `--compact` for quick glances.

#### Usage
```bash
td_script_info
td_script_info td_math2png
td_script_info --compact
td_script_info --json
```

---

### 2. `td_math2png`

Renders LaTeX math formulas directly to high-resolution PNG images, copies them to the Wayland clipboard via `wl-copy`, and optionally displays them in `swayimg`. Uses Computer Modern serif math typography (`mathtext.fontset: cm`, `font.family: serif`).

#### Features
- Accepts expressions as CLI arguments or piped from `stdin`.
- Automatically strips outer `$...$`, `$$...$$`, `\[...\]`, or `\displaystyle`.
- Directly copies the image to the Wayland clipboard (`image/png`) via a detached `wl-copy` session.
- Seamless preview in `swayimg` (foreground or detached background).
- Supports transparent backgrounds (`-t`), dark theme preset (`-d`), custom colors, DPI, and font sizes.

#### Usage Examples

```bash
# Render and copy quadratic formula to clipboard
td_math2png '\frac{-b \pm \sqrt{b^2-4ac}}{2a}'

# Render, copy to clipboard, and open in swayimg
td_math2png -s '\frac{-b \pm \sqrt{b^2-4ac}}{2a}'

# Open in swayimg in the background (does not block terminal)
td_math2png -s --detach '\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}'

# Render with a transparent background
td_math2png -t -s '\sum_{k=1}^n k = \frac{n(n+1)}{2}'

# Dark mode theme (white text on dark background)
td_math2png -d -s '\mathbf{F} = m \mathbf{a}'

# Save output to a specific PNG file
td_math2png -o formula.png '\lim_{x \to 0} \frac{\sin x}{x} = 1'

# Read formula from stdin
echo '\alpha^2 + \beta^2 = \gamma^2' | td_math2png -s
```

#### Options Reference

| Option | Description |
|---|---|
| `expression` | LaTeX formula string. Reads from `stdin` if omitted or `-`. |
| `-s, --show, --view` | Open the rendered image in `swayimg`. |
| `--detach` | Launch `swayimg` in the background (detaches from terminal). |
| `--swayimg-args ARGS` | Pass custom arguments to `swayimg` (e.g. `'--swayimg-args="-S 600,400"'`). |
| `-o, --output FILE` | Output PNG file path (default: temporary file in `/tmp/math_*.png`). |
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
| `-q, --quiet` | Suppress status output. |

---

### 3. `td_battery_info`

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

#### Example Output
```text
--- Battery Information (BAT0) ---
Health           : 78.23%
Capacity         : 1721/2200 mAh
Status           : Full
CC phase estimate: 1.37A
```

---

### 4. `td_battery_watch`

Interactive live terminal monitor and power consumption tracker.

#### Features
- Full argument parser with configurable refresh rate, `--once` mode, and `--json` export.
- Graphical charge progress bar (`[███████████████] 100%`).
- Real-time power draw calculation in milliAmperes (mA) and Watts (W).
- Live estimation of **Time to empty** (while discharging) or **Time to full** (while charging).
- Color-coded status alerts (Charging, Discharging, Full).
- Clean exit on `Ctrl+C` without terminal cursor or traceback glitches.

#### Usage
```bash
# Live dashboard (default 0.5s refresh)
td_battery_watch

# Custom refresh interval
td_battery_watch -i 1.0

# Print single status snapshot and exit (no infinite loop)
td_battery_watch --once

# Single snapshot in JSON format
td_battery_watch --once --json

# Append mode (do not clear screen)
td_battery_watch --no-clear
```

#### Example Output
```text
Battery       : BAT0
Status        : Full
Charge        : 100.00% [███████████████] (1721/1721 mAh)
Current       : 1.00 mA (~0.02 W)
Time          : Full (charged)
```

---

## Authors

- **Ansh Dadwal** ([@T-Dynamos](https://github.com/T-Dynamos))
- **Antigravity** (Google DeepMind)

---

## License

This project is licensed under the [MIT License](LICENSE).
