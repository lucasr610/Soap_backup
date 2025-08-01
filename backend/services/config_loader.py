from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict


@dataclass
class AIModelConfig:
    provider: str
    name: str
    enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIConfig:
    general: Dict[str, Any] = field(default_factory=dict)
    models: Dict[str, AIModelConfig] = field(default_factory=dict)


class ConfigLoader:
    """Load AI configuration from a JSON file."""

    def __init__(self, path: Path | None = None) -> None:
        if path is None:
            path = Path(__file__).resolve().parents[1] / "configs" / "ai_config.json"
        self.path = path
        self._config: AIConfig | None = None

    def get_config(self) -> AIConfig:
        if self._config is None:
            data = json.loads(self.path.read_text())
            general = data.get("general", {})
            models = {
                key: AIModelConfig(**val) for key, val in data.get("models", {}).items()
            }
            self._config = AIConfig(general=general, models=models)
        return self._config
