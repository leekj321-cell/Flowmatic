from __future__ import annotations

import os
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.constants import ERROR_CORRECT_H


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets" / "branding"

BLUE = "#1565D8"
RED = "#E53935"
YELLOW = "#F4C20D"
INK = "#111111"
WHITE = "#FFFFFF"
URL = "https://flowmatic-os.com/"
DISPLAY_URL = "flowmatic-os.com"
EMAIL = "contact@flowmatic-os.com"


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / ("arialbd.ttf" if bold else "arial.ttf"),
        Path(r"C:\Windows\Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def svg_mark(size: int = 256) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 256 256" role="img" aria-labelledby="title desc">
  <title id="title">Flowmatic official logo mark</title>
  <desc id="desc">A two by two square: blue top left, red bottom left, yellow top right and yellow bottom right.</desc>
  <rect x="8" y="8" width="240" height="240" fill="{YELLOW}" stroke="{INK}" stroke-width="16"/>
  <rect x="16" y="16" width="112" height="112" fill="{BLUE}"/>
  <rect x="16" y="128" width="112" height="112" fill="{RED}"/>
  <path d="M128 8V248M8 128H248" fill="none" stroke="{INK}" stroke-width="16"/>
</svg>
'''


def draw_mark(size: int) -> Image.Image:
    scale = 4
    canvas = Image.new("RGBA", (size * scale, size * scale), (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)
    margin = round(size * 0.035 * scale)
    stroke = max(2 * scale, round(size * 0.065 * scale))
    center = size * scale // 2
    edge = size * scale - margin
    inner = margin + stroke // 2
    draw.rectangle((margin, margin, edge, edge), fill=YELLOW, outline=INK, width=stroke)
    draw.rectangle((inner, inner, center, center), fill=BLUE)
    draw.rectangle((inner, center, center, edge - stroke // 2), fill=RED)
    draw.line((center, margin, center, edge), fill=INK, width=stroke)
    draw.line((margin, center, edge, center), fill=INK, width=stroke)
    return canvas.resize((size, size), Image.Resampling.LANCZOS)


def horizontal_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="400" viewBox="0 0 1600 400" role="img" aria-labelledby="title desc">
  <title id="title">Flowmatic</title>
  <desc id="desc">Flowmatic official horizontal logo.</desc>
  <g transform="translate(40 40) scale(1.25)">{svg_mark().split('<svg', 1)[1].split('>', 1)[1].rsplit('</svg>', 1)[0]}</g>
  <text x="400" y="268" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="210" font-weight="700" letter-spacing="-8">Flowmatic</text>
</svg>
'''


def horizontal_png() -> Image.Image:
    image = Image.new("RGBA", (1600, 400), (255, 255, 255, 0))
    image.alpha_composite(draw_mark(320), (40, 40))
    draw = ImageDraw.Draw(image)
    draw.text((400, 86), "Flowmatic", fill=INK, font=font(210, bold=True), spacing=0)
    return image


def qr_matrix() -> list[list[bool]]:
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=1, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    return qr.get_matrix()


def qr_signature_png() -> Image.Image:
    width, height = 1200, 1400
    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rectangle((18, 18, width - 18, height - 18), outline=INK, width=18)
    draw.rectangle((18, 18, 210, 150), fill=BLUE, outline=INK, width=12)
    draw.rectangle((990, 18, width - 18, 150), fill=YELLOW, outline=INK, width=12)
    draw.rectangle((18, 1250, 230, height - 18), fill=RED, outline=INK, width=12)
    draw.rectangle((930, 1250, width - 18, height - 18), fill=YELLOW, outline=INK, width=12)
    image.paste(draw_mark(116), (86, 174), draw_mark(116))
    draw.text((230, 188), "Flowmatic", fill=INK, font=font(82, bold=True))

    matrix = qr_matrix()
    modules = len(matrix)
    box = 18
    qr_size = modules * box
    qr_left = (width - qr_size) // 2
    qr_top = 330
    draw.rectangle((qr_left, qr_top, qr_left + qr_size, qr_top + qr_size), fill=WHITE)
    for row, values in enumerate(matrix):
        for col, value in enumerate(values):
            if value:
                x = qr_left + col * box
                y = qr_top + row * box
                draw.rectangle((x, y, x + box - 1, y + box - 1), fill=INK)

    draw.text((width // 2, 1060), DISPLAY_URL, fill=INK, font=font(66, bold=True), anchor="mm")
    draw.text((width // 2, 1145), EMAIL, fill=INK, font=font(48, bold=True), anchor="mm")
    return image


def qr_signature_svg() -> str:
    matrix = qr_matrix()
    box = 18
    qr_size = len(matrix) * box
    left = (1200 - qr_size) // 2
    top = 330
    path = []
    for row, values in enumerate(matrix):
        for col, value in enumerate(values):
            if value:
                x = left + col * box
                y = top + row * box
                path.append(f"M{x} {y}h{box}v{box}h-{box}z")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1400" viewBox="0 0 1200 1400" role="img" aria-labelledby="title desc">
  <title id="title">Flowmatic QR contact signature</title>
  <desc id="desc">Scan to open https://flowmatic-os.com/. Contact email: contact@flowmatic-os.com.</desc>
  <rect width="1200" height="1400" fill="{WHITE}"/>
  <rect x="18" y="18" width="1164" height="1364" fill="none" stroke="{INK}" stroke-width="18"/>
  <rect x="18" y="18" width="192" height="132" fill="{BLUE}" stroke="{INK}" stroke-width="12"/>
  <rect x="990" y="18" width="192" height="132" fill="{YELLOW}" stroke="{INK}" stroke-width="12"/>
  <rect x="18" y="1250" width="212" height="132" fill="{RED}" stroke="{INK}" stroke-width="12"/>
  <rect x="930" y="1250" width="252" height="132" fill="{YELLOW}" stroke="{INK}" stroke-width="12"/>
  <g transform="translate(86 174) scale(.453125)">{svg_mark().split('<svg', 1)[1].split('>', 1)[1].rsplit('</svg>', 1)[0]}</g>
  <text x="230" y="260" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="82" font-weight="700">Flowmatic</text>
  <rect x="{left}" y="{top}" width="{qr_size}" height="{qr_size}" fill="{WHITE}"/>
  <path d="{''.join(path)}" fill="{INK}"/>
  <text x="600" y="1075" text-anchor="middle" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="700">{DISPLAY_URL}</text>
  <text x="600" y="1160" text-anchor="middle" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="700">{EMAIL}</text>
</svg>
'''


def og_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
  <title id="title">Flowmatic | Manufacturing Intelligence</title>
  <desc id="desc">Flowmatic official social preview.</desc>
  <rect width="1200" height="630" fill="{WHITE}"/>
  <rect x="32" y="32" width="1136" height="566" fill="none" stroke="{INK}" stroke-width="12"/>
  <rect x="846" y="32" width="322" height="150" fill="{BLUE}" stroke="{INK}" stroke-width="12"/>
  <rect x="1000" y="182" width="168" height="220" fill="{YELLOW}" stroke="{INK}" stroke-width="12"/>
  <rect x="846" y="402" width="322" height="196" fill="{RED}" stroke="{INK}" stroke-width="12"/>
  <g transform="translate(72 72) scale(.625)">{svg_mark().split('<svg', 1)[1].split('>', 1)[1].rsplit('</svg>', 1)[0]}</g>
  <text x="270" y="205" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="104" font-weight="700" letter-spacing="-4">Flowmatic</text>
  <text x="76" y="360" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="700">Manufacturing Intelligence</text>
  <text x="78" y="452" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="700">Motion → Event → Decision → Action</text>
  <text x="78" y="540" fill="{INK}" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="700">flowmatic-os.com</text>
</svg>
'''


def og_png() -> Image.Image:
    image = Image.new("RGB", (1200, 630), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rectangle((32, 32, 1168, 598), outline=INK, width=12)
    draw.rectangle((846, 32, 1168, 182), fill=BLUE, outline=INK, width=12)
    draw.rectangle((1000, 182, 1168, 402), fill=YELLOW, outline=INK, width=12)
    draw.rectangle((846, 402, 1168, 598), fill=RED, outline=INK, width=12)
    image.paste(draw_mark(160).convert("RGB"), (72, 72))
    draw.text((270, 86), "Flowmatic", fill=INK, font=font(104, bold=True))
    draw.text((76, 290), "Manufacturing Intelligence", fill=INK, font=font(66, bold=True))
    draw.text((78, 406), "Motion → Event → Decision → Action", fill=INK, font=font(40, bold=True))
    draw.text((78, 514), DISPLAY_URL, fill=INK, font=font(32, bold=True))
    return image


def main() -> None:
    BRAND.mkdir(parents=True, exist_ok=True)
    (BRAND / "flowmatic-logo-mark.svg").write_text(svg_mark(), encoding="utf-8")
    draw_mark(1024).save(BRAND / "flowmatic-logo-mark.png", optimize=True)
    (BRAND / "flowmatic-logo-horizontal.svg").write_text(horizontal_svg(), encoding="utf-8")
    horizontal_png().save(BRAND / "flowmatic-logo-horizontal.png", optimize=True)
    draw_mark(256).save(BRAND / "flowmatic-favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    for size, filename in (
        (180, "apple-touch-icon.png"),
        (192, "android-chrome-192x192.png"),
        (512, "android-chrome-512x512.png"),
    ):
        icon = Image.new("RGBA", (size, size), WHITE)
        icon.alpha_composite(draw_mark(size))
        icon.convert("RGB").save(BRAND / filename, optimize=True)
    (BRAND / "flowmatic-qr-contact-signature.svg").write_text(qr_signature_svg(), encoding="utf-8")
    qr_signature_png().save(BRAND / "flowmatic-qr-contact-signature.png", optimize=True)
    (BRAND / "flowmatic-og.svg").write_text(og_svg(), encoding="utf-8")
    og_png().save(BRAND / "flowmatic-og.png", optimize=True)
    (ROOT / "favicon.svg").write_text(svg_mark(64), encoding="utf-8")
    (ROOT / "og-flowmatic.svg").write_text(og_svg(), encoding="utf-8")


if __name__ == "__main__":
    main()
