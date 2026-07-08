# ai-trend

Hacker News, arXiv, Lobste.rs, HuggingFace Papers에서 AI/에이전트 관련 트렌드를 자동 수집하고 카테고리별로 요약하는 도구.

## 기능

- **자동 수집**: Hacker News 상위 글 + arXiv 논문(harness, agentic loop, multi-agent 등) + Lobste.rs(tag=ai) + HuggingFace 큐레이션 논문
- **날짜 필터**: arXiv 논문을 날짜 범위로 필터링
- **다이제스트 생성**: 수집 데이터를 카테고리별 한국어 요약으로 변환
- **스케줄러**: 매일 09:00 KST 자동 수집
- **Claude Code 스킬**: `/collect`, `/digest`, `/add-topic` 지원

## 빠른 시작

```bash
# 오늘 트렌드 수집
cd pipeline && python3 collect.py

# 날짜 범위 지정 (arXiv)
python3 collect.py --from-date 2026-06-01 --to-date 2026-06-30

# 스케줄러 실행 (백그라운드)
nohup python3 scheduler.py > ../output/scheduler.log 2>&1 &
```

## Claude Code 스킬

| 스킬 | 설명 |
|------|------|
| `/collect [날짜] [from=...] [to=...]` | 수집 + 카테고리 분류 + 요약 |
| `/digest [날짜]` | 저장된 데이터로 다이제스트 생성 |
| `/add-topic <카테고리> <토픽명>` | 새 토픽 문서 추가 |
| `/review-loop [PR번호]` | 코드 리뷰 루프 자동 실행 |
| `/bot-review [PR번호]` | gemini-code-assist 리뷰 반영 |

## 구조

```
ai-trend/
├── pipeline/
│   ├── collect.py          # 메인 수집 스크립트
│   ├── scheduler.py        # 일일 자동 수집 스케줄러
│   └── collectors/
│       ├── hn.py           # Hacker News 수집기
│       └── arxiv.py        # arXiv 논문 수집기
├── output/                 # 수집 결과 (YYYY-MM-DD.json, YYYY-MM-DD-digest.md)
└── topics/                 # 큐레이션 토픽 문서
    ├── harness/
    ├── loop-engineering/
    └── infra/
```

## 테스트

```bash
cd pipeline && python3 -m pytest tests/ -v
```

외부 API 호출 없이 monkeypatch로 동작합니다.
