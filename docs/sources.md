# AI 트렌드 수집 가능 소스 목록

현재 통합된 소스와 향후 추가 가능한 소스 정리.

## 현재 수집 중 ✅

| 소스 | 파일 | 특징 |
|------|------|------|
| Hacker News | `collectors/hn.py` | AI 키워드 필터링, 점수 기반 |
| arXiv | `collectors/arxiv.py` | 날짜 범위 필터 지원 |
| Lobste.rs | `collectors/lobsters.py` | tag=ai, 인증 불필요 |
| HuggingFace Papers | `collectors/huggingface.py` | 커뮤니티 upvote 큐레이션 |

---

## 추가 가능한 소스

### 논문 (수집 난이도 낮음)

| 소스 | 접근 | 특징 |
|------|------|------|
| **Papers with Code** | REST API (무료, 인증X) | 논문+코드+벤치마크 SOTA 연동. 트렌드 파악에 최적 |
| **Semantic Scholar** | Graph API (무료, 키 선택) | 인용수·영향력 지표 제공. 분당 100건 제한 |
| **OpenReview** | REST API (무료) | ICLR/NeurIPS 등 학회 리뷰·평점 공개 |
| **bioRxiv/medRxiv** | REST API | AI+바이오 교차 연구 |

### 뉴스/블로그 (RSS)

| 소스 | 특징 |
|------|------|
| **Google/DeepMind Blog** | 프론티어 연구 1차 소스 |
| **OpenAI / Anthropic Blog** | 모델 릴리스·정책 |
| **MIT Technology Review (AI)** | 산업·정책 심층 기사 |
| **VentureBeat AI / TechCrunch AI** | 스타트업·펀딩 |
| **The Gradient** | 연구자 에세이 |

### 뉴스레터 (RSS/아카이브)

| 소스 | 특징 |
|------|------|
| **Import AI** (Jack Clark) | 정책+연구 주간 요약 |
| **The Batch** (deeplearning.ai) | Andrew Ng 주간 요약 |
| **Interconnects** (Nathan Lambert) | RLHF·post-training 전문 |
| **AI News** (smol.ai) | 매일 HN/Reddit/Discord 자동 요약 |

### 커뮤니티

| 소스 | 접근 | 특징 |
|------|------|------|
| **Reddit r/MachineLearning, r/LocalLLaMA** | OAuth2 필요 (앱 등록 필요) | 상세한 커뮤니티 토론 |
| **HuggingFace Forums** | Discourse `.json` API | 실용적 질문/답변 |

---

## 추가 우선순위 추천

1. **Papers with Code** — arXiv 보완, SOTA 벤치마크 정보 추가
2. **RSS 묶음** (DeepMind/Anthropic/OpenAI 블로그) — 뉴스성 보강
3. **Semantic Scholar** — 인용 수 기반 임팩트 측정
