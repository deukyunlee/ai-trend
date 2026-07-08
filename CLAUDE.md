# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI 트렌드 수집 도구. Hacker News, arXiv, Lobste.rs, HuggingFace Papers에서 AI/에이전트 관련 콘텐츠를 수집하고, 카테고리별로 분류·요약해 `output/` 디렉토리에 저장한다. 외부 의존성 없이 Python stdlib만 사용한다.

## Commands

```bash
# 테스트
cd pipeline && python3 -m pytest tests/ -v

# 오늘 트렌드 수집
cd pipeline && python3 collect.py

# 날짜 지정 수집 (arXiv 날짜 범위 필터 지원)
cd pipeline && python3 collect.py --date 2026-06-25
cd pipeline && python3 collect.py --from-date 2026-06-01 --to-date 2026-06-30

# 스케줄러 실행 (매일 09:00 KST 자동 수집)
cd pipeline && python3 scheduler.py
```

## Repository

- GitHub: https://github.com/deukyunlee/ai-trend

## PR Workflow

PR 생성 요청 시 아래 흐름을 자동으로 처리한다:

1. **브랜치 생성 및 push** — `git checkout -b <branch>` → 커밋 → `git push -u origin <branch>`
2. **PR 생성** — `gh pr create`
3. **리뷰 루프** — `/review-loop <PR번호>` 스킬 실행
   - 이슈가 없을 때까지 리뷰 → 수정 → push → 재리뷰를 자동 반복
   - 완료 후 PR에 리뷰 요약 comment 자동 게시
   - 구조적 문제 발견 시 머지하지 않고 사용자에게 보고
4. **머지** — `gh pr merge --squash --delete-branch`

## 주의사항

- GitHub의 gemini-code-assist 봇 리뷰는 외부 검증 참고용으로만 활용하고, 대기하지 않는다.
- 외부 라이브러리를 새로 추가하지 않는다. stdlib만 사용한다.
- 테스트는 외부 API를 호출하지 않는다. monkeypatch로 mock 처리한다.
