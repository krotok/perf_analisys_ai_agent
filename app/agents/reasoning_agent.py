# LLM bottleneck analysis

# Expected answer
# {
#   "root_causes": [
#     {
#       "cause": "CPU saturation",
#       "confidence": 0.82,
#       "evidence": [
#         "CPU usage > 90%",
#         "Latency increases with RPS",
#         "No HPA enabled"
#       ]
#     },
#     {
#       "cause": "Database connection pool exhaustion",
#       "confidence": 0.64,
#       "evidence": [
#         "Timeout errors in logs",
#         "p99 latency spikes",
#         "Recent DB config change"
#       ]
#     }
#   ]
# }

from typing import Dict, Any
from app.integrations.llm import LLMClient


SYSTEM_PROMPT = """
You are an expert Site Reliability Engineer and Performance Engineer.

Your task:
- Analyze latency degradation symptoms
- Identify probable bottlenecks
- Provide confidence scores
- Base conclusions ONLY on provided data

Rules:
- Do NOT invent metrics
- Do NOT propose changes without evidence
- Prefer infrastructure and runtime causes first
- Output MUST be valid JSON
"""


class ReasoningAgent:
    """
    LLM-based bottleneck reasoning agent.
    """

    def __init__(self, settings):
        self.llm = LLMClient(
            provider=settings.llm_provider,
            model=settings.llm_model,
        )

    def analyze(
        self,
        symptom: str,
        metrics: Dict[str, Any],
        logs: Dict[str, Any],
        k8s: Dict[str, Any],
        code: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        payload = {
            "symptom": symptom,
            "metrics": metrics,
            "logs": logs,
            "kubernetes": k8s,
            "recent_code_changes": code or {},
        }

        result = self.llm.reason(
            system_prompt=SYSTEM_PROMPT,
            user_payload=payload,
        )

        self._validate_result(result)
        return result

    # ---------------- validation ----------------

    def _validate_result(self, result: Dict[str, Any]):
        """
        Ensures LLM output follows expected contract.
        """
        if "root_causes" not in result:
            raise RuntimeError("LLM output missing 'root_causes' field")

        for cause in result["root_causes"]:
            if not all(k in cause for k in ("cause", "confidence", "evidence")):
                raise RuntimeError(
                    f"Invalid root cause format: {cause}"
                )

            if not (0.0 <= cause["confidence"] <= 1.0):
                raise RuntimeError(
                    f"Confidence out of range: {cause}"
                )
