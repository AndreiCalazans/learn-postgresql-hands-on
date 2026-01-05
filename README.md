# PostgreSQL in 36 Lessons (Hugo + Vercel)

This repository hosts a Hugo static site with 36 hands-on PostgreSQL CLI challenges. Each lesson is a five-minute, self-contained task grouped into three levels: platform fundamentals, common mistakes, and engine internals.

## Repo layout

- `content/lessons/level-1|2|3/`: Lesson Markdown files (one page per task).
- `content/_index.md`: Landing page with guidance and recap prompts.
- `layouts/`: Minimal Hugo templates for single pages and lists.
- `scripts/generate_lessons.py`: Helper used to generate the lesson Markdown from structured data.
- `hugo.toml`: Site configuration and permalinks.
- `vercel.json`: Vercel build configuration (uses Hugo output in `public/`).

## Local development

1. Install **Hugo Extended** (v0.154.2 or newer). On macOS: `brew install hugo`.
2. From the repo root, run `npm run dev` to start a local server.
3. Run `npm run build` to produce the static site in `public/`.

> Note: The container environment used to author this change could not download Hugo binaries. Ensure Hugo is available locally before running the commands above.

## Deploying to Vercel

- The included `vercel.json` sets `HUGO_VERSION` and uses `npm run vercel-build` as the build command.
- Output directory is `public/`.
- Add the project in Vercel and deploy; no external services are required.

Happy shipping!
