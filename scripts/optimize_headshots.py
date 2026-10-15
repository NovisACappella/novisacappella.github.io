#!/usr/bin/env python3
"""Shrink member headshots for the website.

For every image under img/headshots/ (any folder), this:
  - rotates it upright using the photo's orientation tag,
  - converts its colors to standard sRGB (iPhone photos use "Display P3"),
  - shrinks it to fit inside 600x800 pixels (never enlarges),
  - removes hidden metadata (camera info, GPS location),
  - saves it as a lowercase .jpg (f26-Ian.JPG -> f26-ian.jpg),
  - and updates any file that mentions the old name (roster .yml files, .html, ...).
Photos that are already done are skipped, so running it twice changes nothing.

Run by the "Optimize headshots" GitHub Action. To run it yourself:
    pip install pillow pillow-heif
    python3 scripts/optimize_headshots.py
"""
import io, os, re, sys
from PIL import Image, ImageOps, ImageCms

try:                                   # lets iPhone .heic photos work too
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADSHOTS = os.path.join(ROOT, "img", "headshots")
MAX_W, MAX_H, QUALITY, MIN_QUALITY, MAX_BYTES = 600, 800, 82, 60, 300 * 1024
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
TEXT_EXT = {".html", ".yml", ".yaml", ".md", ".css", ".js", ".json"}
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))


def canonical(name):
    stem = os.path.splitext(name)[0].lower()
    stem = re.sub(r"[^a-z0-9_-]+", "-", stem).strip("-")
    return re.sub(r"-+", "-", stem) + ".jpg"


def already_done(path):
    # No size test here: optimize() already keeps files small, and a size test would make
    # an unusually grainy photo get re-compressed (and re-committed) on every run.
    with Image.open(path) as im:
        return (im.format == "JPEG" and im.width <= MAX_W and im.height <= MAX_H
                and "icc_profile" not in im.info and not im.getexif())


def optimize(src, dst):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        icc = im.info.get("icc_profile")
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.getchannel("A"))
            im = bg
        else:
            im = im.convert("RGB")
        if icc:
            im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB")
        im.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
        tmp = dst + ".tmp"
        try:
            quality = QUALITY
            while True:   # lower the quality a little if a very grainy photo comes out too big
                im.save(tmp, "JPEG", quality=quality, optimize=True, progressive=True)
                if os.path.getsize(tmp) <= MAX_BYTES or quality <= MIN_QUALITY:
                    break
                quality -= 6
            os.replace(tmp, dst)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)


def main():
    renames, errors, report = [], 0, []
    for folder, _, files in os.walk(HEADSHOTS):
        for name in sorted(files):
            if os.path.splitext(name)[1].lower() not in IMAGE_EXT:
                continue
            src = os.path.join(folder, name)
            dst = os.path.join(folder, canonical(name))
            rel = os.path.relpath(src, ROOT)
            try:
                if src == dst and already_done(src):
                    continue
                if src != dst and os.path.exists(dst):
                    print(f"::error file={rel}::Would be renamed to {os.path.basename(dst)}, but that file already exists. Delete one of them.")
                    errors += 1
                    continue
                before = os.path.getsize(src)
                optimize(src, dst)
                if src != dst:
                    os.remove(src)
                    renames.append((name, os.path.basename(dst)))
                report.append(f"| `{os.path.relpath(dst, ROOT)}` | {before // 1024} KB | {os.path.getsize(dst) // 1024} KB |")
            except Exception as e:  # unreadable or unsupported file
                print(f"::error file={rel}::Could not process this image ({e}). Re-export it as a JPG and upload again.")
                errors += 1

    # Point every page and roster file at the new names (whole-name matches only).
    for old, new in renames:
        pattern = re.compile(r"(?<![A-Za-z0-9_.-])" + re.escape(old) + r"(?![A-Za-z0-9_-])")
        for folder, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "_site", "node_modules", "vendor")]
            for f in files:
                if os.path.splitext(f)[1].lower() in TEXT_EXT:
                    p = os.path.join(folder, f)
                    text = open(p, encoding="utf-8", errors="ignore").read()
                    if pattern.search(text):
                        open(p, "w", encoding="utf-8").write(pattern.sub(new, text))
                        print(f"Updated references in {os.path.relpath(p, ROOT)}: {old} -> {new}")

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    lines = ["| File | Before | After |", "|---|---|---|"] + report if report else ["All headshots were already optimized."]
    print("\n".join(lines))
    if summary:
        with open(summary, "a") as fh:
            fh.write("\n".join(lines) + "\n")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
