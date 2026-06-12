# claude-plugin-stats

Daily scrape of Claude Code plugin install stats from Anthropic's public endpoint.

Data source: `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/plugin-stats/plugin-details.json`

Inspired by [Simon Willison's git scraper pattern](https://simonwillison.net/2020/Oct/9/git-scraping/).

## Files

- `plugin-details.json` — latest snapshot
- `.github/workflows/scrape.yml` — daily fetch + commit

