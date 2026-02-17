from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Dict, List

from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent

# ADK loads apps with /workspace/src on sys.path; add project root so src.* imports resolve.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.adk_agent_factory import build_llm_agent
from src.utils.adk_runner import (
    coerce_dict,
    extract_final_responses,
    parse_json_payload,
    run_agent,
)

ADK_ROOT_NAME = "event_planner"
AGENT_NAME = "event_planner_agent"


def build_event_planner_agent() -> LlmAgent:
    instruction_path = Path(__file__).with_name("instruction.txt")
    return build_llm_agent(
        name=AGENT_NAME,
        description=EventManager.description,
        instruction_path=instruction_path,
    )


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=ADK_ROOT_NAME,
        description=EventManager.description,
        sub_agents=[build_event_planner_agent()],
    )


class EventManager:
    """LlmAgent-style planner that returns a 2026 event calendar."""

    name = "Event Planner"
    description = (
        "Identifies major 2026 sports and entertainment events that can "
        "drive fast-food demand."
    )

    def run(self, query: str, logs: List[str] | None = None) -> Dict[str, Any]:
        if logs is not None:
            logs.append("Event Planner: compiling 2026 high-velocity events.")

        events = run_agent(build_agent(), query)
        outputs = extract_final_responses(events)

        planner_text = outputs.get(AGENT_NAME, "")
        planner_payload = parse_json_payload(planner_text)
        return coerce_dict(planner_payload)


root_agent = build_agent()
