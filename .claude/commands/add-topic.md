# /add-topic

새 트렌드 토픽 문서를 생성합니다.

## 사용법
```
/add-topic <카테고리> <토픽명>
```
예: `/add-topic harness multi-agent-coordination`

## 실행 순서

1. 인자에서 카테고리와 토픽명을 파싱한다.
   - 카테고리: `harness`, `loop-engineering`, `infra` 중 하나
   - 없으면 카테고리를 물어본다.
2. `topics/<카테고리>/<토픽명>.md` 파일을 다음 템플릿으로 생성한다:

```markdown
# <토픽명>

## 개요
(무엇인지, 왜 중요한지)

## 핵심 개념

## 주요 사례 / 구현체

## 관련 자료

## 업데이트 히스토리
- YYYY-MM-DD: 문서 생성
```

3. 파일 경로를 출력한다.
