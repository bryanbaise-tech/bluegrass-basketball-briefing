# Briefing theme — porting guide

This is a self-contained Jekyll theme in the Lankford Legends style: a serif
display face, monospace uppercase section labels with rules, inline-anchor
links, and clean stat tables. It does not depend on Minima's layouts or
includes even though `theme: minima` remains in `_config.yml` (kept only so the
`minima` gem resolves; our layouts fully override it).

## What the theme is made of

```
_layouts/
  default.html   Base shell: <head> with fonts + CSS, header nav, footer.
  post.html      Renders a post: <h1> title + the post body.
  page.html      Static pages (About).
  home.html      Homepage: intro + reverse-chronological post list.
assets/css/
  style.css      The entire look. One file. No preprocessor.
```

## Why it "just works" with the pipeline output

The generator emits markdown with a fixed structure, and the CSS styles that
structure directly. Nothing in the layout parses game data.

| Markdown the pipeline writes | Rendered element | Styled as |
| --- | --- | --- |
| `## Score and Data for ...` | `<h2>` | uppercase mono section label + rule |
| `### Line Score` | `<h3>` | italic serif sub-head |
| `| Team | 1H | ... |` table | `<table>` | mono headers, tabular-nums, hairlines |
| `[Aberdeen](url) scored 17` | `<a>` | accent-colored inline citation |

So a game-day post and an off-season post both render correctly with zero
per-post styling.

## Porting to another briefing site (e.g. a different team or sport)

1. Copy `_layouts/`, `assets/css/style.css`, and this file into the new site
   repo.
2. In `assets/css/style.css`, edit only the `:root` block at the top:
   - `--accent` / `--accent-hover`: the team's link color.
   - `--font-display` / `--font-body` / `--font-label`: swap fonts if desired
     (and update the Google Fonts `<link>` in `_layouts/default.html` to match).
3. In `_config.yml`, set `title:` and `description:` to the new site's name.
4. Make sure the Gemfile keeps `jekyll-feed` and `jekyll-seo-tag` (the layout
   calls `{% feed_meta %}` and `{% seo %}`). If you drop those plugins, delete
   those two lines from `_layouts/default.html`.
5. Point the generator at the new repo (`site_repo_path` in its `config.yaml`)
   and the new markdown will render in this theme automatically.

The accent color is the one deliberate brand decision. Everything else is
structural and carries over unchanged.

## Current brand values

- Accent: `#0033a0` (Kentucky blue) in light mode, `#6ea8ff` in dark.
- Display: Roboto Slab. Body: Inter. Labels: JetBrains Mono.
