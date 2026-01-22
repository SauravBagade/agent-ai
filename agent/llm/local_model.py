# agent/llm/local_model.py

import os
import requests

class LocalModel:
    """
    Local LLM for parsing + lightweight reasoning.
    Optimized for:
      - logs
      - errors
      - outputs
      - small transformations

    Default backend: OLLAMA (offline)
      example models:
        - llama3
        - qwen2
        - mistral
        - codellama
    """

    def __init__(self):
        self.backend = os.getenv("LOCAL_LLM_PROVIDER", "ollama").lower()
        self.model = os.getenv("LOCAL_LLM_MODEL", "llama3")
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def generate(self, prompt: str) -> str:
        """
        Unified interface for local inference.
        """

        if self.backend == "ollama":
            return self._call_ollama(prompt)

        return f"[local-disabled, backend={self.backend}] {prompt}"

    # --- OLLAMA CALL ---

    def _call_ollama(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt
        }

        try:
            resp = requests.post(f"{self.host}/api/generate", json=payload)
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
            return f"[ollama-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[ollama-connection-error] {str(e)}"

