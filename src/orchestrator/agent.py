from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from src.utils.instruction_loader import load_instruction


class OfferOrchestratorAgent:
    """Combines all upstream outputs into a single payload."""

    name = "Offer Orchestrator"
    description = "Combines trend briefs, customer insights, and events."

    def __init__(self) -> None:
        instruction_path = Path(__file__).with_name("instruction.txt")
        self.instructions = load_instruction(instruction_path)

    def run(
        self,
        query: str,
        trend_briefs: List[Dict[str, Any]],
        customer_insights: List[Dict[str, Any]],
        event_calendar: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "research_topic": query,
            "trend_briefs": trend_briefs,
            "customer_insights": customer_insights,
            "event_calendar": event_calendar,
        }
