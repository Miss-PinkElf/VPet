import json
from typing import Union
from urllib import error as urllib_error
from urllib import request as urllib_request

from fastapi import HTTPException

from ..core.config import Settings
from ..schemas.chat import ChatMessage


class LlmService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def is_configured(self) -> bool:
        return bool(self._settings.llm_api_key)

    def get_model_name(self) -> str:
        return self._settings.llm_model

    def build_chat_completions_url(self) -> str:
        normalized_base_url = self._settings.llm_base_url.rstrip('/')
        if normalized_base_url.endswith('/chat/completions'):
            return normalized_base_url
        if normalized_base_url.endswith('/v1'):
            return f'{normalized_base_url}/chat/completions'
        return f'{normalized_base_url}/v1/chat/completions'

    def complete_chat(self, messages: list[Union[ChatMessage, dict[str, str]]]) -> str:
        if not self._settings.llm_api_key:
            raise HTTPException(
                status_code=503,
                detail='后端未配置模型 API Key，请先设置 PET_LLM_API_KEY 或 OPENAI_API_KEY。',
            )

        serialized_messages = [
            message.model_dump() if hasattr(message, 'model_dump') else message
            for message in messages
        ]
        payload = {
            'model': self._settings.llm_model,
            'messages': serialized_messages,
        }
        request = urllib_request.Request(
            url=self.build_chat_completions_url(),
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {self._settings.llm_api_key}',
                'Content-Type': 'application/json',
            },
            method='POST',
        )

        try:
            with urllib_request.urlopen(request, timeout=self._settings.upstream_timeout_seconds) as response:
                response_body = response.read().decode('utf-8')
                response_payload = json.loads(response_body)
        except urllib_error.HTTPError as exc:
            raise HTTPException(status_code=exc.code, detail=self.map_upstream_error(exc.code)) from exc
        except urllib_error.URLError as exc:
            raise HTTPException(status_code=502, detail='无法连接模型服务，请检查网络或服务地址配置。') from exc
        except TimeoutError as exc:
            raise HTTPException(status_code=504, detail='模型服务响应超时，请稍后重试。') from exc

        return self.extract_reply_text(response_payload)

    @staticmethod
    def extract_reply_text(payload: dict) -> str:
        choices = payload.get('choices') or []
        if not choices:
            raise HTTPException(status_code=502, detail='上游模型返回为空，暂时无法生成回复。')

        first_choice = choices[0] or {}
        message = first_choice.get('message') or {}
        content = (message.get('content') or '').strip()

        if content:
            return content

        raise HTTPException(status_code=502, detail='上游模型返回格式异常，未获取到回复内容。')

    @staticmethod
    def map_upstream_error(status_code: int) -> str:
        if status_code == 401:
            return '模型服务鉴权失败，请检查后端 API Key 配置。'
        if status_code == 429:
            return '模型服务当前限流，请稍后重试。'
        if status_code >= 500:
            return '模型服务暂时不可用，请稍后重试。'
        return '模型服务调用失败，请检查后端配置或稍后重试。'
