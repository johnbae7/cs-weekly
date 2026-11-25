"""메일 발송 (W3-02·W3-03)

TODO(유시웅)
- MAIL_PROVIDER=ses → boto3 SES, smtp → smtplib (Q-8)
- 수신 주소는 recipients 테이블에서만
- 결과를 deliveries에 기록, 실패 시 DELIVERY_FAILED (E-5)
"""
