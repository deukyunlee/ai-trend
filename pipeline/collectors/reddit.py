"""Reddit collector — fetches hot/new posts from AI subreddits via Official API.

Setup:
  1. https://www.reddit.com/prefs/apps 에서 "script" 타입 앱 생성
  2. 환경변수 설정:
       export REDDIT_CLIENT_ID=<your_client_id>
       export REDDIT_CLIENT_SECRET=<your_client_secret>

인증 방식: OAuth2 client_credentials (사용자 로그인 불필요)
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, UTC

SUBREDDITS = ["MachineLearning", "LocalLLaMA"]
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API_BASE = "https://oauth.reddit.com"
USER_AGENT = "ai-trend-collector/1.0 (by /u/ai-trend)"

AI_KEYWORDS = [
    "ai", "llm", "agent", "claude", "openai", "gpt", "gemini", "anthropic",
    "harness", "agentic", "inference", "transformer", "rag", "mcp",
    "multimodal", "fine-tun", "prompt", "embedding", "model", "benchmark",
    "hugging", "mistral", "llama", "deepseek", "qwen", "diffusion",
]


def _get_token(client_id: str, client_secret: str) -> str:
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")

    # Basic auth
    import base64
    creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    req.add_header("Authorization", f"Basic {creds}")
    req.add_header("User-Agent", USER_AGENT)

    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())["access_token"]


def _fetch_subreddit(token: str, subreddit: str, limit: int) -> list[dict]:
    url = f"{API_BASE}/r/{subreddit}/hot?limit=100"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"bearer {token}")
    req.add_header("User-Agent", USER_AGENT)

    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())

    results = []
    for child in data.get("data", {}).get("children", []):
        if len(results) >= limit:
            break
        post = child.get("data", {})
        title = (post.get("title") or "").lower()

        # r/MachineLearning은 AI 전용이므로 키워드 필터 완화
        if subreddit == "MachineLearning" or any(kw in title for kw in AI_KEYWORDS):
            post_id = post.get("id", "")
            url_field = post.get("url") or f"https://www.reddit.com{post.get('permalink', '')}"
            results.append({
                "source": f"reddit_r_{subreddit.lower()}",
                "id": f"reddit:{post_id}",
                "title": post.get("title", ""),
                "url": url_field,
                "score": post.get("score", 0),
                "subreddit": subreddit,
                "num_comments": post.get("num_comments", 0),
                "collected_at": datetime.now(UTC).isoformat(),
            })

    return results


def fetch(limit_per_sub: int = 20) -> list[dict]:
    client_id = os.environ.get("REDDIT_CLIENT_ID", "")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        print("Reddit: REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET 환경변수가 없습니다. 건너뜁니다.", flush=True)
        return []

    try:
        token = _get_token(client_id, client_secret)
    except Exception as e:
        print(f"Reddit 인증 실패: {e}", flush=True)
        return []

    results = []
    seen_ids: set[str] = set()

    for sub in SUBREDDITS:
        try:
            items = _fetch_subreddit(token, sub, limit_per_sub)
        except urllib.error.URLError as e:
            print(f"Reddit r/{sub} fetch 실패: {e}", flush=True)
            continue

        for item in items:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                results.append(item)

    return results


if __name__ == "__main__":
    items = fetch()
    if not items:
        print("수집된 항목 없음 (환경변수 확인)")
    for item in items:
        print(f"[{item['subreddit']:16s}] [{item['score']:5d}] {item['title'][:65]}")
