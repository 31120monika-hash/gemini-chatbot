import os
from typing import List, Optional

import requests
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class GeminiAPIError(Exception):
    pass


class GeminiLLM:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        max_output_tokens: int = 512,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY in your .env file."
            )

    # ---------------- FORMAT CHAT HISTORY ----------------
    def format_messages(self, messages: List[object]) -> str:
        conversation_lines: List[str] = []

        for message in messages:
            if isinstance(message, SystemMessage):
                role = "System"
                content = message.content
            elif isinstance(message, HumanMessage):
                role = "User"
                content = message.content
            elif isinstance(message, AIMessage):
                role = "Assistant"
                content = message.content
            else:
                role = "Message"
                content = str(message)

            conversation_lines.append(f"{role}: {content}")

        return "\n".join(conversation_lines)

    # ---------------- PUBLIC METHOD ----------------
    def generate_response(self, user_input: str, history: List[object]) -> str:
        messages = history + [HumanMessage(content=user_input)]
        prompt = self.format_messages(messages)
        return self._call(prompt)

    # ---------------- GEMINI API CALL ----------------
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1/models/"
            f"{self.model_name}:generateContent?key={self.api_key}"
        )

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_output_tokens,
            },
        }

        if stop:
            payload["generationConfig"]["stopSequences"] = stop

        response = requests.post(url, json=payload, timeout=30)

        if response.status_code != 200:
            raise GeminiAPIError(f"HTTP {response.status_code}: {response.text}")

        data = response.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            raise GeminiAPIError("Unexpected Gemini response format")


# ---------------- FACTORY ----------------
def build_conversation_chain(api_key: Optional[str] = None) -> GeminiLLM:
    return GeminiLLM(api_key=api_key)