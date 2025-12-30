"""Unified LLM client interface - Dec 2025."""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LLMResponse:
    """Standardized response from any LLM."""
    text: str
    model: str
    provider: str


class LLMClient(ABC):
    @abstractmethod
    def query(self, prompt: str, max_tokens: int = 1000) -> LLMResponse:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass


class ClaudeClient(LLMClient):
    def __init__(self, model: str = None):
        import anthropic
        self.client = anthropic.Anthropic()
        self.model = model or os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    
    def query(self, prompt: str, max_tokens: int = 1000) -> LLMResponse:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return LLMResponse(
            text=response.content[0].text,
            model=self.model,
            provider="anthropic"
        )
    
    @property
    def name(self) -> str:
        return f"claude:{self.model}"


class OpenAIClient(LLMClient):
    def __init__(self, model: str = None):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
    
    def query(self, prompt: str, max_tokens: int = 1000) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return LLMResponse(
            text=response.choices[0].message.content,
            model=self.model,
            provider="openai"
        )
    
    @property
    def name(self) -> str:
        return f"openai:{self.model}"


class GoogleClient(LLMClient):
    """Google Gemini client - supports both old and new SDK."""
    
    def __init__(self, model: str = None):
        self.model_name = model or os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
        
        # Try new SDK first (google-genai)
        try:
            from google import genai
            self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            self._use_new_sdk = True
            return
        except ImportError:
            pass
        
        # Fall back to old SDK (google-generativeai)
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self._model = genai.GenerativeModel(self.model_name)
            self._use_new_sdk = False
        except ImportError:
            raise ImportError("Install either google-genai or google-generativeai")
    
    def query(self, prompt: str, max_tokens: int = 1000) -> LLMResponse:
        if self._use_new_sdk:
            from google.genai import types
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(max_output_tokens=max_tokens)
            )
            text = response.text
        else:
            response = self._model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens}
            )
            text = response.text
        
        return LLMResponse(text=text, model=self.model_name, provider="google")
    
    @property
    def name(self) -> str:
        return f"google:{self.model_name}"


def get_client(provider: str, model: str = None) -> LLMClient:
    """Factory function to get appropriate client."""
    providers = {
        "claude": ClaudeClient,
        "anthropic": ClaudeClient,
        "openai": OpenAIClient,
        "gpt": OpenAIClient,
        "google": GoogleClient,
        "gemini": GoogleClient,
    }
    
    if provider.lower() not in providers:
        raise ValueError(f"Unknown provider: {provider}")
    
    return providers[provider.lower()](model)


def get_all_clients() -> list:
    """Get all configured clients."""
    clients = []
    
    for name, key_var, cls in [
        ("Claude", "ANTHROPIC_API_KEY", ClaudeClient),
        ("OpenAI", "OPENAI_API_KEY", OpenAIClient),
        ("Google", "GOOGLE_API_KEY", GoogleClient),
    ]:
        if os.getenv(key_var):
            try:
                clients.append(cls())
            except Exception as e:
                print(f"Warning: Could not initialize {name}: {e}")
    
    return clients
