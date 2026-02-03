from __future__ import annotations

from typing import Any, Dict, List

from src.customer_insights.sub_agents.behavioral_analysis.agent import (
    BehavioralAnalysisAgent,
)
from src.customer_insights.sub_agents.profile_synthesizer.agent import (
    ProfileSynthesizerAgent,
)


class CustomerInsightsManagerAgent:
    """Sequential agent for customer behavioral analysis and synthesis."""

    name = "Customer Insights Manager"
    description = (
        "Runs behavioral analysis and profile synthesis to generate "
        "actionable customer insight segments."
    )

    def __init__(self) -> None:
        self.behavioral_analysis = BehavioralAnalysisAgent()
        self.profile_synthesizer = ProfileSynthesizerAgent()

    def run(self, query: str, logs: List[str] | None = None) -> List[Dict[str, Any]]:
        if logs is not None:
            logs.append("Customer Insights: Behavioral Analysis Agent running.")
        behavioral_payload = self.behavioral_analysis.run(query)

        if logs is not None:
            logs.append("Customer Insights: Profile Synthesizer Agent running.")
        customer_insights = self.profile_synthesizer.run(behavioral_payload)

        return customer_insights
