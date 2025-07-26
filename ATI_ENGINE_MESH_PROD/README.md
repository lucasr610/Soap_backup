# ATI Engine Mesh Production

This directory holds configuration files for deployment of the ATI Engine Mesh in production.

## Environment Variables

The config loader reads the following variables:

- `ATI_LLM_ENDPOINT` – URL of the large language model API.
- `ATI_EMBEDDING_ENDPOINT` – URL of the embedding service API.
- `ATI_API_KEY_PATH` – Filesystem path to the API key used by the services.

If these variables are not set, `config_loader.py` falls back to values in `configs/ai_config.json`.
