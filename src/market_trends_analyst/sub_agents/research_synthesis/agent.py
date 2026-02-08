from __future__ import annotations

from pathlib import Path

from google.adk.agents.llm_agent import LlmAgent

from src.market_trends_analyst.sub_agents.research_synthesis.tools import (
    web_scraper_tool,
)
from src.utils.adk_agent_factory import build_llm_agent

NAME = "Research Synthesis Agent"
DESCRIPTION = "Analyzes raw data sources and produces evidence-based trend briefs."


def build_agent() -> LlmAgent:
    instruction_path = Path(__file__).with_name("instruction.txt")
    return build_llm_agent(
        name=NAME,
        description=DESCRIPTION,
        instruction_path=instruction_path,
        tools=[web_scraper_tool],
    )
