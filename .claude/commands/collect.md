# /collect

AI 트렌드 데이터를 수집하고 요약합니다.

## 실행 순서

1. `pipeline/collect.py`를 실행해서 HN과 arXiv에서 데이터를 수집한다.
2. 오늘 날짜의 `output/YYYY-MM-DD.json` 파일을 읽는다.
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
cd /Users/duke-server/Desktop/projects/ai-trend/pipeline && python collect.py
```
