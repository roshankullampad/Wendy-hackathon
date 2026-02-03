from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from src.market_trends_analyst.sub_agents.data_collection.tools import google_search
from src.utils.instruction_loader import load_instruction


class DataCollectionAgent:
    """Collects raw URLs and data points using search tools."""

    name = "Data Collection Agent"
    description = (
        "Fetches raw data points and URLs from search tools without analyzing content."
    )

    def __init__(self) -> None:
        instruction_path = Path(__file__).with_name("instruction.txt")
        self.instructions = load_instruction(instruction_path)

    def run(self, query: str) -> Dict[str, Any]:
        urls = google_search(query, limit=12)
        return {
            "topic": query,
            "urls": urls,
            "notes": "Sample sources collected via google_search.",
        }
