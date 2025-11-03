# Simple Markdown Blog

Minimal static blog generator:
- Write posts as Markdown files in `content/` with YAML frontmatter.
- Run `python create_post.py "My Title"` to create a new post file.
- Run `python build.py` to build `site/`.
- Push to GitHub; GitHub Actions will deploy `site/` to `gh-pages`.

Requirements:
pip install -r requirements.txt

Then:
python create_post.py "My first post"
# edit the created markdown in content/
python build.py
# check site/ directory
