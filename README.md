# shell_scripts

A collection of lightweight, practical command-line utilities designed for Linux and Wayland, intended to be installed in `~/.local/bin`.

---

## Prerequisites

The scripts require Python 3 and a few desktop tools depending on the utility:

| Dependency | Purpose | Required by |
|---|---|---|
| `python3` | Script execution runtime | All scripts |
| `python-matplotlib` | Standalone LaTeX math engine and PNG rendering | `math2png` |
| `wl-clipboard` (`wl-copy`) | Copying images and text to Wayland clipboard | `math2png` |
| `swayimg` | Wayland-native image viewer | `math2png` (optional, for viewing) |
| `/sys/class/power_supply/` | Linux kernel battery sysfs interface | `battery_info`, `battery_watch` |

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

Ensure `~/.local/bin` is in your `$PATH` (e.g. In `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### One-line command to install or update in `~/.local/bin`

Run this single command from within the cloned repository to install or update all scripts into `~/.local/bin`:

```bash
mkdir -p ~/.local/bin && install -m 755 -v battery_info battery_watch math2png ~/.local/bin/
```

> **Tip (Symlink install)**: If you develop or pull git changes frequently, you can symlink them so updates reflect immediately without re-copying:
> ```bash
> mkdir -p ~/.local/bin && ln -sf "$PWD"/{battery_info,battery_watch,math2png} ~/.local/bin/
> ```

---

## Included Scripts

### 1. `math2png`

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
math2png '\frac{-b \pm \sqrt{b^2-4ac}}{2a}'

# Render, copy to clipboard, and open in swayimg
math2png -s '\frac{-b \pm \sqrt{b^2-4ac}}{2a}'

# Open in swayimg in the background (does not block terminal)
math2png -s --detach '\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}'

# Render with a transparent background
math2png -t -s '\sum_{k=1}^n k = \frac{n(n+1)}{2}'

# Dark mode theme (white text on dark background)
math2png -d -s '\mathbf{F} = m \mathbf{a}'

# Save output to a specific PNG file
math2png -o formula.png '\lim_{x \to 0} \frac{\sin x}{x} = 1'

# Read formula from stdin
echo '\alpha^2 + \beta^2 = \gamma^2' | math2png -s
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

### 2. `battery_info`

Quick battery diagnostics script that reads from `/sys/class/power_supply/BAT0/` and prints health metrics.

#### Metrics Reported
- **Health**: Percentage of current full charge capacity relative to design capacity (`(charge_full / charge_full_design) * 100`).
- **Capacity**: Formatted in `mAh` (`charge_full / charge_full_design`).
- **CC Phase Estimate**: Estimated Constant Current charging phase current in Amperes.

#### Usage
```bash
battery_info
```

#### Example Output
```text
Health: 87.42%
Capacity: 4120/4713 mAh
CC phase estimate: 3.29A
```

---

### 3. `battery_watch`

Interactive live terminal monitor for real-time battery status and power consumption.

#### Features
- Refreshes every 0.5 seconds.
- Displays charging status (`Charging`, `Discharging`, `Full`, etc.).
- Displays current battery charge level and percentage.
- Displays instantaneous current rate in `mA`.
- Calculates and estimates **Time to empty** (while discharging) or **Time to full** (while charging).

#### Usage
```bash
battery_watch
```

Press `Ctrl+C` to exit the monitor.

---

## Authors

- **Ansh Dadwal** ([@T-Dynamos](https://github.com/T-Dynamos))
- **Antigravity** (Google DeepMind)

---

## License

This project is licensed under the [MIT License](LICENSE).
