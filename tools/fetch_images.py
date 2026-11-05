"""
Download the images from the old Google Sites portfolio into assets/img/.

Version 2: instead of using saved image links (which Google rejected with
403 Forbidden), this opens each live Google Sites page, grabs the image links
it's serving right now, and downloads them the way a browser would.

Run it from anywhere, while the Google Site is still published:

    python tools/fetch_images.py

Files that already exist are skipped, so it's safe to run again.
"""

import html
import pathlib
import re
import urllib.request

SITE = "https://www.derrickzhao.com"

# Page on the old site -> where each image on that page should go, in the
# order the images appear on the page. None means "skip this one".
PAGES = {
    "/home": ["about.jpg", None, None],
    "/projects/baja-sae/front-upright": [
        "front-upright/hero.jpg",
        "front-upright/assembly.jpg",
        "front-upright/iteration-1.jpg",
        "front-upright/iteration-2.jpg",
        "front-upright/iteration-3.jpg",
        "front-upright/fea-initial.jpg",
        "front-upright/fea-final-1.jpg",
        "front-upright/fea-final-2.jpg",
        "front-upright/fea-final-3.jpg",
        "front-upright/fea-final-4.jpg",
    ],
    "/projects/baja-sae/suspension-arm-fixturing": [
        "h-arm-fixture/hero.jpg",
        "h-arm-fixture/fixture.jpg",
    ],
    "/projects/baja-sae/cvt-coupler-guarding": [
        "cvt-coupler-guard/hero.jpg",
        "cvt-coupler-guard/flat-pattern.jpg",
    ],
    "/projects/improved-quieter-hair-dryer": [
        "fozzle/hero.jpg",
        "fozzle/research.jpg",
        "fozzle/prototype-1.jpg",
        "fozzle/prototype-2.jpg",
        "fozzle/prototype-3.jpg",
        "fozzle/prototype-4.jpg",
        "fozzle/prototype-5.jpg",
        "fozzle/prototype-6.jpg",
    ],
    "/projects/foldable-ball-return-for-early-childhood-development": [
        "rollaroo/hero.jpg",
        "rollaroo/constraints.jpg",
        "rollaroo/prototype-1.jpg",
        "rollaroo/prototype-2.jpg",
        "rollaroo/prototype-3.jpg",
        "rollaroo/prototype-4.jpg",
        "rollaroo/prototype-5.jpg",
    ],
}

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

IMG_RE = re.compile(
    r"https://lh\d+(?:-[a-z]+)?\.googleusercontent\.com/sitesv-images[^\"'\s)<>\\]*"
)


def get(url, referer=None, accept="text/html"):
    headers = {"User-Agent": UA, "Accept": accept, "Accept-Language": "en-US,en;q=0.9"}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def image_links(page_html):
    """Image links in page order, one per image, at a good size."""
    text = html.unescape(page_html).replace("\\u003d", "=").replace("\\u0026", "&")
    seen, links = set(), []
    for url in IMG_RE.findall(text):
        base = url.split("=")[0]          # same image can appear at several sizes
        if base in seen:
            continue
        seen.add(base)
        links.append(base + "=w1600")
    return links


def main():
    img_dir = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
    saved = skipped = 0
    problems = []

    for path, names in PAGES.items():
        page_url = SITE + path
        print(f"\n{page_url}")
        try:
            links = image_links(get(page_url).decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001
            problems.append(f"couldn't open {page_url}: {e}")
            print("  couldn't open page:", e)
            continue

        expected = len(names)
        if len(links) != expected:
            # Order can't be trusted, so save everything numbered for sorting by hand.
            folder = img_dir / "_unsorted" / path.strip("/").replace("/", "_")
            print(f"  found {len(links)} images, expected {expected}; saving to {folder} for you to sort")
            problems.append(f"{path}: sort images in {folder}")
            targets = [folder / f"{i + 1:02d}.jpg" for i in range(len(links))]
        else:
            targets = [img_dir / n if n else None for n in names]

        for url, dest in zip(links, targets):
            if dest is None:
                continue
            if dest.exists():
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                dest.write_bytes(get(url, referer=page_url, accept="image/avif,image/webp,image/*,*/*"))
                saved += 1
                print("  saved ", dest.relative_to(img_dir))
            except Exception as e:  # noqa: BLE001
                problems.append(f"{dest.relative_to(img_dir)}: {e}")
                print("  FAILED", dest.relative_to(img_dir), "-", e)

    print(f"\n{saved} downloaded, {skipped} already there, {len(problems)} problem(s)")
    for p in problems:
        print("  -", p)


if __name__ == "__main__":
    main()
