"""환경 변수 읽기. 키 이름은 루트 CLAUDE.md 5절·.env.example과 같아야 합니다."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    # 업무 API 접두사 (/health, /health/ready, /metrics에는 붙지 않음)
    api_prefix: str = "/api"

    database_url: str = ""
    jwt_secret: str = "changeme"

    # LLM 실패 전환 (AD-1): 쉼표로 구분한 순서. 앞 업체 실패 시 다음 업체
    llm_provider_order: str = "claude,gemini,groq"
    claude_model: str = ""
    gemini_model: str = ""
    groq_model: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    llm_timeout: int = 60

    mail_provider: str = "ses"  # ses 또는 smtp (Q-8)
    mail_from: str = ""
    aws_region: str = "ap-northeast-2"
    smtp_user: str = ""
    smtp_password: str = ""

    app_base_url: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()
