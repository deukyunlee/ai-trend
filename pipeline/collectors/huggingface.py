"""HuggingFace Papers collector — fetches community-curated daily papers.

HuggingFace가 매일 큐레이션하는 화제 논문 목록. arXiv 원본 중
커뮤니티 upvote를 받은 것만 추려져 노이즈가 적다.
인증 불필요, open JSON API.
"""
import json
import urllib.error
import urllib.request
from datetime import datetime, UTC

# date 파라미터 없이 호출하면 최신 daily papers 반환
DAILY_PAPERS = "https://huggingface.co/api/daily_papers"


def fetch(limit: int = 30, date: str | None = None) -> list[dict]:
    """
    Args:
        limit: 최대 결과 수
        date: 특정 날짜 (YYYY-MM-DD). None이면 최신 큐레이션.
    """
    url = DAILY_PAPERS
    if date:
        url = f"{DAILY_PAPERS}?date={date}"

    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            papers = json.loads(r.read())
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"HuggingFace Papers fetch failed: {e}", flush=True)
        return []

    results = []
    for entry in papers[:limit]:
        paper = entry.get("paper", {})
        paper_id = paper.get("id", "")
        if not paper_id:
            continue
        results.append({
            "source": "huggingface",
            "id": f"hf:{paper_id}",
            "title": entry.get("title", "").strip(),
            "summary": (paper.get("ai_summary") or paper.get("summary") or "").strip()[:500],
            "url": f"https://huggingface.co/papers/{paper_id}",
            "score": paper.get("upvotes", 0),
            "keywords": paper.get("ai_keywords", [])[:8],
            "num_comments": entry.get("numComments", 0),
            "published_at": paper.get("publishedAt", ""),
            "collected_at": datetime.now(UTC).isoformat(),
        })

    return results


if __name__ == "__main__":
    for item in fetch():
        print(f"[{item['score']:3d}up] {item['title'][:60]}")
        print(f"        {item['url']}  kw={item['keywords'][:3]}\n")
