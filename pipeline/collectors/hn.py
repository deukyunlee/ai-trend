"""Hacker News collector — fetches top AI-related stories."""
import json
import urllib.request
from datetime import datetime, UTC

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"

AI_KEYWORDS = [
    "ai", "llm", "agent", "claude", "openai", "gpt", "gemini", "anthropic",
    "harness", "agentic", "inference", "transformer", "rag", "mcp",
    "multimodal", "fine-tun", "prompt", "embedding",
]


def fetch(limit: int = 30) -> list[dict]:
    with urllib.request.urlopen(HN_TOP_STORIES) as r:
        ids = json.loads(r.read())[:200]

    results = []
    for story_id in ids:
        if len(results) >= limit:
            break
        with urllib.request.urlopen(HN_ITEM.format(story_id)) as r:
            item = json.loads(r.read())
        if not item or item.get("type") != "story":
            continue
        title = (item.get("title") or "").lower()
        if any(kw in title for kw in AI_KEYWORDS):
            results.append({
                "source": "hackernews",
                "id": str(item["id"]),
                "title": item.get("title", ""),
                "url": item.get("url", f"https://news.ycombinator.com/item?id={item['id']}"),
                "score": item.get("score", 0),
                "collected_at": datetime.now(UTC).isoformat(),
            })

    return results


if __name__ == "__main__":
    for item in fetch(10):
        print(f"[{item['score']:4d}] {item['title']}")
        print(f"       {item['url']}\n")
