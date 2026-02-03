from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.customer_insights.sub_agents.behavioral_analysis.tools import (
    generate_synthetic_behavioral_data,
)
from src.utils.instruction_loader import load_instruction


class BehavioralAnalysisAgent:
    """Generates synthetic behavioral segments and metrics."""

    name = "Behavioral Analysis Agent"
    description = "Analyzes structured behavioral data with synthetic metrics."

    def __init__(self) -> None:
        instruction_path = Path(__file__).with_name("instruction.txt")
        self.instructions = load_instruction(instruction_path)

    def run(self, query: str) -> Dict[str, Any]:
        segments = generate_synthetic_behavioral_data(num_segments=3)
        return {
            "topic": query,
            "segments": segments,
        }
