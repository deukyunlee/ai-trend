"""In-process scheduler — run once, collects daily at configured time."""
import sys
import time
import subprocess
from datetime import datetime, UTC
from pathlib import Path

COLLECT_HOUR_KST = 9  # 매일 오전 9시 (KST)
COLLECT_HOUR_UTC = (COLLECT_HOUR_KST - 9) % 24  # KST is UTC+9; always 0–23

ROOT = Path(__file__).parent


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
        scheduled_time = datetime(today.year, today.month, today.day, COLLECT_HOUR_UTC, 0, tzinfo=UTC)

        if now >= scheduled_time and last_run_date != today:
            success = run_collect()
            if success:
                last_run_date = today  # 성공 시에만 업데이트, 실패 시 재시도

        time.sleep(10)


if __name__ == "__main__":
    main()
