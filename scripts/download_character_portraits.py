#!/usr/bin/env python3
"""Fetch character portraits from Jujutsu Kaisen fandom pages and save them as WebP under static/images."""

from __future__ import annotations

import re
import sys
import time
from io import BytesIO
from pathlib import Path

try:
    import cloudscraper
except ImportError:
    print("Install cloudscraper: pip install cloudscraper", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)

from data.characters_py import characters

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "static" / "images"
UA = "jjk-static-gallery/1.0 (local Flask demo; cloudscraper)"

FALLBACK_SOURCES: dict[str, str] = {
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

META_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
INFBOX_IMAGE_RE = re.compile(
    r'<figure[^>]+class=["\"][^"\"]*pi-item pi-image[^"\"]*["\"][\s\S]*?<img[^>]+src=["\']([^"\']+)["\']',
    re.I,
)


def fetch(url: str) -> bytes:
    scraper = cloudscraper.create_scraper(browser={"custom": UA})
    resp = scraper.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content


def save_webp(raw: bytes, dest: Path) -> None:
    im = Image.open(BytesIO(raw))
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=86, method=6)


def get_wiki_image_url(page_url: str) -> str:
    scraper = cloudscraper.create_scraper(browser={"custom": UA})
    resp = scraper.get(page_url, timeout=60)
    resp.raise_for_status()
    html = resp.text
    match = META_IMAGE_RE.search(html)
    if match:
        url = match.group(1)
        return url if url.startswith("http") else "https:" + url
    match = INFBOX_IMAGE_RE.search(html)
    if match:
        url = match.group(1)
        return url if url.startswith("http") else "https:" + url
    raise ValueError("Could not find fandom portrait URL on page")


def get_character_image_url(char: dict[str, object]) -> str:
    page_url = char.get("imageCredit")
    if isinstance(page_url, str) and "fandom.com" in page_url:
        try:
            return get_wiki_image_url(page_url)
        except Exception as exc:
            print(f"  warning: failed to parse fandom page for {char['id']}: {exc}")
    fallback = FALLBACK_SOURCES.get(Path(char["image"]).name)
    if fallback:
        print(f"  using fallback source for {char['id']}")
        return fallback
    raise ValueError(f"No image source available for {char['id']}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for char in characters:
        dest = OUT_DIR / Path(char["image"]).name
        print(f"{char['id']} -> {dest.name}")
        try:
            src_url = get_character_image_url(char)
            raw = fetch(src_url)
            save_webp(raw, dest)
            print(f"  wrote {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KiB)")
        except Exception as exc:
            print(f"  error: {exc}")
        time.sleep(0.6)


if __name__ == "__main__":
    main()
