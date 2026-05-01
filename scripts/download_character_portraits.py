#!/usr/bin/env python3
"""Fetch roster portraits from AniList CDN and save as WebP under static/images."""

from __future__ import annotations

import sys
import time
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)

import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "static" / "images"

# AniList character CDN URLs (official promotional artwork mirrored on AniList).
SOURCES: dict[str, str] = {
    "nanami-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b133704-8wLTGjc234q2.png",
    "mahito-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b133702-Y7JRG5vAvjIL.png",
    "kenjaku-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b289584-KndGudJZm5Ik.jpg",
    "hakari-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b197584-fK7Jc6DLfx7e.jpg",
    "kashimo-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b248143-w5ZilMdkvpbe.jpg",
    "yuki-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b196502-aBvtPFr9lGm2.png",
    "todo-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b137975-6TH7PiLWJaqy.png",
    "choso-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b157116-2jYQf3y8NeTZ.png",
    "panda-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b137974-9qnK3DPrvLKh.jpg",
    "hanami-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b172743-4Y5SXqED6A3G.jpg",
    "miwa-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b156848-Rf0tuoQCNyZV.png",
    "mechamaru-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b210154-nIn9DX39GFKP.jpg",
    "dagon-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b204383-5oTlVPpaCnM2.jpg",
    "uro-web.webp": "https://s4.anilist.co/file/anilistcdn/character/large/b283136-NvWh6wRYmFnn.jpg",
}

UA = "jjk-static-gallery/1.0 (local Flask demo; Pillow resize)"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def save_webp(raw: bytes, dest: Path) -> None:
    im = Image.open(BytesIO(raw))
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=86, method=6)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for i, (fname, url) in enumerate(SOURCES.items()):
        if i:
            time.sleep(0.6)
        dest = OUT_DIR / fname
        print(f"{fname} …")
        raw = fetch(url)
        save_webp(raw, dest)
        print(f"  wrote {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
