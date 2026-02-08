from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent

from src.utils.adk_agent_factory import build_llm_agent
from src.utils.adk_runner import (
    coerce_dict,
    extract_final_responses,
    parse_json_payload,
    run_agent,
)

AGENT_NAME = "Offer Orchestrator Agent"


def build_offer_orchestrator_agent() -> LlmAgent:
    instruction_path = Path(__file__).with_name("instruction.txt")
    return build_llm_agent(
        name=AGENT_NAME,
        description=OfferOrchestratorAgent.description,
        instruction_path=instruction_path,
    )


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=OfferOrchestratorAgent.name,
        description=OfferOrchestratorAgent.description,
        sub_agents=[build_offer_orchestrator_agent()],
    )


class OfferOrchestratorAgent:
    """Combines all upstream outputs into a single payload."""

    name = "Offer Orchestrator"
    description = "Combines trend briefs, customer insights, and events."

    def run(
        self,
        query: str,
        trend_briefs: List[Dict[str, Any]],
        customer_insights: List[Dict[str, Any]],
        event_calendar: Dict[str, Any],
    ) -> Dict[str, Any]:
        payload = {
            "research_topic": query,
            "trend_briefs": trend_briefs,
            "customer_insights": customer_insights,
            "event_calendar": event_calendar,
        }
        payload_text = json.dumps(payload, indent=2)
        events = run_agent(build_agent(), payload_text)
        outputs = extract_final_responses(events)
        orchestrator_text = outputs.get(AGENT_NAME, "")
        orchestrator_payload = parse_json_payload(orchestrator_text)
        return coerce_dict(orchestrator_payload)
