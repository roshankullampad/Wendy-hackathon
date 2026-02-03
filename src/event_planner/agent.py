from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from src.utils.instruction_loader import load_instruction


class EventManager:
    """LlmAgent-style planner that returns a 2026 event calendar."""

    name = "Event Planner"
    description = (
        "Identifies major 2026 sports and entertainment events that can "
        "drive fast-food demand."
    )

    def __init__(self) -> None:
        instruction_path = Path(__file__).with_name("instruction.txt")
        self.instructions = load_instruction(instruction_path)

    def run(self, query: str, logs: List[str] | None = None) -> Dict[str, Any]:
        if logs is not None:
            logs.append("Event Planner: compiling 2026 high-velocity events.")

        return {
            "year": 2026,
            "brand_focus": "Wendy's",
            "high_velocity_events": [
                {
                    "event_name": "Super Bowl LX",
                    "host_city": "TBD",
                    "date": "2026-02-08",
                    "potential_global_viewership": "120M+ projected",
                    "past_sales_history": "$3.8M projected lift",
                    "strategic_opportunity": "Game-day bundles and spicy offers.",
                    "target_segment": "Domestic US, multi-generational families",
                },
                {
                    "event_name": "FIFA World Cup 2026 (North America)",
                    "host_city": "Multiple cities (TBD)",
                    "date": "2026-06-11",
                    "potential_global_viewership": "4B+ global reach",
                    "past_sales_history": "$5.1M projected lift",
                    "strategic_opportunity": "Match-day value meals and shareable combos.",
                    "target_segment": "Global fans, soccer-first households",
                },
                {
                    "event_name": "Winter Olympics 2026 (Milan-Cortina)",
                    "host_city": "Milan-Cortina",
                    "date": "2026-02-06",
                    "potential_global_viewership": "2B+ global reach",
                    "past_sales_history": "$2.4M projected lift",
                    "strategic_opportunity": "Limited-time international flavor menu.",
                    "target_segment": "Sports enthusiasts and adventure-seeking diners",
                },
            ],
        }
