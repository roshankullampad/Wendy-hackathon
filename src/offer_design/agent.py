from __future__ import annotations

from typing import Any, Dict, List

from src.offer_design.sub_agents.simplified_offer_design.agent import (
    SimplifiedOfferDesignAgent,
)


class OfferDesignRootAgent:
    """Root agent that delegates to the simplified offer design agent."""

    name = "Offer Design Root"
    description = "Generates offer concepts based on orchestrated insights."

    def __init__(self) -> None:
        self.simplified_agent = SimplifiedOfferDesignAgent()

    def run(
        self, orchestrator_payload: Dict[str, Any], logs: List[str] | None = None
    ) -> List[Dict[str, Any]]:
        if logs is not None:
            logs.append("Offer Design: SimplifiedOfferDesignAgent running.")
        return self.simplified_agent.run(orchestrator_payload)
