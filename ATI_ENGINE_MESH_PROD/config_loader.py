"""Load AI config from environment variables or ai_config.json."""

import json
import os
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent / "configs"
CONFIG_FILE = CONFIG_DIR / "ai_config.json"

ENV_VARS = {
    "llm_endpoint": "ATI_LLM_ENDPOINT",
    "embedding_endpoint": "ATI_EMBEDDING_ENDPOINT",
    "api_key_path": "ATI_API_KEY_PATH",
}

def load_config():
    """Return AI configuration as a dictionary."""
    config = {}
    for key, env_var in ENV_VARS.items():
        value = os.getenv(env_var)
        if value:
            config[key] = value
    if len(config) < len(ENV_VARS) and CONFIG_FILE.exists():
        try:
            file_data = json.loads(CONFIG_FILE.read_text())
            for key in ENV_VARS:
                config.setdefault(key, file_data.get(key))
        except json.JSONDecodeError:
            pass
    return config

if __name__ == "__main__":
    print(json.dumps(load_config(), indent=2))
