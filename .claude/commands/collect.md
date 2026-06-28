# /collect [날짜] [from=YYYY-MM-DD] [to=YYYY-MM-DD]

AI 트렌드 데이터를 수집하고 요약합니다.

## 인자 파싱 규칙

`$ARGUMENTS`를 다음 규칙으로 파싱한다:
- 첫 번째 YYYY-MM-DD 형식 단독 인자 → `--date` (저장 파일명)
- `from=YYYY-MM-DD` → arXiv `--from-date`
- `to=YYYY-MM-DD` → arXiv `--to-date`

예시:
- `/collect` → 오늘 날짜, arXiv 최신순
- `/collect 2026-06-25` → output/2026-06-25.json에 저장, arXiv 최신순
- `/collect from=2026-06-01 to=2026-06-30` → 6월 제출 arXiv 논문만
- `/collect 2026-06-30 from=2026-06-01 to=2026-06-30` → 저장 날짜 + arXiv 범위 동시 지정

## 실행 순서

1. `$ARGUMENTS`를 파싱해서 date, from_date, to_date를 추출한다.
2. 아래 명령을 실행한다.
3. 해당 날짜의 `output/YYYY-MM-DD.json` 파일을 읽는다.
3. 수집된 항목들을 분석해서 다음 카테고리로 분류한다:
   - **Harness & Orchestration**: 에이전트 하네스, 오케스트레이션 패턴
   - **Loop Engineering**: agentic loop, 반복 추론 패턴
   - **Infrastructure**: 추론 인프라, 배포, 서빙
   - **Models & Research**: 새 모델, 논문, 벤치마크
   - **Tools & Frameworks**: MCP, tool use, 프레임워크
4. 카테고리별로 주요 항목 3~5개를 한국어로 요약한다.
5. 요약 결과를 `output/YYYY-MM-DD-digest.md`로 저장한다.
6. 터미널에 요약을 출력한다.

## 실행 명령

```bash
# 오늘 날짜, arXiv 최신순
cd /Users/duke-server/Desktop/projects/ai-trend/pipeline && python3 collect.py

# 저장 날짜 지정
python3 collect.py --date 2026-06-25

# arXiv 날짜 범위 지정
python3 collect.py --from-date 2026-06-01 --to-date 2026-06-30

# 저장 날짜 + arXiv 범위 동시
python3 collect.py --date 2026-06-30 --from-date 2026-06-01 --to-date 2026-06-30
```
