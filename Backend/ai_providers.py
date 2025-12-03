import requests
from typing import Optional
from .config import (
    OPENAI_API_KEY,
    GROQ_API_KEY,
    GEMINI_API_KEY,
    DEEPSEEK_API_KEY,
)


# ---------------------------
# LOCAL OFFLINE AI FALLBACK
# ---------------------------

def local_ai_response(provider, model, prompt, system_prompt):
    """Return a fake but useful AI-like response."""
    sys = f"[System: {system_prompt}]" if system_prompt else ""
    return (
        f"(Offline {provider}/{model}) {sys}\n"
        f"I am an offline local AI model and cannot call external APIs.\n"
        f"Here is a helpful simulated answer to your prompt:\n\n"
        f"→ {prompt}\n\n"
        f"(This is a dummy response used only for local testing.)"
    )


# ---------------------------
# AI PROVIDER CLASS
# ---------------------------

class AIProvider:
    def __init__(self, name: str, model: str, api_key: str, base_url: str):
        self.name = name
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    # MAIN ENTRY
    def ask(self, prompt: str, system_prompt: Optional[str] = None) -> str:

        # OFFLINE MODE: if missing API key
        if not self.api_key:
            return local_ai_response(self.name, self.model, prompt, system_prompt)

        try:
            if self.name == "openai":
                return self._ask_openai(prompt, system_prompt)
            if self.name == "groq":
                return self._ask_groq(prompt, system_prompt)
            if self.name == "gemini":
                return self._ask_gemini(prompt, system_prompt)
            if self.name == "deepseek":
                return self._ask_deepseek(prompt, system_prompt)

            return f"[Unknown provider: {self.name}]"

        except Exception as e:
            # Fallback to offline simulated answer if error occurs
            print(f"{self.name} provider failed → using offline fallback:", str(e))
            return local_ai_response(self.name, self.model, prompt, system_prompt)

    # ---------------------------
    # REAL PROVIDERS (ONLY USED IF KEYS EXIST)
    # ---------------------------

    def _ask_openai(self, prompt, system_prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        body = {"model": self.model, "messages": messages}

        r = requests.post(
            f"{self.base_url}/chat/completions", json=body, headers=headers
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _ask_groq(self, prompt, system_prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        body = {"model": self.model, "messages": messages}

        r = requests.post(
            f"{self.base_url}/chat/completions", json=body, headers=headers
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _ask_gemini(self, prompt, system_prompt):
        text = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        body = {"contents": [{"parts": [{"text": text}]}]}
        r = requests.post(url, json=body)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _ask_deepseek(self, prompt, system_prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        body = {"model": self.model, "messages": messages}

        r = requests.post(
            f"{self.base_url}/chat/completions", json=body, headers=headers
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


# ---------------------------
# AGENT REGISTRATION
# ---------------------------

AGENTS = {
    "gpt4_coder": AIProvider(
        name="openai",
        model="gpt-4.1",
        api_key=OPENAI_API_KEY,
        base_url="https://api.openai.com/v1",
    ),
    "groq_llama": AIProvider(
        name="groq",
        model="llama3-70b-8192",
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    ),
    "gemini_flash": AIProvider(
        name="gemini",
        model="gemini-1.5-flash",
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/models",
    ),
    "deepseek_chat": AIProvider(
        name="deepseek",
        model="deepseek-chat",
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com/v1",
    ),
}
