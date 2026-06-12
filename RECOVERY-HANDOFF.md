# Handoff: Recovering Historical Arq Backup Data for claude-plugin-stats

## Goal
Backfill the git repository `https://github.com/prime-radiant-inc/claude-plugin-stats` with historical snapshots of `plugin-details.json`, recovered from Arq 7 backups. The file is currently scraped daily going forward; we want to recover ~1 year of prior history.

## Source File
`~/.claude/plugins/plugin-catalog-cache.json` on Jesse's M4 Max MacBook Pro. This file is fetched from Anthropic's servers and contains `unique_installs` counts per Claude Code plugin.

The live public endpoint (for daily scraping going forward) is:
`https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/plugin-stats/plugin-details.json`

## Arq Backup Details
- **Tool**: Arq 7 on macOS
- **Backend**: AWS S3
- **Bucket**: `arq-m4max-mbp` (us-west-2)
- **Backup plan UUID**: `35490EA4-2A55-45FD-9F8B-0967A00A3D6B`
- **Backup folder UUID**: `3C00C34E-B63F-4DDC-9591-541FEE1A4E23`
- **Snapshots available**: 1,171 records from Dec 2024 through Jun 2026, often multiple per day
- **AWS profile**: `personal` in `~/.aws/credentials` — has full access to the bucket
- **Encryption**: backups ARE encrypted (`isEncrypted: true` in backupconfig.json)

Snapshot records are at:
`s3://arq-m4max-mbp/35490EA4-2A55-45FD-9F8B-0967A00A3D6B/backupfolders/3C00C34E-B63F-4DDC-9591-541FEE1A4E23/backuprecords/`

Filenames are Unix epoch timestamps, e.g. `00178/1206423.backuprecord`.

## Tools Investigated

### arq_restore (open source, https://github.com/arqbackup/arq_restore)
- Built from source at `/tmp/arq_restore`, patched binary at `~/bin/arq_restore_patched`
- Two patches applied to source:
  1. Skip (not crash) on unparseable buckets in `listcomputers`
  2. Accept optional bucket name as 6th arg to `addtarget aws`
- **Status**: `listcomputers` works (finds the plan). `listfolders` fails because the saved target uses the us-east-1 endpoint; bucket is in us-west-2. Also — backups are encrypted, so `restore` will require the Arq encryption password.
- Target configured as `arq-aws` pointing at `arq-m4max-mbp`

### arqreader
- Bundled with Arq 7 at `/Applications/Arq.app/Contents/Resources/ArqAgent.app/Contents/Resources/arqreader`
- Specifically built for Arq 7 format — likely the right tool
- **Status**: Not yet properly explored; hangs/produces massive output when run without args

### arqc
- `/Applications/Arq.app/Contents/Resources/arqc` — official CLI, manages the running Arq daemon
- Cannot restore files; only manages backup plans/status

## What Needs to Happen
1. Figure out the right invocation for `arqreader` (or fix the `arq_restore` endpoint issue) to restore individual snapshots of `~/.claude/plugins/plugin-catalog-cache.json`
2. The Arq **encryption password** will be needed — Jesse knows it and can provide it interactively
3. Script the restore loop: for each snapshot date (ideally one per day, deduped), restore the file to a temp path
4. For each restored snapshot, extract the JSON and commit it to `~/git/prime-radiant-inc/claude-plugin-stats/` with the snapshot date as the commit date
5. Push the backfilled history to GitHub

## Git Repo
`~/git/prime-radiant-inc/claude-plugin-stats/` — already initialized with today's data as the first commit. Backfilled commits should be inserted with correct historical dates using `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE`.
