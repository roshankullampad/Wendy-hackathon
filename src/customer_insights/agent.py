from __future__ import annotations

from typing import Any, Dict, List

from google.adk.agents import SequentialAgent

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


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=CustomerInsightsManagerAgent.name,
        description=CustomerInsightsManagerAgent.description,
        sub_agents=[
            build_behavioral_analysis_agent(),
            build_profile_synthesizer_agent(),
        ],
    )


class CustomerInsightsManagerAgent:
    """Sequential agent for customer behavioral analysis and synthesis."""

    name = "CustomerInsightsManagerAgent"
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


# Export root_agent for ADK discovery
root_agent = build_agent()
