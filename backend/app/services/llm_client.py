"""LLM 호출 (W3-01, AD-1) — 실패 전환: Claude → Gemini → Groq

TODO(유시웅)
- 업체별 호출 함수 3개 (httpx 또는 업체별 SDK). 키: ANTHROPIC_API_KEY / GEMINI_API_KEY / GROQ_API_KEY,
  모델: CLAUDE_MODEL / GEMINI_MODEL / GROQ_MODEL
- LLM_PROVIDER_ORDER 순서로 업체당 1회 시도, LLM_TIMEOUT 초과·오류·형식 깨짐 시 다음 업체
- 키가 비어 있는 업체는 건너뜀
- 3곳 모두 실패하면 GENERATION_FAILED (E-2)
- 응답한 업체·소요 시간·전환 횟수를 지표로 남김 (Grafana 패널, W3-06)
- 상담 내용은 구분자 안의 데이터로만 넣고 지시문과 섞지 않음
"""
