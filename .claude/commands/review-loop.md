# /review-loop [PR번호]

현재 브랜치의 diff를 대상으로, 코드 리뷰 이슈가 없을 때까지 리뷰 → 수정 → 재리뷰를 반복한다.

PR 번호를 인수로 받을 수 있다: `/review-loop 5` (없으면 현재 브랜치 기준)

## 실행 흐름

### Step 1 — diff 수집

```bash
git diff main...HEAD
```

diff가 비어 있으면 "리뷰할 변경사항이 없습니다"를 출력하고 종료한다.

### Step 2 — 리뷰 실행

`/code-review medium` 스킬을 실행한다.
반환된 findings 목록을 캡처한다.

### Step 3 — 판정

findings를 분석한다:

- **빈 목록** → Step 5로 이동 (루프 종료)
- **구조적 문제** (설계 결함, 잘못된 접근 등 단순 수정으로 해결 불가) → 사용자에게 보고하고 종료. 머지하지 않는다.
- **수정 가능한 이슈** → Step 4로 이동

### Step 4 — 수정 & 재리뷰

1. findings를 심각도 순으로 모두 수정한다
2. 테스트가 있으면 실행해서 통과를 확인한다
3. 커밋한다:
   ```bash
   git add -A && git commit -m "fix: apply review findings (iteration N)"
   ```
4. push한다:
   ```bash
   git push
   ```
5. Step 2로 돌아간다 (이슈가 없어질 때까지 반복)

반복 횟수(N)는 1부터 시작하며, 매 반복마다 증가시킨다.
최대 5회 반복 후에도 이슈가 남아 있으면 사용자에게 현황을 보고하고 종료한다.

### Step 5 — 리뷰 요약 comment 게시

PR 번호가 제공된 경우 아래 형식으로 comment를 게시한다:

```bash
gh pr comment <number> --body "..."
```

comment 내용:
- 총 반복 횟수
- 각 iteration에서 발견된 이슈 목록과 수정 내용 요약
- 최종 결과: "이슈 없음 — 머지 준비 완료"

PR 번호가 없으면 comment 단계를 건너뛴다.

### Step 6 — 완료 보고

사용자에게 최종 결과를 출력한다:
- 총 반복 횟수
- 수정된 이슈 수
- "이슈 없음" 확인 메시지

머지는 자동으로 하지 않는다. 사용자가 별도로 요청할 때 한다.

## 주의사항

- 각 iteration은 독립적인 `/code-review` 실행이다. 이전 iteration 결과를 재사용하지 않는다.
- 수정 후 반드시 push까지 완료한 뒤 다음 리뷰를 시작한다.
- 구조적 문제는 수정을 시도하지 않고 즉시 사용자에게 보고한다.
