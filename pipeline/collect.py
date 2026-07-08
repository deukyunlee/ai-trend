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
from collectors.lobsters import fetch as fetch_lobsters
from collectors.huggingface import fetch as fetch_huggingface


def collect(
    sources: list[str] | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[dict]:
    sources = sources or ["hn", "arxiv", "lobsters", "huggingface"]
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

    if "lobsters" in sources:
        print("Fetching Lobste.rs (tag=ai)...", flush=True)
        lobsters_items = fetch_lobsters()
        items += lobsters_items
        print(f"  -> {len(lobsters_items)} items")

    if "huggingface" in sources:
        print("Fetching HuggingFace Papers...", flush=True)
        hf_items = fetch_huggingface()
        items += hf_items
        print(f"  -> {len(hf_items)} items")

    return items


SEEN_CACHE = OUTPUT / "seen_ids.json"


def _load_seen_ids() -> set[str]:
    if not SEEN_CACHE.exists():
        return set()
    try:
        return set(json.loads(SEEN_CACHE.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, TypeError):
        return set()


def _save_seen_ids(seen: set[str]) -> None:
    tmp = SEEN_CACHE.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(sorted(seen), ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, SEEN_CACHE)


NEUTRAL_SCORE = 0.5


def add_normalized_scores(items: list[dict]) -> list[dict]:
    """소스별로 score를 0~1 범위로 min-max 정규화해 normalized_score 필드를 채운다.

    소스마다 점수 척도가 다르므로(HN 수백, HF 수십, Lobste.rs 한 자릿수,
    arXiv 점수 없음) 그대로 비교하면 HN이 항상 상단을 독식한다.
    소스 그룹 내에서 상대 순위로 환산해 공정하게 랭킹한다.

    - 점수가 없는 소스(arXiv) 또는 그룹 내 점수가 모두 동일 → NEUTRAL_SCORE
    """
    by_source: dict[str, list[dict]] = {}
    for item in items:
        by_source.setdefault(item["source"], []).append(item)

    for group in by_source.values():
        scores = [i["score"] for i in group if isinstance(i.get("score"), (int, float))]
        if not scores:
            for i in group:
                i["normalized_score"] = NEUTRAL_SCORE
            continue
        lo, hi = min(scores), max(scores)
        span = hi - lo
        for i in group:
            raw = i.get("score")
            if not isinstance(raw, (int, float)) or span == 0:
                i["normalized_score"] = NEUTRAL_SCORE
            else:
                i["normalized_score"] = round((raw - lo) / span, 3)

    return items


def save(items: list[dict], date_str: str | None = None) -> Path:
    date_str = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    out_path = OUTPUT / f"{date_str}.json"

    existing = []
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            backup = out_path.with_suffix(".bak.json")
            out_path.rename(backup)
            print(f"Warning: {out_path.name} was malformed, backed up to {backup.name}", flush=True)

    seen_ids = _load_seen_ids() | {i["id"] for i in existing}
    new_items = [i for i in items if i["id"] not in seen_ids]
    all_items = add_normalized_scores(existing + new_items)

    tmp_path = out_path.with_suffix(".tmp.json")
    tmp_path.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp_path, out_path)  # atomic overwrite

    _save_seen_ids(seen_ids | {i["id"] for i in new_items})
    print(f"\nSaved {len(new_items)} new items -> {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="저장 날짜 (YYYY-MM-DD). 기본값: 오늘")
    parser.add_argument("--from-date", help="arXiv 수집 시작 날짜 (YYYY-MM-DD)")
    parser.add_argument("--to-date", help="arXiv 수집 종료 날짜 (YYYY-MM-DD)")
    parser.add_argument("--sources", nargs="*", help="수집 소스 (hn, arxiv, lobsters, huggingface)")
    args = parser.parse_args()

    items = collect(args.sources, from_date=args.from_date, to_date=args.to_date)
    path = save(items, args.date)

    print(f"\n=== Collected {len(items)} items -> {path.name} ===")
    for item in items[:5]:
        print(f"[{item['source']:12s}] {item['title'][:80]}")
