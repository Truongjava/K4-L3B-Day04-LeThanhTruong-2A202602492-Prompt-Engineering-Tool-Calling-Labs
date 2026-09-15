from __future__ import annotations

import json
import os
from typing import Any

import requests

from providers.base import ModelResponse, ToolCall


class AIBOXProvider:
    """AI Box / Custom OpenAI-compatible endpoint provider (uses requests, not OpenAI SDK)."""

    def __init__(
        self,
        *,
        auth_token_env: str = "AIBOX_AUTH_TOKEN",
        base_url_env: str = "AIBOX_BASE_URL",
        model_env: str = "AIBOX_MODEL",
    ) -> None:
        self.auth_token_env = auth_token_env
        self.base_url = os.getenv(base_url_env, "").rstrip("/")
        self.default_model = os.getenv(model_env, "qwen3.7-flash")

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        api_key = os.getenv(self.auth_token_env)
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.auth_token_env}")

        payload: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            payload["tools"] = tools
        if tool_choice is not None:
            if isinstance(tool_choice, str):
                # Normalize "required" -> allow any tool; AI Box doesn't accept "any" type.
                # Instead, omit tool_choice entirely so the model auto-selects.
                pass  # omit tool_choice for "required" / any string value
            elif isinstance(tool_choice, dict):
                payload["tool_choice"] = tool_choice
            else:
                pass  # omit

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/chat/completions"
        resp = requests.post(url, headers=headers, json=payload, timeout=120)

        if resp.status_code != 200:
            raise RuntimeError(f"AI Box API error [{resp.status_code}]: {resp.text[:500]}")

        data = resp.json()
        msg = data["choices"][0]["message"]
        calls: list[ToolCall] = []
        for tc in msg.get("tool_calls") or []:
            args = json.loads(tc.get("function", {}).get("arguments", "{}"))
            name = tc.get("function", {}).get("name", "")
            calls.append(ToolCall(name=name, args=args))
        return ModelResponse(text=msg.get("content"), tool_calls=calls, raw=data)
