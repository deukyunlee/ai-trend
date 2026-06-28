"""Main collection script — run directly or via /collect skill."""
import argparse
import json
import os
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

from collectors.hn import fetch as fetch_hn
from collectors.arxiv import fetch as fetch_arxiv


def collect(
    sources: list[str] | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[dict]:
    sources = sources or ["hn", "arxiv"]
    items = []

    if "hn" in sources:
        print("Fetching Hacker News...", flush=True)
        hn_items = fetch_hn()
        items += hn_items
        print(f"  -> {len(hn_items)} items")

    if "arxiv" in sources:
        date_info = f" (from={from_date}, to={to_date})" if from_date or to_date else ""
        print(f"Fetching arXiv{date_info}...", flush=True)
        arxiv_items = fetch_arxiv(from_date=from_date, to_date=to_date)
        items += arxiv_items
        print(f"  -> {len(arxiv_items)} items")

    return items


def save(items: list[dict], date_str: str | None = None) -> Path:
    date_str = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    out_path = OUTPUT / f"{date_str}.json"

    existing = []
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text())
        except json.JSONDecodeError:
            backup = out_path.with_suffix(".bak.json")
            out_path.rename(backup)
            print(f"Warning: {out_path.name} was malformed, backed up to {backup.name}", flush=True)

    seen_ids = {i["id"] for i in existing}
    new_items = [i for i in items if i["id"] not in seen_ids]
    all_items = existing + new_items

    tmp_path = out_path.with_suffix(".tmp.json")
    tmp_path.write_text(json.dumps(all_items, ensure_ascii=False, indent=2))
    os.replace(tmp_path, out_path)  # atomic overwrite
    print(f"\nSaved {len(new_items)} new items -> {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="저장 날짜 (YYYY-MM-DD). 기본값: 오늘")
    parser.add_argument("--from-date", help="arXiv 수집 시작 날짜 (YYYY-MM-DD)")
    parser.add_argument("--to-date", help="arXiv 수집 종료 날짜 (YYYY-MM-DD)")
    parser.add_argument("--sources", nargs="*", help="수집 소스 (hn, arxiv)")
    args = parser.parse_args()

    items = collect(args.sources, from_date=args.from_date, to_date=args.to_date)
    path = save(items, args.date)

    print(f"\n=== Collected {len(items)} items -> {path.name} ===")
    for item in items[:5]:
        print(f"[{item['source']:12s}] {item['title'][:80]}")
