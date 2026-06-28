"""In-process scheduler — run once, collects daily at configured time."""
import sys
import time
import subprocess
from datetime import datetime, UTC
from pathlib import Path

COLLECT_HOUR_KST = 9  # 매일 오전 9시 (KST)
COLLECT_HOUR_UTC = (COLLECT_HOUR_KST - 9) % 24  # KST is UTC+9; always 0–23

ROOT = Path(__file__).parent


def should_run_now() -> bool:
    now = datetime.now(UTC)
    return now.hour == COLLECT_HOUR_UTC and now.minute < 5  # 5분 윈도우로 sleep jitter 허용


def run_collect() -> bool:
    print(f"[{datetime.now(UTC).isoformat()}] Running collect...", flush=True)
    try:
        result = subprocess.run(
            [sys.executable, "collect.py"],
            cwd=ROOT,
            capture_output=False,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        print("collect.py timed out after 300s", flush=True)
        return False
    if result.returncode != 0:
        print(f"collect.py exited with code {result.returncode}", flush=True)
        return False
    return True


def main():
    print("Scheduler started. Collecting daily at 09:00 KST.", flush=True)
    last_run_date = None

    while True:
        now = datetime.now(UTC)
        today = now.date()

        if should_run_now() and last_run_date != today:
            success = run_collect()
            if success:
                last_run_date = today  # 성공 시에만 업데이트, 실패 시 다음 분에 재시도

        time.sleep(60)


if __name__ == "__main__":
    main()
