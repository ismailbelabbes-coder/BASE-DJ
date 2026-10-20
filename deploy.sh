#!/usr/bin/env bash
# Construye y publica la demo de BaseDJ en Cloudflare Pages (propuesta-basedj.pages.dev).
set -euo pipefail
cd "$(dirname "$0")"
python -I build.py
rm -f dist/app.css
DIR="$PWD/dist"
cd "${TMPDIR:-/tmp}"
npx --yes wrangler@4 pages project create propuesta-basedj --production-branch main --force 2>/dev/null || true
npx --yes wrangler@4 pages deploy "$DIR" --project-name propuesta-basedj --branch main --commit-dirty=true
