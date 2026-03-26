import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

DEFAULT_LLM_BASE_URL = 'https://codex.hiyo.top/'
DEFAULT_LLM_MODEL = 'gpt-5.4'
DEFAULT_SERVER_HOST = '127.0.0.1'
DEFAULT_SERVER_PORT = 8787
DEFAULT_UPSTREAM_TIMEOUT_SECONDS = 40.0
DEFAULT_MAX_HISTORY_ITEMS = 12

load_dotenv()


@dataclass(frozen=True)
class Settings:
    llm_base_url: str
    llm_model: str
    llm_api_key: str
    backend_host: str
    backend_port: int
    upstream_timeout_seconds: float
    max_history_items: int
    system_prompt: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        llm_base_url=os.getenv('PET_LLM_BASE_URL', DEFAULT_LLM_BASE_URL).strip() or DEFAULT_LLM_BASE_URL,
        llm_model=os.getenv('PET_LLM_MODEL', DEFAULT_LLM_MODEL).strip() or DEFAULT_LLM_MODEL,
        llm_api_key=(os.getenv('PET_LLM_API_KEY') or os.getenv('OPENAI_API_KEY') or '').strip(),
        backend_host=os.getenv('PET_BACKEND_HOST', DEFAULT_SERVER_HOST).strip() or DEFAULT_SERVER_HOST,
        backend_port=int(os.getenv('PET_BACKEND_PORT', str(DEFAULT_SERVER_PORT))),
        upstream_timeout_seconds=float(
            os.getenv('PET_LLM_TIMEOUT_SECONDS', str(DEFAULT_UPSTREAM_TIMEOUT_SECONDS)),
        ),
        max_history_items=int(os.getenv('PET_CHAT_MAX_HISTORY_ITEMS', str(DEFAULT_MAX_HISTORY_ITEMS))),
        system_prompt=(
            '你是一只桌面陪伴型桌宠，用简体中文和用户对话。'
            '回复保持自然、简洁、友好，优先给出可直接理解的回答。'
        ),
    )
