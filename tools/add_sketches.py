#!/usr/bin/env python3
"""
Add new sketches to Mami's Musings.

  1. Drop new photos (e.g. from WhatsApp) into the  inbox/  folder.
  2. Run:   python3 tools/add_sketches.py
  3. Open the new files in _musings/ and type the Tamil caption + message.

For each photo it:
  * skips exact duplicates (moved to _duplicates/),
  * moves it to assets/images/sketches/sketch-NNN.jpg,
  * makes a small thumbnail in assets/images/thumbs/,
  * creates _musings/NNN.md ready for the Tamil text.

Needs Pillow:  python3 -m pip install pillow
"""
import hashlib, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT    = Path(__file__).resolve().parent.parent
INBOX   = ROOT / "inbox"
SKETCH  = ROOT / "assets/images/sketches"
THUMB   = ROOT / "assets/images/thumbs"
MUSINGS = ROOT / "_musings"
DUPES   = ROOT / "_duplicates"
EXTS    = {".jpg", ".jpeg", ".png", ".webp"}
THUMB_WIDTH = 600

STUB = """---
order: {n}
publish_on:        # when it goes live (India time), e.g. "2026-10-25 07:30" — empty = draft
image: /assets/images/sketches/{img}
thumb: /assets/images/thumbs/{img}
caption: ""        # Tamil title, e.g. "கடந்த காலத்தின் இசை"
caption_en: ""     # optional English title
---
<!-- மாமியின் செய்தியை இங்கே தமிழில் எழுதுங்கள் / Write Mami's message below, in Tamil -->
"""

def md5(p): return hashlib.md5(p.read_bytes()).hexdigest()

def main():
    for d in (SKETCH, THUMB, MUSINGS, DUPES, INBOX): d.mkdir(parents=True, exist_ok=True)
    seen = {md5(p) for p in SKETCH.iterdir() if p.suffix.lower() in EXTS}
    nums = [int(m.group(1)) for p in MUSINGS.glob("*.md") if (m := re.match(r"(\d+)", p.stem))]
    n = max(nums, default=0)

    new = sorted(p for p in INBOX.iterdir() if p.suffix.lower() in EXTS)
    if not new:
        print("inbox/ is empty — nothing to add."); return
    added = dup = 0
    for src in new:
        h = md5(src)
        if h in seen:
            shutil.move(str(src), DUPES / src.name); dup += 1; continue
        seen.add(h); n += 1
        ext = ".png" if src.suffix.lower() == ".png" else ".jpg" if src.suffix.lower() in {".jpg", ".jpeg"} else src.suffix.lower()
        img = f"sketch-{n:03d}{ext}"
        dest = SKETCH / img
        shutil.move(str(src), dest)
        with Image.open(dest) as im:
            im = ImageOps.exif_transpose(im)
            im.thumbnail((THUMB_WIDTH, THUMB_WIDTH * 2))
            if im.mode not in ("RGB", "L") and ext == ".jpg": im = im.convert("RGB")
            im.save(THUMB / img, quality=80, optimize=True)
        (MUSINGS / f"{n:03d}.md").write_text(STUB.format(n=n, img=img), encoding="utf-8")
        added += 1
    print(f"Added {added} sketch(es); {dup} duplicate(s) moved to _duplicates/. Last number: {n:03d}")

if __name__ == "__main__":
    main()
