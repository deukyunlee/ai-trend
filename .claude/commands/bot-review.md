# /bot-review [PR번호]

PR에 남긴 gemini-code-assist 봇 리뷰를 가져와서, 수정 가능한 이슈는 반영하고 각 댓글에 답글을 단다.

PR 번호를 인수로 받는다: `/bot-review 5`
인수가 없으면 현재 브랜치의 열린 PR을 자동으로 찾는다.

## 실행 흐름

### Step 1 — PR 번호 확인

인수가 없으면 현재 브랜치의 PR을 찾는다:
```bash
gh pr view --json number --jq '.number'
```

### Step 2 — 봇 리뷰 댓글 수집

PR의 리뷰 댓글과 일반 댓글을 모두 가져온다:
```bash
# 인라인 리뷰 댓글
gh api repos/{owner}/{repo}/pulls/{PR번호}/comments

# 일반 PR 댓글
gh api repos/{owner}/{repo}/issues/{PR번호}/comments

# 리뷰 목록
gh api repos/{owner}/{repo}/pulls/{PR번호}/reviews
```

`user.login`이 `gemini-code-assist`인 항목만 필터링한다.
봇 댓글이 없으면 "gemini-code-assist 리뷰 없음"을 출력하고 종료한다.

### Step 3 — 댓글 분석 및 판정

각 댓글을 분석한다:

- **수정 가능한 이슈** (버그, 스타일, 로직 문제 등) → Step 4로 이동
- **구조적 문제** (설계 결함, 단순 수정 불가) → 사용자에게 보고하고 답글만 단다
- **정보성 / 참고용** (칭찬, 설명 요청 등) → 답글만 단다

### Step 4 — 수정

수정 가능한 이슈를 모두 반영한다.
테스트가 있으면 실행해서 통과를 확인한다:
```bash
cd pipeline && python3 -m pytest tests/ -v
```

수정 후 커밋 & 푸시한다:
```bash
git add -A && git commit -m "fix: address gemini-code-assist review comments"
git push
```

### Step 5 — 답글 게시

각 봇 댓글에 답글을 단다.

인라인 댓글 답글:
```bash
gh api repos/{owner}/{repo}/pulls/{PR번호}/comments \
  --method POST \
  --field body="..." \
  --field in_reply_to={comment_id}
```

일반 댓글 답글:
```bash
gh pr comment {PR번호} --body "..."
```

답글 형식:
- 수정한 경우: "✅ 수정했습니다. [수정 내용 한 줄 요약]"
- 구조적 문제로 미수정: "확인했습니다. [이유 설명] — 별도로 검토가 필요합니다."
- 정보성 댓글: "감사합니다. [간단한 응답]"

### Step 6 — 완료 보고

사용자에게 최종 결과를 출력한다:
- 처리한 봇 댓글 수
- 수정한 이슈 수
- 답글 게시 완료 여부

## 주의사항

- gemini-code-assist 봇 리뷰는 참고용으로 활용한다. CLAUDE.md에서 "외부 검증 참고용으로만 활용하고, 대기하지 않는다"고 명시돼 있으므로, 봇 의견이 프로젝트 방향과 맞지 않으면 수정 없이 답글만 달고 이유를 설명한다.
- 수정 후 반드시 테스트를 실행하고 통과를 확인한다.
- 머지는 하지 않는다. 사용자가 별도로 요청할 때 한다.
