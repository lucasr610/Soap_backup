# ATI Engine Mesh Production

This directory holds configuration files and utility scripts for deploying and managing the ATI Engine Mesh in production environments.

---

## 🔧 Environment Configuration

The config loader reads the following environment variables:

- `ATI_LLM_ENDPOINT` – URL of the large language model API  
- `ATI_EMBEDDING_ENDPOINT` – URL of the embedding service API  
- `ATI_API_KEY_PATH` – Filesystem path to the API key used by the services  

If these variables are not set, `config_loader.py` falls back to values defined in `configs/ai_config.json`.

---

## 🚀 `push_to_github.py`

This script pushes the current repository to a GitHub remote. It determines the repository URL and target branch from the following sources, in order:

1. Environment variables:  
   - `REPO_URL`  
   - `BRANCH_NAME`
2. A `config.json` file located next to the script:
   ```json
   {
     "repo_url": "https://github.com/myorg/myrepo.git",
     "branch": "main"
   }
