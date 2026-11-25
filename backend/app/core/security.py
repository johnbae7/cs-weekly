"""JWT 발급·확인, 비밀번호 해시 (W2-04, F-6).

TODO(유시웅)
- create_access_token(user): 토큰에 user_id, role, recipient_group 포함
- decode_token(token): 실패 시 401
- hash_password / verify_password: bcrypt
"""
