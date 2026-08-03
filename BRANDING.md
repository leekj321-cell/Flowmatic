# Flowmatic Brand Assets

## Official logo

The only official logo mark is a flat 2×2 square with a single dark outline and dividers:

- top left: blue `#1565D8`
- bottom left: red `#E53935`
- top right: yellow `#F4C20D`
- bottom right: yellow `#F4C20D`
- stroke: `#111111`
- white: `#FFFFFF`

Do not rearrange the quadrants, add gradients or shadows, or use a different mark for small icons.

## Source and derived assets

The canonical vector and its derived files live in `/assets/branding/`:

- `flowmatic-logo-mark.svg` / `.png`
- `flowmatic-logo-horizontal.svg` / `.png`
- `flowmatic-favicon.ico`
- `apple-touch-icon.png`
- `android-chrome-192x192.png`
- `android-chrome-512x512.png`
- `flowmatic-og.svg` / `.png`
- `flowmatic-qr-contact-signature.svg` / `.png`

Run `tools/generate_brand_assets.py` with the QR dependency available to regenerate every derived asset from the same constants.

## Official QR contact signature

- destination: `https://flowmatic-os.com/`
- displayed URL: `flowmatic-os.com`
- displayed email: `contact@flowmatic-os.com`

The QR quiet zone must remain white and unobstructed. Do not place a logo or decoration over the QR modules.
