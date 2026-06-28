"""arXiv collector — fetches recent AI/agent papers."""
import json
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


def fetch(max_per_query: int = 5) -> list[dict]:
    results = []
    seen = set()

    for query in QUERIES:
        params = urllib.parse.urlencode({
            "search_query": query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": max_per_query,
        })
        url = f"{ARXIV_API}?{params}"
        with urllib.request.urlopen(url) as r:
            tree = ET.fromstring(r.read())

        for entry in tree.findall(f"{{{NS}}}entry"):
            arxiv_id = entry.findtext(f"{{{NS}}}id", "").strip()
            if arxiv_id in seen:
                continue
            seen.add(arxiv_id)
            results.append({
                "source": "arxiv",
                "id": arxiv_id,
                "title": (entry.findtext(f"{{{NS}}}title") or "").strip(),
                "summary": (entry.findtext(f"{{{NS}}}summary") or "").strip()[:500],
                "url": arxiv_id,
                "collected_at": datetime.now(UTC).isoformat(),
            })

    return results


if __name__ == "__main__":
    for item in fetch():
        print(f"{item['title']}")
        print(f"  {item['url']}\n")
