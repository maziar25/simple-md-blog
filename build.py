#!/usr/bin/env python3
"""
Simple static site builder:
- Reads Markdown files from content/
- Parses YAML frontmatter (between --- markers)
- Renders post pages and index using Jinja2 templates
- Copies static/ into site/static/
"""
import os
import shutil
import glob
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

ROOT = os.path.abspath(os.path.dirname(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
TEMPLATES_DIR = os.path.join(ROOT, "templates")
STATIC_DIR = os.path.join(ROOT, "static")
OUTPUT_DIR = os.path.join(ROOT, "site")

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

def parse_markdown_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            # parts[1] is YAML frontmatter
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].lstrip("\n")
    html = markdown.markdown(body, extensions=["fenced_code", "codehilite"])
    return meta, html

def slug_from_meta(meta, filename):
    if "slug" in meta:
        return meta["slug"]
    base = os.path.splitext(os.path.basename(filename))[0]
    return base

def build():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    posts = []
    for path in sorted(glob.glob(os.path.join(CONTENT_DIR, "*.md")), reverse=True):
        meta, html = parse_markdown_file(path)
        filename = os.path.basename(path)
        slug = slug_from_meta(meta, filename)
        title = meta.get("title", slug)
        date_str = meta.get("date", None)
        # expect date in YYYY-MM-DD or ISO; fallback to file mtime
        try:
            if date_str:
                date = datetime.fromisoformat(date_str)
            else:
                date = datetime.fromtimestamp(os.path.getmtime(path))
        except Exception:
            date = datetime.fromtimestamp(os.path.getmtime(path))
        output_subdir = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(output_subdir, exist_ok=True)

        # render post
        tmpl = env.get_template("post.html")
        rendered = tmpl.render(title=title, date=date, content=html, meta=meta, slug=slug)
        with open(os.path.join(output_subdir, "index.html"), "w", encoding="utf-8") as f:
            f.write(rendered)

        posts.append({"title": title, "date": date, "slug": slug, "meta": meta})

    # sort posts by date desc
    posts.sort(key=lambda p: p["date"], reverse=True)

    # render index
    index_tmpl = env.get_template("index.html")
    index_html = index_tmpl.render(posts=posts)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # copy static
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, os.path.join(OUTPUT_DIR, "static"))

    print("Built site into", OUTPUT_DIR)

if __name__ == "__main__":
    build()
