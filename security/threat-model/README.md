# 위협 모델링 (W1-08, W2-10 / S-1, S-2)

## 보호 자산
- 상담기록 원본(consults): 고객명·전화·이메일·주소·주문번호
- 보고서(승인 전·후), 수신자 허용 목록
- Secret: DATABASE_URL, JWT_SECRET, ANTHROPIC_API_KEY·GEMINI_API_KEY·GROQ_API_KEY, SES·SMTP

## 데이터 흐름과 점검 지점 (시트 「풀스택아키텍처」 연결 흐름)
| 번호 | 흐름 | 점검 지점 |
|---|---|---|
| L-2 | 브라우저 → 백엔드 API | 인증·권한 검사 |
| L-3 | 백엔드 → Amazon RDS | 신뢰 경계, 보안 그룹 |
| L-4 | 백엔드 → 외부 LLM API(Claude → Gemini → Groq) | 입력·출력 가드레일 |
| L-5 | 백엔드 → SES | 전달 가드레일 |
| L-6 | Prometheus → /metrics | 클러스터 내부만 |

## 위협 목록
TODO(김찬규): 권한 우회, 미승인 전달·수신자 변조, 인젝션, 정보 유출, Secret·설정 노출

## 보안 요구사항 (담당 과정 구분)
TODO(김찬규)
