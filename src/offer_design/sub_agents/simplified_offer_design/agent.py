from __future__ import annotations

from pathlib import Path

from google.adk.agents.llm_agent import LlmAgent

from src.utils.adk_agent_factory import build_llm_agent

NAME = "Simplified Offer Design Agent"
DESCRIPTION = "Synthesizes insights into 3 prioritized offer concepts."


def build_agent() -> LlmAgent:
    instruction_path = Path(__file__).with_name("instruction.txt")
    return build_llm_agent(
        name=NAME,
        description=DESCRIPTION,
        instruction_path=instruction_path,
    )
