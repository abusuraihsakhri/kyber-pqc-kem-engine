"""
Deterministic mock response provider with identifier pattern checks.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Kyber Pqc Kem Engine"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} demo assistant]: No cryptographic validation was performed. Received query: '{prompt[:60]}...'. Use the audit endpoint for local threshold checks."


class LLMFactory:
    """Only deterministic local mock mode is implemented."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Kyber Pqc Kem Engine"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        raise ValueError(f"Unsupported provider {provider!r}; only mock is implemented")
