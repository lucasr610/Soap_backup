import logging
from typing import Optional

from .ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class OllamaAgent:
    """Specialized agent using :class:`OllamaClient` as its toolbox."""

    def __init__(self, client: OllamaClient) -> None:
        self.client = client

    async def ensure_ready(self) -> bool:
        """Verify the underlying Ollama service is reachable."""
        return await self.client.ensure_ready()

    async def run(
        self, prompt: str, model_id: str = "ollama_mistral_7b", **kwargs
    ) -> Optional[str]:
        """Generate text via the managed :class:`OllamaClient`.

        Args:
            prompt: The text prompt to send.
            model_id: Identifier of the configured Ollama model.
            **kwargs: Extra generation parameters.
        """
        return await self.client.generate_text(model_id=model_id, prompt=prompt, **kwargs)

    async def close(self) -> None:
        """Release resources held by the underlying client."""
        await self.client.close()
