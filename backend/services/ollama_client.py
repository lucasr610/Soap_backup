import logging
from typing import Dict, Optional

import httpx
from httpx import AsyncClient, HTTPStatusError, RequestError, TimeoutException

from .config_loader import ConfigLoader, AIModelConfig

logger = logging.getLogger(__name__)


class OllamaClient:
    """Service for interacting with a locally running Ollama instance.
    Manages text generation requests to local LLMs."""

    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.config = self.config_loader.get_config()
        self.ollama_host = self.config.general.get("ollama_host")
        self.http_client: Optional[AsyncClient] = None
        if not self.ollama_host:
            logger.error(
                "Ollama host not configured in ai_config.json -> general.ollama_host."
            )
            self.is_ready = False
        else:
            self.http_client = AsyncClient(base_url=self.ollama_host, timeout=30.0)
            self.is_ready = True
            logger.info(
                f"OllamaClient initialized, targeting host: {self.ollama_host}"
            )

    async def close(self) -> None:
        """Close underlying HTTP client."""
        if self.http_client:
            await self.http_client.aclose()

    async def _check_ollama_status(self) -> bool:
        """Checks if the Ollama server is reachable."""
        if not self.is_ready or not self.http_client:
            return False
        try:
            response = await self.http_client.get("/api/tags")
            response.raise_for_status()
            logger.debug("Ollama server is reachable.")
            return True
        except HTTPStatusError as e:
            logger.warning(
                f"Ollama server returned an error status: {e.response.status_code} - {e.response.text}"
            )
            return False
        except RequestError as e:
            logger.warning(
                f"Could not connect to Ollama server at {self.ollama_host}: {e}"
            )
            self.is_ready = False
            return False
        except Exception as e:
            logger.exception(
                f"An unexpected error occurred while checking Ollama status: {e}"
            )
            return False

    async def ensure_ready(self) -> bool:
        """Public helper to verify the Ollama server is reachable."""
        if not self.is_ready:
            return False
        return await self._check_ollama_status()

    async def generate_text(self, model_id: str, prompt: str, **kwargs) -> Optional[str]:
        """Generates text using a specified local Ollama model."""
        if not await self.ensure_ready():
            logger.error(
                f"Ollama client not ready or server unreachable for model: {model_id}"
            )
            return None

        model_cfg: Optional[AIModelConfig] = self.config.models.get(model_id)
        if (
            not model_cfg
            or not model_cfg.enabled
            or model_cfg.provider != "ollama"
        ):
            logger.warning(
                f"Attempted to use disabled, non-existent, or non Ollama model: {model_id}"
            )
            return None

        ollama_model_name = model_cfg.name

        default_params: Dict[str, float] = {}
        if getattr(model_cfg, "parameters", None):
            try:
                default_params = model_cfg.parameters.dict(exclude_none=True)
            except AttributeError:
                if isinstance(model_cfg.parameters, dict):
                    default_params = {
                        k: v for k, v in model_cfg.parameters.items() if v is not None
                    }

        params = {**default_params, **kwargs}
        request_body = {
            "model": ollama_model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": params.get("temperature", 0.7),
                "num_predict": params.get("max_tokens", 1024),
            },
        }

        if not self.http_client:
            logger.error("HTTP client not initialized.")
            return None

        try:
            response = await self.http_client.post(
                "/api/generate", json=request_body
            )
            response.raise_for_status()
            data = response.json()
            generated_text = data.get("response", "").strip()
            logger.debug(
                f"Ollama generated text for {model_id}, length: {len(generated_text)}"
            )
            return generated_text
        except HTTPStatusError as e:
            logger.error(
                f"Ollama API call for {model_id} failed with status {e.response.status_code}: {e.response.text}"
            )
            return None
        except TimeoutException as e:
            logger.error(f"Ollama API call for {model_id} timed out: {e}")
            return None
        except RequestError as e:
            logger.error(
                f"Network error during Ollama API call for {model_id}: {e}"
            )
            return None
        except Exception as e:
            logger.exception(
                f"An unexpected error occurred during Ollama text generation for {model_id}."
            )
            return None
