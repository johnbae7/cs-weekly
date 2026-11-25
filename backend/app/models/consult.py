"""consults: consult_id(PK), received_at, week_key, upload_id(FK), channel, customer_name, phone, email,
address, order_no, product_name, inquiry_type, content, resolution, status, agent, satisfaction
인덱스 (week_key, consult_id). 개인정보 열(customer_name, phone, email, address, order_no, agent)은 LLM으로 보내지 않음.
"""
