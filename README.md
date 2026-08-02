# Flowmatic Website

Static Flowmatic website for GitHub Pages and `flowmatic-os.com`.

## Structure

- `/`, `/nc.html`, `/ct.html`, `/quality.html`, `/work-standard.html`, `/tms.html`, `/amr.html`: Korean compatibility URLs for existing links.
- `/ko/`, `/en/`, `/ar/`: language-specific canonical pages.
- `/ko/{product}/`, `/en/{product}/`, `/ar/{product}/`: language-specific product pages.
- `build_site.py`: static page generator for the multilingual HTML output.
- `style-v5.20.css`: current stylesheet.
- `script.js`: navigation, reveal, product CTA, text fitting, demo-video loader, and AJAX inquiry submission.

## Demo Videos

The current working demo videos are:

- `flowmatic_nc_demo.mp4`
- `flowmatic_ct_demo.mp4`

Flowmatic Quality shows working-prototype and integration status without claiming a public demo. Work Standard, TMS, and AMR pages intentionally show development-preview panels instead of empty video players.

## Contact

The site displays `contact@flowmatic-os.com`. The contact form submits to a Formspree endpoint that delivers inquiries to this verified recipient address.

## Build

Run:

```bash
python3 build_site.py
```

The site is pure static HTML/CSS/JS and does not require a package install.
