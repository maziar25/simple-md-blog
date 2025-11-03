#!/usr/bin/env python3
import sys
import os
from datetime import datetime
import slugify  # optional; we'll provide fallback

ROOT = os.path.abspath(os.path.dirname(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")

def slugify_simple(s):
    # very small slugifier (no external dep)
    import re
    s = s.lower()
    s = re.sub(r'[^a-z0-9\- ]', '', s)
    s = s.replace(' ', '-')
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def create_post(title):
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify_simple(title)
    filename = f"{date}-{slug}.md"
    path = os.path.join(CONTENT_DIR, filename)
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR)
    if os.path.exists(path):
        print("File already exists:", path)
        return
    template = f"""---
title: "{title}"
date: {date}
tags: []
---
# {title}

اولین پاراگراف نوشته را اینجا بنویسید.

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(template)
    print("Created:", path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_post.py \"My Title\"")
        sys.exit(1)
    create_post(sys.argv[1])
