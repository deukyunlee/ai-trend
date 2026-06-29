"""Tests for collect.py — save logic and date handling."""
import json
import sys
from pathlib import Path

import pytest

# pipeline/ 디렉토리를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from collect import collect, save

FAKE_LOBSTERS_ITEM = {"source": "lobsters", "id": "lobsters:abc123", "title": "Lobste.rs AI Post", "url": "https://lobste.rs/s/abc123", "score": 10, "tags": ["ai"], "num_comments": 5, "collected_at": "2026-06-29T00:00:00+00:00"}


# ── fixtures ──────────────────────────────────────────────────────────────────

FAKE_ITEMS = [
    {"source": "hackernews", "id": "1", "title": "HN Item 1", "url": "https://example.com/1", "score": 100, "collected_at": "2026-06-28T00:00:00+00:00"},
    {"source": "arxiv",      "id": "arxiv:001", "title": "arXiv Paper 1", "url": "https://arxiv.org/abs/001", "summary": "summary", "published_at": "2026-06-28", "collected_at": "2026-06-28T00:00:00+00:00"},
]


# ── save() ────────────────────────────────────────────────────────────────────

def test_save_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr("collect.OUTPUT", tmp_path)
    path = save(FAKE_ITEMS, date_str="2026-06-28")
    assert path.exists()
    data = json.loads(path.read_text())
    assert len(data) == 2


def test_save_deduplicates_by_id(tmp_path, monkeypatch):
    monkeypatch.setattr("collect.OUTPUT", tmp_path)
    save(FAKE_ITEMS, date_str="2026-06-28")
    # 동일 ID로 재저장 — 중복 없어야 함
    path = save(FAKE_ITEMS, date_str="2026-06-28")
    data = json.loads(path.read_text())
    assert len(data) == 2


def test_save_appends_new_items(tmp_path, monkeypatch):
    monkeypatch.setattr("collect.OUTPUT", tmp_path)
    save(FAKE_ITEMS, date_str="2026-06-28")
    new_item = {"source": "hackernews", "id": "99", "title": "New", "url": "https://example.com/99", "score": 1, "collected_at": "2026-06-28T01:00:00+00:00"}
    path = save([new_item], date_str="2026-06-28")
    data = json.loads(path.read_text())
    assert len(data) == 3


def test_save_uses_today_when_no_date(tmp_path, monkeypatch):
    from datetime import datetime, UTC
    monkeypatch.setattr("collect.OUTPUT", tmp_path)
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    path = save(FAKE_ITEMS)
    assert path.name == f"{today}.json"


def test_save_different_dates_create_separate_files(tmp_path, monkeypatch):
    monkeypatch.setattr("collect.OUTPUT", tmp_path)
    save(FAKE_ITEMS, date_str="2026-06-01")
    save(FAKE_ITEMS, date_str="2026-06-02")
    assert (tmp_path / "2026-06-01.json").exists()
    assert (tmp_path / "2026-06-02.json").exists()


def test_save_global_dedup_across_dates(tmp_path, monkeypatch):
    monkeypatch.setattr("collect.OUTPUT", tmp_path)
    # 06-01에 저장된 항목은 06-02에 다시 저장되지 않아야 함
    save(FAKE_ITEMS, date_str="2026-06-01")
    path = save(FAKE_ITEMS, date_str="2026-06-02")
    data = json.loads(path.read_text())
    assert len(data) == 0


# ── collect() — 외부 API mocking ──────────────────────────────────────────────

def test_collect_hn_only(monkeypatch):
    monkeypatch.setattr("collect.fetch_hn", lambda: FAKE_ITEMS[:1])
    items = collect(sources=["hn"])
    assert len(items) == 1
    assert items[0]["source"] == "hackernews"


def test_collect_arxiv_only(monkeypatch):
    monkeypatch.setattr("collect.fetch_arxiv", lambda **_: FAKE_ITEMS[1:])
    items = collect(sources=["arxiv"])
    assert len(items) == 1
    assert items[0]["source"] == "arxiv"


def test_collect_passes_date_range_to_arxiv(monkeypatch):
    captured = {}

    def fake_fetch_arxiv(from_date=None, to_date=None, **_):
        captured["from_date"] = from_date
        captured["to_date"] = to_date
        return []

    monkeypatch.setattr("collect.fetch_arxiv", fake_fetch_arxiv)
    collect(sources=["arxiv"], from_date="2026-06-01", to_date="2026-06-30")
    assert captured["from_date"] == "2026-06-01"
    assert captured["to_date"] == "2026-06-30"


def test_collect_lobsters_only(monkeypatch):
    monkeypatch.setattr("collect.fetch_lobsters", lambda **_: [FAKE_LOBSTERS_ITEM])
    items = collect(sources=["lobsters"])
    assert len(items) == 1
    assert items[0]["source"] == "lobsters"


def test_collect_default_sources(monkeypatch):
    called = []
    monkeypatch.setattr("collect.fetch_hn", lambda: called.append("hn") or [])
    monkeypatch.setattr("collect.fetch_arxiv", lambda **_: called.append("arxiv") or [])
    monkeypatch.setattr("collect.fetch_lobsters", lambda **_: called.append("lobsters") or [])
    collect()
    assert "hn" in called
    assert "arxiv" in called
    assert "lobsters" in called
