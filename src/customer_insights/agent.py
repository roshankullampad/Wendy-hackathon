from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Dict, List

from google.adk.agents import SequentialAgent

# ADK loads apps with /workspace/src on sys.path; add project root so src.* imports resolve.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.customer_insights.sub_agents.behavioral_analysis.agent import (
    build_agent as build_behavioral_analysis_agent,
)
from src.customer_insights.sub_agents.profile_synthesizer.agent import (
    NAME as PROFILE_SYNTHESIZER_NAME,
)
from src.customer_insights.sub_agents.profile_synthesizer.agent import (
    build_agent as build_profile_synthesizer_agent,
)
from src.utils.adk_runner import (
    coerce_list,
    extract_final_responses,
    parse_json_payload,
    run_agent,
)

ADK_ROOT_NAME = "customer_insights_manager"


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=ADK_ROOT_NAME,
        description=CustomerInsightsManagerAgent.description,
        sub_agents=[
            build_behavioral_analysis_agent(),
            build_profile_synthesizer_agent(),
        ],
    )


class CustomerInsightsManagerAgent:
    """Sequential agent for customer behavioral analysis and synthesis."""

    name = "Customer Insights Manager"
    description = (
        "Runs behavioral analysis and profile synthesis to generate "
        "actionable customer insight segments."
    )

    def run(self, query: str, logs: List[str] | None = None) -> List[Dict[str, Any]]:
        if logs is not None:
            logs.append("Customer Insights: Behavioral Analysis Agent running.")
            logs.append("Customer Insights: Profile Synthesizer Agent running.")

        events = run_agent(build_agent(), query)
        outputs = extract_final_responses(events)

        profile_text = outputs.get(PROFILE_SYNTHESIZER_NAME, "")
        profile_payload = parse_json_payload(profile_text)
        insights = coerce_list(profile_payload, key="customer_insights")
        if not insights and profile_payload is None:
            insights = []
        return insights


root_agent = build_agent()
