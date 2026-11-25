"""검토 필요 판정 R1~R4 (W3-02)

기준값은 Q-6 결정 대기 → 아래 상수만 바꾸면 되도록 한 곳에 둡니다.

TODO(유시웅): judge(report, upload) → (is_review_needed, reasons)

"""

# R2 상품 불량 집중: 같은 상품 불량 키워드 문의 N건 이상
R2_MIN_DEFECT_COUNT = 5
# R3 문의 유형 급증: 전주 대비 비율 이상 그리고 건수 이상 증가 (전주 없으면 생략)
R3_MIN_RATE = 0.30
R3_MIN_DELTA = 10
