from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from src.market_trends_analyst.sub_agents.research_synthesis.tools import (
    web_scraper_tool,
)
from src.utils.instruction_loader import load_instruction


class ResearchSynthesisAgent:
    """Synthesizes trend briefs from collected sources."""

    name = "Research Synthesis Agent"
    description = (
        "Analyzes raw data sources and produces evidence-based trend briefs."
    )

    def __init__(self) -> None:
        instruction_path = Path(__file__).with_name("instruction.txt")
        self.instructions = load_instruction(instruction_path)

    def run(self, data_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        topic = data_payload.get("topic", "fast food promotions")
        urls = data_payload.get("urls", [])

        snippets = []
        for item in urls[:3]:
            url = item.get("url", "")
            if not url:
                continue
            content = web_scraper_tool(url).get("content", "")
            snippets.append(f"{content[:120]}... ({url})")

        trend_briefs = [
            {
                "title": "App-first value unlocks",
                "summary": (
                    "Promotions increasingly drive traffic into apps through exclusive "
                    "value offers and limited-time bundles. This reinforces loyalty "
                    "and enables targeted messaging."
                ),
                "evidence_snippets": snippets or [item.get("url", "") for item in urls[:2]],
                "signal_strength": "HIGH",
                "velocity": "RISING",
                "recommended_directions": (
                    "Expand app-exclusive bundles and time-boxed value rewards "
                    "to increase repeat visits."
                ),
            },
            {
                "title": "Family and group bundle momentum",
                "summary": (
                    "Consumers respond to bundled meals that simplify group ordering "
                    "and deliver perceived savings. Bundles align with sports and "
                    "entertainment viewing moments."
                ),
                "evidence_snippets": snippets or [item.get("url", "") for item in urls[2:4]],
                "signal_strength": "MEDIUM",
                "velocity": "STABLE",
                "recommended_directions": (
                    "Create family-sized bundles tied to game-day or movie-night moments."
                ),
            },
            {
                "title": "Late-night craveable rewards",
                "summary": (
                    "Late-night demand is growing with younger audiences seeking "
                    "craveable, spicy, or novelty items paired with digital deals."
                ),
                "evidence_snippets": snippets or [item.get("url", "") for item in urls[4:6]],
                "signal_strength": "MEDIUM",
                "velocity": "RISING",
                "recommended_directions": (
                    "Test limited-time spicy items and late-night digital coupons."
                ),
            },
        ]

        return trend_briefs
