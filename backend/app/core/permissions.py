"""권한 검사 함수 1개 (W2-04, F-6, AD 「역할·상태」).

검사 순서는 반드시 이 순서입니다.
  1) 인증        → 401
  2) 역할        → 403  (uploader / reviewer / recipient)
  3) 소유·그룹   → 403  (작성자는 본인 업로드, 수신자는 자기 그룹에 전달된 보고서만)
  4) 상태        → 409  (예: APPROVED가 아니면 전달 불가)

거부할 때마다 services/security_log.py로 security_events에 기록합니다 (S-7).
라우터마다 따로 검사 코드를 만들지 않고 이 함수만 씁니다.

TODO(유시웅): check_access(user, action, target) 구현
"""
