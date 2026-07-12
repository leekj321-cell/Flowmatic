# Flowmatic Website

Static Flowmatic website for GitHub Pages and `flowmatic-os.com`.

## Structure

- `/`, `/nc.html`, `/ct.html`, `/work-standard.html`, `/tms.html`, `/amr.html`: Korean compatibility URLs for existing links.
- `/ko/`, `/en/`, `/ar/`: language-specific canonical pages.
- `/ko/{product}/`, `/en/{product}/`, `/ar/{product}/`: language-specific product pages.
- `build_site.py`: static page generator for the multilingual HTML output.
- `style-v5.19.css`: current stylesheet.
- `script.js`: navigation, reveal, product CTA, text fitting, and demo-video loader.

## Demo Videos

The current working demo videos are:

- `flowmatic_nc_demo.mp4`
- `flowmatic_ct_demo.mp4`

Work Standard, TMS, and AMR pages intentionally show development-preview panels instead of empty video players.

## Build

Run:

```bash
python3 build_site.py
```

The site is pure static HTML/CSS/JS and does not require a package install.
