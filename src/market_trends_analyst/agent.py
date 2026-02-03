from __future__ import annotations

from typing import Any, Dict, List

from src.market_trends_analyst.sub_agents.data_collection.agent import DataCollectionAgent
from src.market_trends_analyst.sub_agents.research_synthesis.agent import (
    ResearchSynthesisAgent,
)


class MarketTrendsAnalystRoot:
    """Sequential agent that runs data collection then research synthesis."""

    name = "Market Trends Analyst"
    description = (
        "Analyzes fast food market trends by collecting sources and "
        "synthesizing them into trend briefs."
    )

    def __init__(self) -> None:
        self.data_collection = DataCollectionAgent()
        self.research_synthesis = ResearchSynthesisAgent()

    def run(self, query: str, logs: List[str] | None = None) -> List[Dict[str, Any]]:
        if logs is not None:
            logs.append("Market Trends: Data Collection Agent running.")
        data_payload = self.data_collection.run(query)

        if logs is not None:
            logs.append("Market Trends: Research Synthesis Agent running.")
        trend_briefs = self.research_synthesis.run(data_payload)

        return trend_briefs
