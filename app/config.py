# Config & env

from dataclasses import dataclass
import os

@dataclass
class Settings:
    prom_url: str = os.getenv("PROM_URL", "http://prometheus:9090")
    loki_url: str = os.getenv("LOKI_URL", "http://loki:3100")
    slack_webhook: str = os.getenv("SLACK_WEBHOOK", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4")