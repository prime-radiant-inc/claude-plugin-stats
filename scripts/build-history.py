#!/usr/bin/env python3
"""Walk the git history of the install-count files and emit docs/data.json.

Handles all three formats that have held the data over time:
  install-counts-cache.json   {"fetchedAt", "counts": [{"plugin", "unique_installs"}]}
  plugin-catalog-cache.json   {"fetchedAt", "catalog": {"plugins": {name: {"unique_installs"}}}}
  plugin-details.json         {"installs_generated_at", "plugins": {name: {"unique_installs"}}}

Output: {"generated": iso8601, "plugins": {name: [[YYYY-MM-DD, installs], ...]}}
One point per plugin per day (last write wins).
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FILES = ["install-counts-cache.json", "plugin-catalog-cache.json", "plugin-details.json"]


def snapshot_counts(blob):
    """Return (date, {plugin: installs}) for any of the three formats."""
    data = json.loads(blob)
    if "counts" in data:
        date = data["fetchedAt"]
        counts = {c["plugin"]: c["unique_installs"] for c in data["counts"]}
    elif "catalog" in data:
        date = data["fetchedAt"]
        counts = {name: p["unique_installs"]
                  for name, p in data["catalog"]["plugins"].items()
                  if "unique_installs" in p}
    elif "plugins" in data:
        date = data.get("installs_generated_at") or data["generated_at"]
        counts = {name: p["unique_installs"]
                  for name, p in data["plugins"].items()
                  if "unique_installs" in p}
    else:
        raise ValueError("unrecognized format")
    return date[:10], counts


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args],
                          capture_output=True, text=True, check=True).stdout


def main():
    series = {}  # plugin -> {date: installs}
    for fname in FILES:
        commits = git("log", "--format=%H", "--", fname).split()
        for commit in commits:
            try:
                blob = git("show", f"{commit}:{fname}")
                date, counts = snapshot_counts(blob)
            except (subprocess.CalledProcessError, ValueError, KeyError) as e:
                print(f"skipping {commit[:8]}:{fname}: {e}", file=sys.stderr)
                continue
            for plugin, installs in counts.items():
                series.setdefault(plugin, {})[date] = installs

    out = {
        "generated": git("log", "-1", "--format=%cI").strip(),
        "plugins": {p: sorted(d.items()) for p, d in sorted(series.items())},
    }
    dest = REPO / "docs" / "data.json"
    dest.parent.mkdir(exist_ok=True)
    with open(dest, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    npoints = sum(len(v) for v in series.values())
    print(f"wrote {dest}: {len(series)} plugins, {npoints} points", file=sys.stderr)


if __name__ == "__main__":
    main()
