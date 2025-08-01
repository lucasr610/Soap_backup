import asyncio
import json
import httpx

from backend.services import ConfigLoader, OllamaClient


def test_generate_text(tmp_path):
    async def run():
        config = {
            "general": {"ollama_host": "http://test"},
            "models": {
                "ollama_mistral_7b": {
                    "provider": "ollama",
                    "name": "mistral:latest",
                    "enabled": True,
                    "parameters": {"temperature": 0.7, "max_tokens": 100},
                }
            },
        }
        config_path = tmp_path / "ai_config.json"
        config_path.write_text(json.dumps(config))
        loader = ConfigLoader(config_path)

        async def handler(request):
            if request.url.path == "/api/tags":
                return httpx.Response(200, json={})
            if request.url.path == "/api/generate":
                return httpx.Response(200, json={"response": "hello"})
            return httpx.Response(404)

        transport = httpx.MockTransport(handler)
        client = OllamaClient(loader)
        client.http_client = httpx.AsyncClient(transport=transport, base_url="http://test")
        assert await client.ensure_ready() is True
        text = await client.generate_text("ollama_mistral_7b", "hi")
        assert text == "hello"
        await client.close()

    asyncio.run(run())
