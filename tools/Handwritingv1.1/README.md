# Handwriting Batch Renderer v1.1

Turns a text file into A4 handwriting-style PNG pages and a PDF.
Uses a **user-provided** handwriting font (TTF/OTF/TTC) — no fonts are bundled.

> **v1.1** — Updated license server address.

## Quick Start

```powershell
# Activate license (one-time)
python handwriting.py --license-setup YOUR-KEY

# Check quota
python handwriting.py --license-info

# Render (font can come from preset or CLI)
python handwriting.py --input myfile.txt --preset presets/default.json

# Or pass font explicitly
python handwriting.py --input myfile.txt --font my-font.ttf

# Preview mode (no key, watermarked output)
python handwriting.py --input myfile.txt --font my-handwriting-font.ttf --preview
```

## Encrypted Build (Pyarmor)

The Pyarmor-encrypted version requires **Python 3.13.12 (64-bit, Windows)**.
The `.pyd` runtime is bound to this version — other Python versions cannot run it.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input PATH` | — | `.txt` input file (UTF-8 or GBK) |
| `--font PATH` | — | TTF/OTF/TTC font file (not bundled; can be set via preset) |
| `--out PATH` | `output` | Output directory |
| `--paper` | `white` | `white`, `plain`, `lined`, or `grid` |
| `--ink` | `#000000` | Ink color hex |
| `--seed` | random | Fixed seed for reproducibility |
| `--preset PATH` | — | JSON preset file |
| `--preview` | off | Skip license, add watermark |
| `--license-setup KEY` | — | Activate license key |
| `--license-info` | — | Query remaining quota |
| `--margin` | 220 | Page margin (px) |
| `--font-size` | 80 | Font size (px) |
| `--line-height` | 90 | Line height (px) |
| `--wrap-safety` | 80 | Wrap safety (px) |
| `--font-size-jitter` | 0.025 | Size jitter ratio |
| `--line-y-jitter` | 3.0 | Line Y jitter (px) |
| `--char-y-jitter` | 5.0 | Char Y jitter (px) |
| `--char-x-jitter` | 0.8 | Char X jitter (px) |
| `--latin-y-jitter` | 1.6 | Latin Y jitter (px) |
| `--latin-x-jitter` | 0.35 | Latin X jitter (px) |
| `--char-spacing-min` | -10.5 | Min char spacing (px) |
| `--char-spacing-max` | -4.0 | Max char spacing (px) |
| `--punct-spacing-min` | -24.0 | Min punct spacing (px) |
| `--punct-spacing-max` | -15.0 | Max punct spacing (px) |
| `--colon-spacing-min` | -8.0 | Min colon spacing (px) |
| `--colon-spacing-max` | 4.0 | Max colon spacing (px) |
| `--baseline-drift-min` | -0.8 | Min drift (px) |
| `--baseline-drift-max` | 0.8 | Max drift (px) |
| `--baseline-drift-limit` | 14.0 | Drift limit (px) |
| `--baseline-drift-recovery` | 0.35 | Drift recovery rate |
| `--baseline-shock-chance` | 0.16 | Shock probability |
| `--baseline-shock-min` | 5.0 | Min shock (px) |
| `--baseline-shock-max` | 11.0 | Max shock (px) |
| `--baseline-shock-cooldown` | 2 | Shock cooldown lines |
| `--line-slope-chance` | 0.5 | Slope probability |
| `--line-slope-min` | -35.0 | Min slope (px) |
| `--line-slope-max` | 35.0 | Max slope (px) |
| `--line-slope-recovery` | 0.85 | Slope recovery rate |
| `--line-slope-limit` | 40.0 | Slope limit (px) |
| `--mistake-chance` | 0 | Mistake probability |
| `--mistake-crossout-lines` | 15 | Crossout scribble strokes |
| `--mistake-crossout-thickness` | 4.0 | Crossout thickness (%) |

## Presets

Default values can be loaded from a JSON file. CLI arguments override preset values.

```json
{
    "font": "my-font.ttf",
    "paper": "white",
    "font_size": 80,
    "line_height": 90,
    "line_y_jitter": 3,
    "line_slope_min": -35,
    "line_slope_max": 35,
    "line_slope_limit": 40,
    "line_slope_chance": 0.5,
    "line_slope_recovery": 0.85,
    "mistake_chance": 0,
    "mistake_crossout_lines": 15,
    "mistake_crossout_thickness": 4.0
}
```

Font paths in presets are resolved relative to the working directory where you run
the script. Save a custom preset with your font path to avoid typing it every time.

## License

Per-1000-character billing. Preview mode is free but watermarked.

A valid license key is required for normal rendering. Run `--license-setup <key>` to activate.
