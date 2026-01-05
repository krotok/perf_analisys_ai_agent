# GPT / Claude wrapper

import os
import json
from typing import Dict, Any, List

# Optional imports – will be loaded in case of usage only
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class LLMClient:
    """
    Vendor-agnostic LLM wrapper.
    Responsible ONLY for:
    - prompt delivery
    - structured response parsing
    """

    def __init__(self, provider: str, model: str):
        self.provider = provider.lower()
        self.model = model

        if self.provider == "openai":
            if OpenAI is None:
                raise RuntimeError("openai package not installed")
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        elif self.provider == "gemini":
            if genai is None:
                raise RuntimeError("google-generativeai package not installed")
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.client = genai.GenerativeModel(model)

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def reason(self, system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends structured input to LLM and expects STRICT JSON output.
        """
        prompt = self._build_prompt(system_prompt, user_payload)

        if self.provider == "openai":
            response = self._call_openai(prompt)
        elif self.provider == "gemini":
            response = self._call_gemini(prompt)
        else:
            raise RuntimeError("Invalid provider")

        return self._parse_json(response)

    # ---------------- internal ----------------

    def _build_prompt(self, system_prompt: str, payload: Dict[str, Any]) -> str:
        return f"""
{system_prompt}

Input data (JSON):
{json.dumps(payload, indent=2)}

Return ONLY valid JSON. No explanations.
"""

    def _call_openai(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a senior SRE and Performance Engineer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return completion.choices[0].message.content

    def _call_gemini(self, prompt: str) -> str:
        response = self.client.generate_content(prompt)
        return response.text

    def _parse_json(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise RuntimeError(
                f"LLM returned non-JSON response:\n{text}"
            )

