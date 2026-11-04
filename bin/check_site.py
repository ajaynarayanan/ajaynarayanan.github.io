#!/usr/bin/env python3
"""Check internal page links and assets in the generated Jekyll site."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            self.links.extend(
                item.strip().split()[0]
                for item in attrs["srcset"].split(",")
                if item.strip()
            )


def check_site(root, site_url):
    if not (root / "index.html").is_file():
        print(f"Missing homepage: {root / 'index.html'}")
        return 1

    site = urlsplit(site_url)
    errors = set()
    pages = [
        path for path in root.rglob("*.html")
        if "assets" not in path.relative_to(root).parts
    ]
    for path in pages:
        relative_path = path.relative_to(root)
        parser = PageLinks()
        parser.feed(path.read_text(encoding="utf-8"))
        page_url = urljoin(site_url.rstrip("/") + "/", relative_path.as_posix())
        for link in parser.links:
            target = urlsplit(urljoin(page_url, link))
            if target.scheme not in ("http", "https") or target.netloc != site.netloc:
                continue
            local_path = root / unquote(target.path.lstrip("/"))
            if not (local_path.is_file() or (local_path / "index.html").is_file()):
                errors.add(f"{relative_path}: missing {target.path}")

    for error in sorted(errors):
        print(error)
    print(f"Checked {len(pages)} generated pages; {len(errors)} broken internal links.")
    return int(bool(errors))


if __name__ == "__main__":
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("directory", type=Path)
    arguments.add_argument("--site-url", default="https://ajaynarayanan.github.io/")
    args = arguments.parse_args()
    raise SystemExit(check_site(args.directory.resolve(), args.site_url))
