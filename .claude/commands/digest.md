# /digest

저장된 수집 데이터를 바탕으로 트렌드 다이제스트를 생성합니다.

## 실행 순서

1. `output/` 디렉토리에서 가장 최근 JSON 파일을 찾아 읽는다.
2. 항목들을 분석해서 이번 주/오늘의 핵심 AI 트렌드를 파악한다.
3. 다음 형식으로 한국어 다이제스트를 작성한다:

```markdown
# AI Trend Digest — YYYY-MM-DD

## 이번 주 핵심 트렌드
(2~3문장 전체 요약)

## Harness & Orchestration
- **제목**: 요약 (출처 링크)

## Loop Engineering
...

## 주목할 논문
...
```

4. `output/YYYY-MM-DD-digest.md`로 저장한다.
5. 터미널에 출력한다.

인자로 날짜를 넘기면 (`/digest 2025-06-20`) 해당 날짜 파일을 사용한다.
