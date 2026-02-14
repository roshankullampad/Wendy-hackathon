from __future__ import annotations

from pathlib import Path

from google.adk.agents.llm_agent import LlmAgent

from src.market_trends_analyst.sub_agents.data_collection.tools import google_search
from src.utils.adk_agent_factory import build_llm_agent

NAME = "DataCollectionAgent"
DESCRIPTION = "Fetches raw data points and URLs from search tools without analyzing content."


def build_agent() -> LlmAgent:
    instruction_path = Path(__file__).with_name("instruction.txt")
    return build_llm_agent(
        name=NAME,
        description=DESCRIPTION,
        instruction_path=instruction_path,
        tools=[google_search],
    )
