"""arXiv collector — fetches AI/agent papers, optionally filtered by date range."""
import urllib.error
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, UTC

ARXIV_API = "https://export.arxiv.org/api/query"
NS = "http://www.w3.org/2005/Atom"

QUERIES = [
    "ti:agentic+loop",
    "ti:LLM+agent",
    "ti:harness+agent",
    "ti:multi-agent",
    "ti:tool+use+LLM",
]


def _date_range_filter(from_date: str | None, to_date: str | None) -> str | None:
    """arXiv submittedDate range filter 문자열 생성.

    from_date / to_date: YYYY-MM-DD 형식
    Lucene range 문법은 TO 전후로 공백 필요 — urlencode가 공백을 %20으로 인코딩해야 올바르게 동작.
    """
    if not from_date and not to_date:
        return None
    from_str = from_date.replace("-", "") + "0000" if from_date else "000000000000"
    to_str = to_date.replace("-", "") + "2359" if to_date else "999999999999"
    return f"submittedDate:[{from_str} TO {to_str}]"


def fetch(
    max_per_query: int = 5,
    from_date: str | None = None,
    to_date: str | None = None,
) -> list[dict]:
    """
    Args:
        max_per_query: 쿼리당 최대 결과 수
        from_date: 시작 날짜 (YYYY-MM-DD). None이면 제한 없음.
        to_date: 종료 날짜 (YYYY-MM-DD). None이면 제한 없음.
    """
    date_filter = _date_range_filter(from_date, to_date)
    results = []
    seen = set()

    for query in QUERIES:
        full_query = f"({query}) AND {date_filter}" if date_filter else query
        params = urllib.parse.urlencode({
            "search_query": full_query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": max_per_query,
        })
        url = f"{ARXIV_API}?{params}"
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                tree = ET.fromstring(r.read())
        except urllib.error.URLError as e:
            print(f"arXiv fetch failed for query '{query}': {e}", flush=True)
            continue

        for entry in tree.findall(f"{{{NS}}}entry"):
            arxiv_id = entry.findtext(f"{{{NS}}}id", "").strip()
            if arxiv_id in seen:
                continue
            seen.add(arxiv_id)

            published = (entry.findtext(f"{{{NS}}}published") or "").strip()
            results.append({
                "source": "arxiv",
                "id": arxiv_id,
                "title": (entry.findtext(f"{{{NS}}}title") or "").strip(),
                "summary": (entry.findtext(f"{{{NS}}}summary") or "").strip()[:500],
                "url": arxiv_id,
                "published_at": published,
                "collected_at": datetime.now(UTC).isoformat(),
            })

    return results


if __name__ == "__main__":
    import sys
    from_d = sys.argv[1] if len(sys.argv) > 1 else None
    to_d = sys.argv[2] if len(sys.argv) > 2 else None
    print(f"Fetching arXiv (from={from_d}, to={to_d})...")
    for item in fetch(from_date=from_d, to_date=to_d):
        print(f"[{item['published_at'][:10]}] {item['title']}")
        print(f"  {item['url']}\n")
