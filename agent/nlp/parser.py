# agent/nlp/parser.py

import re

class Parser:
    """
    Extracts entities from natural language queries.
    Entities include:
      - app/service name (nginx, api, backend)
      - replicas / scale (scale to 3)
      - namespace (dev, staging, prod)
      - image (nginx:1.27)
      - version (v1, v2)
      - cloud provider (aws, gcp, azure)
      - cluster (eks, aks, gke)
    """

    def parse(self, query: str) -> dict:
        text = query.lower()

        result = {
            "app": self._extract_app(text),
            "replicas": self._extract_replicas(text),
            "namespace": self._extract_namespace(text),
            "image": self._extract_image(text),
            "version": self._extract_version(text),
            "provider": self._extract_provider(text),
            "cluster": self._extract_cluster(text),
        }

        # remove empty values
        return {k: v for k, v in result.items() if v is not None}

    # --- Extractors ---

    def _extract_app(self, text: str):
        # naive approach for now, later use NER or LLM
        words = ["nginx", "api", "backend", "frontend", "mysql", "redis"]
        for w in words:
            if w in text:
                return w
        return self._extract_generic_name(text)

    def _extract_replicas(self, text: str):
        match = re.search(r"(\d+)\s*(replicas?|instances?|pods?)", text)
        if match:
            return int(match.group(1))

        match = re.search(r"scale\s*(to)?\s*(\d+)", text)
        if match:
            return int(match.group(2))
        return None

    def _extract_namespace(self, text: str):
        for ns in ["dev", "staging", "prod", "production", "test", "default"]:
            if f"{ns}" in text:
                return ns
        return None

    def _extract_provider(self, text: str):
        for cloud in ["aws", "gcp", "azure"]:
            if cloud in text:
                return cloud
        return None

    def _extract_cluster(self, text: str):
        for c in ["eks", "aks", "gke", "k3s", "minikube"]:
            if c in text:
                return c
        return None

    def _extract_image(self, text: str):
        match = re.search(r"([a-z0-9\-]+)/?([a-z0-9\-]+):([a-z0-9\.\-]+)", text)
        if match:
            return match.group(0)
        return None

    def _extract_version(self, text: str):
        match = re.search(r"v[0-9]+(\.[0-9]+)?", text)
        if match:
            return match.group(0)
        return None

    def _extract_generic_name(self, text: str):
        # generic fallback: first noun-ish piece
        parts = text.split()
        for p in parts:
            if p.isalpha() and len(p) > 2:
                return p
        return None
