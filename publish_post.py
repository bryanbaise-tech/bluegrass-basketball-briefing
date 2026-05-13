#!/usr/bin/env python3
"""
publish_post.py — Bluegrass Basketball Briefing pipeline helper

Usage:
    python publish_post.py --title "UK Wins Again" --content path/to/content.md
    python publish_post.py --title "UK Wins Again" --body "Full markdown body here"

This script:
  1. Writes the markdown file to _posts/ with a Jekyll-compatible filename
  2. Runs git add, commit, and push
  3. GitHub Actions then builds and deploys the site automatically

Requirements:
    pip install python-frontmatter
    git must be configured with commit access to the repo
"""

import argparse
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
import re


def slugify(title: str) -> str:
    """Convert a title string to a URL-safe slug."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug


def write_post(title: str, body: str, category: str = "news", author: str = "bryanbaise-tech") -> Path:
    """Write a Jekyll post markdown file to _posts/ and return its path."""
    today = date.today()
    slug = slugify(title)
    filename = f"{today.strftime('%Y-%m-%d')}-{slug}.md"
    posts_dir = Path(__file__).parent / "_posts"
    posts_dir.mkdir(exist_ok=True)
    filepath = posts_dir / filename

    post_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")
    frontmatter = f"""---
layout: post
title: "{title}"
date: {post_dt}
categories: {category}
author: {author}
---

"""
    filepath.write_text(frontmatter + body, encoding="utf-8")
    print(f"[publish_post] Wrote: {filepath}")
    return filepath


def git_commit_and_push(filepath: Path, title: str) -> None:
    """Stage the file, commit, and push to origin/main."""
    repo_root = Path(__file__).parent

    def run(cmd):
        result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ERROR running {' '.join(cmd)}:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)
        return result.stdout.strip()

    run(["git", "add", str(filepath)])
    commit_msg = f"Add post: {title}"
    run(["git", "commit", "-m", commit_msg])
    run(["git", "push", "origin", "main"])
    print(f"[publish_post] Committed and pushed: {commit_msg}")


def main():
    parser = argparse.ArgumentParser(description="Publish a new Jekyll post to the Bluegrass Basketball Briefing.")
    parser.add_argument("--title", required=True, help="Post title")
    parser.add_argument("--body", default="", help="Post body in Markdown (inline)")
    parser.add_argument("--content", default="", help="Path to a .md file containing the post body")
    parser.add_argument("--category", default="news", help="Jekyll category (default: news)")
    parser.add_argument("--author", default="bryanbaise-tech", help="Post author")
    args = parser.parse_args()

    if args.content:
        body = Path(args.content).read_text(encoding="utf-8")
    elif args.body:
        body = args.body
    else:
        print("ERROR: Provide --body or --content", file=sys.stderr)
        sys.exit(1)

    filepath = write_post(args.title, body, args.category, args.author)
    git_commit_and_push(filepath, args.title)
    print("[publish_post] Done! GitHub Actions will build and deploy the site shortly.")


if __name__ == "__main__":
    main()
