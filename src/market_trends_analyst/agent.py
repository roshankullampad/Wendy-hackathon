from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Dict, List

from google.adk.agents import SequentialAgent

# ADK loads apps with /workspace/src on sys.path; add project root so src.* imports resolve.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

ADK_ROOT_NAME = "market_trends_analyst"


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=ADK_ROOT_NAME,
        description=MarketTrendsAnalystRoot.description,
        sub_agents=[
            build_data_collection_agent(),
            build_research_synthesis_agent(),
        ],
    )


class MarketTrendsAnalystRoot:
    """Sequential agent that runs data collection then research synthesis."""

    name = "Market Trends Analyst"
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


root_agent = build_agent()
