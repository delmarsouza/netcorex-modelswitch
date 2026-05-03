from dataclasses import dataclass
import os


@dataclass
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    ollama_default_model: str = os.getenv("OLLAMA_DEFAULT_MODEL", "qwen2.5:14b")
