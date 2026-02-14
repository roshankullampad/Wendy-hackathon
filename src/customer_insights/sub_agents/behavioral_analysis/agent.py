from __future__ import annotations

from pathlib import Path

from google.adk.agents.llm_agent import LlmAgent

from src.customer_insights.sub_agents.behavioral_analysis.tools import (
    generate_synthetic_behavioral_data,
)
from src.utils.adk_agent_factory import build_llm_agent

NAME = "BehavioralAnalysisAgent"
DESCRIPTION = "Analyzes structured behavioral data with synthetic metrics."


def build_agent() -> LlmAgent:
    instruction_path = Path(__file__).with_name("instruction.txt")
    return build_llm_agent(
        name=NAME,
        description=DESCRIPTION,
        instruction_path=instruction_path,
        tools=[generate_synthetic_behavioral_data],
    )
