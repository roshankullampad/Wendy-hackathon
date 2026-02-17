from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Dict, List

from google.adk.agents import SequentialAgent

# ADK loads apps with /workspace/src on sys.path; add project root so src.* imports resolve.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.offer_design.sub_agents.simplified_offer_design.agent import (
    NAME as SIMPLIFIED_OFFER_DESIGN_NAME,
)
from src.offer_design.sub_agents.simplified_offer_design.agent import (
    build_agent as build_simplified_offer_agent,
)
from src.utils.adk_runner import (
    coerce_list,
    extract_final_responses,
    parse_json_payload,
    run_agent,
)

ADK_ROOT_NAME = "offer_design_root"


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=ADK_ROOT_NAME,
        description=OfferDesignRootAgent.description,
        sub_agents=[build_simplified_offer_agent()],
    )


class OfferDesignRootAgent:
    """Root agent that delegates to the simplified offer design agent."""

    name = "Offer Design Root"
    description = "Generates offer concepts based on orchestrated insights."

    def run(
        self, orchestrator_payload: Dict[str, Any], logs: List[str] | None = None
    ) -> List[Dict[str, Any]]:
        if logs is not None:
            logs.append("Offer Design: SimplifiedOfferDesignAgent running.")

        payload_text = json.dumps(orchestrator_payload, indent=2)
        events = run_agent(build_agent(), payload_text)
        outputs = extract_final_responses(events)

        offer_text = outputs.get(SIMPLIFIED_OFFER_DESIGN_NAME, "")
        offer_payload = parse_json_payload(offer_text)
        offer_concepts = coerce_list(offer_payload, key="offer_concepts")
        if not offer_concepts and offer_payload is None:
            offer_concepts = []
        return offer_concepts


root_agent = build_agent()
