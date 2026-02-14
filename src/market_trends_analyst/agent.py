from __future__ import annotations

from typing import Any, Dict, List

from google.adk.agents import SequentialAgent

from src.market_trends_analyst.sub_agents.data_collection.agent import (
    build_agent as build_data_collection_agent,
)
from src.market_trends_analyst.sub_agents.research_synthesis.agent import (
    NAME as RESEARCH_SYNTHESIS_NAME,
)
from src.market_trends_analyst.sub_agents.research_synthesis.agent import (
    build_agent as build_research_synthesis_agent,
)
from src.utils.adk_runner import (
    coerce_list,
    extract_final_responses,
    parse_json_payload,
    run_agent,
)


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=MarketTrendsAnalystRoot.name,
        description=MarketTrendsAnalystRoot.description,
        sub_agents=[
            build_data_collection_agent(),
            build_research_synthesis_agent(),
        ],
    )


class MarketTrendsAnalystRoot:
    """Sequential agent that runs data collection then research synthesis."""

    name = "MarketTrendsAnalyst"
    description = (
        "Analyzes fast food market trends by collecting sources and "
        "synthesizing them into trend briefs."
    )

    def run(self, query: str, logs: List[str] | None = None) -> List[Dict[str, Any]]:
        if logs is not None:
            logs.append("Market Trends: Data Collection Agent running.")
            logs.append("Market Trends: Research Synthesis Agent running.")

        events = run_agent(build_agent(), query)
        outputs = extract_final_responses(events)

        synthesis_text = outputs.get(RESEARCH_SYNTHESIS_NAME, "")
        synthesis_payload = parse_json_payload(synthesis_text)
        trend_briefs = coerce_list(synthesis_payload, key="trend_briefs")
        if not trend_briefs and synthesis_payload is None:
            trend_briefs = []
        return trend_briefs


# Export root_agent for ADK discovery
root_agent = build_agent()
