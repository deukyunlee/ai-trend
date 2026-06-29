"""Lobste.rs collector — fetches AI-tagged posts via open JSON API."""
import json
import urllib.error
import urllib.request
from datetime import datetime, UTC

# ml 태그는 OCaml/ML 언어 커뮤니티이므로 제외
TAGS = ["ai"]
LOBSTERS_TAG = "https://lobste.rs/t/{tag}.json"


def fetch(limit_per_tag: int = 20) -> list[dict]:
    results = []
    seen_ids: set[str] = set()

    for tag in TAGS:
        url = LOBSTERS_TAG.format(tag=tag)
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                posts = json.loads(r.read())
        except urllib.error.URLError as e:
            print(f"Lobste.rs tag={tag} fetch failed: {e}", flush=True)
            continue

        count = 0
        for post in posts:
            if count >= limit_per_tag:
                break
            post_id = post.get("short_id", "")
            if not post_id or post_id in seen_ids:
                continue
            seen_ids.add(post_id)
            results.append({
                "source": "lobsters",
                "id": f"lobsters:{post_id}",
                "title": post.get("title", ""),
                "url": post.get("url") or post.get("comments_url", ""),
                "score": post.get("score", 0),
                "tags": post.get("tags", []),
                "num_comments": post.get("comment_count", 0),
                "collected_at": datetime.now(UTC).isoformat(),
            })
            count += 1

    return results


if __name__ == "__main__":
    for item in fetch():
        print(f"[{item['score']:3d}] [{','.join(item['tags'])}] {item['title'][:70]}")
