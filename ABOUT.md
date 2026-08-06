# claude-plugin-stats

> Daily git-scraper of Claude Code plugin install counts, with history recovered back to December 2025 and an interactive chart.

**Family:** plugins · **Type:** tool · **Lifecycle:** production · **Owner:** obra

## What it does
A GitHub Action fetches Anthropic's public `plugin-details.json` install-stats endpoint daily and commits it when it changes (Simon Willison's git-scraper pattern), then regenerates `docs/data.json` from the full git history to feed an ECharts chart on GitHub Pages. History before the June 2026 scrape start was recovered from encrypted Arq 7 backups in S3 (including Glacier thaws) and committed with original `fetchedAt` timestamps; the process is documented in RECOVERY-HANDOFF.md.

## How it fits
- Depends on: —
- Used by: —
- External: Anthropic public plugin-stats endpoint (storage.googleapis.com), GitHub Actions, GitHub Pages, obra/arq_restore (recovery tooling)

## Runtime & data
- Runs: GitHub Actions (daily scrape workflow) + GitHub Pages (static chart)
- Data in: Anthropic plugin-stats JSON; historical Arq backup snapshots (one-time recovery)
- Data out: committed snapshots (`plugin-details.json` and frozen cache formats), `docs/data.json` chart series

## Links
- [Interactive chart](https://primeradiant.com/claude-plugin-stats/)

<!-- Maintained by the maintaining-project-map skill. Do not hand-edit; regenerated. -->
