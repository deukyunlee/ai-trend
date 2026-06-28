"""Main collection script — run directly or via /collect skill."""
import json
import sys
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

from collectors.hn import fetch as fetch_hn
from collectors.arxiv import fetch as fetch_arxiv


def collect(sources: list[str] | None = None) -> list[dict]:
    sources = sources or ["hn", "arxiv"]
    items = []

    if "hn" in sources:
        print("Fetching Hacker News...", flush=True)
        items += fetch_hn()
        print(f"  -> {len([i for i in items if i['source'] == 'hackernews'])} items")

    if "arxiv" in sources:
        print("Fetching arXiv...", flush=True)
        arxiv_items = fetch_arxiv()
        items += arxiv_items
        print(f"  -> {len(arxiv_items)} items")

    return items


def save(items: list[dict]) -> Path:
    date_str = datetime.now(UTC).strftime("%Y-%m-%d")
    out_path = OUTPUT / f"{date_str}.json"

    existing = []
    if out_path.exists():
        existing = json.loads(out_path.read_text())

    seen_ids = {i["id"] for i in existing}
    new_items = [i for i in items if i["id"] not in seen_ids]
    all_items = existing + new_items

    out_path.write_text(json.dumps(all_items, ensure_ascii=False, indent=2))
    print(f"\nSaved {len(new_items)} new items -> {out_path}")
    return out_path


if __name__ == "__main__":
    sources = sys.argv[1:] or None
    items = collect(sources)
    path = save(items)

    print(f"\n=== Collected {len(items)} items ===")
    for item in items[:5]:
        print(f"[{item['source']:12s}] {item['title'][:80]}")
