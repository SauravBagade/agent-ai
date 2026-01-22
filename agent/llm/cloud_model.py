# agent/llm/cloud_model.py

import os

class CloudModel:
    """
    Cloud LLM for reasoning + planning + explanation.

    Supports:
      - Anthropic Claude
      - OpenAI GPT
      - Cohere
      - Future AWS Bedrock

    Used for:
      - Plan generation
      - Debug explanation
      - CI/CD analysis
      - Kubernetes troubleshooting
      - Terraform reasoning
    """

    def __init__(self):
        self.provider = os.getenv("CLOUD_LLM_PROVIDER", "anthropic").lower()
        self.model = os.getenv("CLOUD_LLM_MODEL", "claude-3-sonnet")

        # lazy SDK setup
        self._setup_provider()

    def _setup_provider(self):
        if self.provider == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            except ImportError:
                self.client = None

        elif self.provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except ImportError:
                self.client = None

        elif self.provider == "cohere":
            try:
                import cohere
                self.client = cohere.Client(os.getenv("COHERE_API_KEY"))
            except ImportError:
                self.client = None

        else:
            self.client = None

    def generate(self, prompt: str) -> str:
        """
        Unified generation interface for all cloud LLM providers.
        """

        if self.client is None:
            return f"[cloud-disabled] {prompt}"

        if self.provider == "anthropic":
            return self._call_anthropic(prompt)

        if self.provider == "openai":
            return self._call_openai(prompt)

        if self.provider == "cohere":
            return self._call_cohere(prompt)

        return f"[unknown-provider:{self.provider}] {prompt}"

    # --- Individual Provider Handlers ---

    def _call_anthropic(self, prompt: str) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256
            )
            return response.content[0].text
        except Exception as e:
            return f"[anthropic-error] {str(e)}"

    def _call_openai(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[openai-error] {str(e)}"

    def _call_cohere(self, prompt: str) -> str:
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                max_tokens=200
            )
            return response.text
        except Exception as e:
            return f"[cohere-error] {str(e)}"

