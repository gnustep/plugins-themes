#!/usr/bin/env python3
"""Build the Darkness file icons (requires CairoSVG and Pillow)."""

from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "Darkness.theme" / "Resources" / "Artwork"
IMAGES = ROOT / "Darkness.theme" / "Resources" / "ThemeImages"

DEFS = """<defs>
  <linearGradient id="front" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#62626e"/><stop offset="1" stop-color="#363640"/>
  </linearGradient>
  <linearGradient id="back" x1="0" y1="0" x2="0" y2="1">
    <stop stop-color="#858591"/><stop offset="1" stop-color="#454550"/>
  </linearGradient>
</defs>"""

FOLDER = """<path d="M5 36V12Q5 10 7 10H18L22 14H40Q42 14 42 16V36Z"
  fill="url(#back)" stroke="#202027" stroke-width="1.5"/>
<path d="M7 13H17L21 17H39" fill="none" stroke="#b2b2bf"/>
<path d="M7 21H43L39 38H4Z" fill="url(#front)"
  stroke="#202027" stroke-width="1.5" stroke-linejoin="round"/>
<path d="M8 23H40M6 36H37" fill="none" stroke="#9292a0" stroke-width="1"/>
"""

# Simple silhouettes remain legible at the native 48-pixel icon size.
BADGES = {
    "Folder": "",
    "HomeDirectory": '<path d="M17 29L23 24L29 29M19 28V34H27V28M22 34V30H24V34"/>',
    "DocsFolder": '<path d="M19 25H25L28 28V34H19ZM25 25V28H28M21 30H25M21 32H25"/>',
    "DownloadFolder": '<path d="M23 24V31M19 28L23 32L27 28M18 32V35H28V32"/>',
    "ApplicationFolder": '<rect x="18" y="25" width="4" height="4" rx=".5"/><rect x="25" y="25" width="4" height="4" rx=".5"/><rect x="18" y="32" width="4" height="3" rx=".5"/><rect x="25" y="32" width="4" height="3" rx=".5"/>',
    "LibraryFolder": '<path d="M18 25V34H20V25ZM23 25V34H25V25ZM28 25L31 33"/>',
    "GSFolder": '<path d="M17 29L23 25L29 29L23 33ZM17 29V33L23 37L29 33V29M23 33V37"/>',
    "ImageFolder": '<rect x="17" y="25" width="13" height="10" rx="1"/><path d="M18 33L22 29L25 32L27 30L29 33"/><circle cx="26" cy="28" r=".7" fill="#e3e3ec" stroke="none"/>',
    "MusicFolder": '<path d="M22 32V26L29 24V31M22 28L29 26"/><ellipse cx="20" cy="33" rx="2" ry="1.5"/><ellipse cx="27" cy="32" rx="2" ry="1.5"/>',
    "VideoFolder": '<rect x="17" y="25" width="14" height="10" rx="1"/><path d="M22 27L27 30L22 33Z"/>',
}

CUBE = """<g stroke="#202027" stroke-width="1.5" stroke-linejoin="round">
  <path d="M24 3L43 14L24 25L5 14Z" fill="#858591"/>
  <path d="M5 14L24 25V45L5 34Z" fill="#51515e"/>
  <path d="M24 25L43 14V34L24 45Z" fill="#30303b"/>
</g>
<path d="M7 14L24 5L41 14M24 26V42" fill="none" stroke="#b4b4c2"/>
<path d="M9 22L19 28M9 25L19 31" fill="none" stroke="#292933" stroke-width="1.5"/>
<path d="M29 30L38 25" fill="none" stroke="#777787" stroke-width="1.5"/>
<path d="M36 33L39 31V34L36 36Z" fill="#d2d2e4"/>
"""

# GWorkspace loads these from FSNode's bundle, so they need bundle-specific
# theme overrides rather than the common_ prefix used by AppKit icons.
DRIVE = """<g stroke="#202027" stroke-width="1.5" stroke-linejoin="round">
  <path d="M4 25L29 10L44 19L19 34Z" fill="url(#back)"/>
  <path d="M4 25L19 34V43L4 34Z" fill="url(#front)"/>
  <path d="M19 34L44 19V28L19 43Z" fill="#30303b"/>
</g>
<path d="M6 25L29 12L41 19M20 35L42 22" fill="none" stroke="#b4b4c2"/>
<path d="M7 30L12 33" fill="none" stroke="#d2d2e4" stroke-width="2"/>
<path d="M23 36L39 27M23 39L39 30" fill="none" stroke="#777787"/>
"""

DRIVE_LID = """<path d="M12 24L28 15L36 20L20 29Z" fill="#62626e"
  stroke="#454550" stroke-linejoin="round"/>
<path d="M17 24L28 18L31 20L20 26Z" fill="#b4b4c2"/>
"""

DRIVE_OPEN = """<g transform="matrix(.866 -.5 .866 .5 24 22)">
  <circle r="9" fill="#30303b" stroke="#202027" stroke-width="1.2"/>
  <circle r="7" fill="#b4b4c2" stroke="#e3e3ec" stroke-width=".8"/>
  <circle r="4.5" fill="none" stroke="#858591" stroke-width=".8"/>
  <circle r="2" fill="#454550" stroke="#e3e3ec" stroke-width=".8"/>
</g>
<path d="M34 20L30 25L24 25" fill="none" stroke="#202027" stroke-width="3"/>
<path d="M34 19L30 24L24 24" fill="none" stroke="#e3e3ec" stroke-width="1.5"/>
"""


def main():
    SOURCES.mkdir(parents=True, exist_ok=True)
    icons = {"Root_PC": CUBE}
    for name, badge in BADGES.items():
        icons[name] = FOLDER + (
            '<g fill="none" stroke="#e3e3ec" stroke-width="1.4" '
            'stroke-linecap="round" stroke-linejoin="round">' + badge + '</g>'
        )
    icons = {f"common_{name}": artwork for name, artwork in icons.items()}
    icons["org.gnustep.FSNode/HardDisk"] = DRIVE + DRIVE_LID
    icons["org.gnustep.FSNode/HardDiskOpen"] = DRIVE + DRIVE_OPEN
    for name, artwork in icons.items():
        source = SOURCES / f"{name}.svg"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" '
            'viewBox="0 0 48 48">\n' + DEFS + '\n' + artwork + '</svg>\n'
        )
        # Keep the existing root filename; the other standard images use .tiff.
        suffix = ".tif" if name == "common_Root_PC" else ".tiff"
        target = IMAGES / (name + suffix)
        target.parent.mkdir(parents=True, exist_ok=True)
        png = cairosvg.svg2png(url=str(source), output_width=192, output_height=192)
        with Image.open(BytesIO(png)) as rendered:
            rendered.convert("RGBA").resize((48, 48), Image.Resampling.LANCZOS).save(
                target, compression="tiff_lzw", dpi=(72, 72)
            )


if __name__ == "__main__":
    main()
