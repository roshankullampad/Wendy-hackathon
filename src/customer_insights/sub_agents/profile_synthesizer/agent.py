from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from src.utils.instruction_loader import load_instruction


class ProfileSynthesizerAgent:
    """Synthesizes behavioral metrics into narrative segment profiles."""

    name = "Profile Synthesizer Agent"
    description = "Creates narrative customer insights from behavioral metrics."

    def __init__(self) -> None:
        instruction_path = Path(__file__).with_name("instruction.txt")
        self.instructions = load_instruction(instruction_path)

    def run(self, behavioral_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        segments = behavioral_payload.get("segments", [])
        insights = []

        for segment in segments:
            segment_id = segment.get("segment_id", "unknown-segment")
            metrics = segment.get("empirical_metrics", {})
            patterns = segment.get("behavioral_patterns", [])

            narrative = (
                f"{segment_id.replace('-', ' ').title()} shoppers tend to respond to "
                f"{metrics.get('channel_preference', 'digital')} offers with a "
                f"{metrics.get('redemption_rate', '1.0x')} redemption lift. "
                "They value convenience and clear value messaging."
            )

            insights.append(
                {
                    "segment_id": segment_id,
                    "description": narrative,
                    "preferred_mechanics": [
                        "BOGO",
                        "time-boxed",
                        "app-exclusive",
                    ],
                    "key_messaging_phrases": [
                        "limited-time value",
                        "easy redemption",
                        "exclusive reward",
                    ],
                    "empirical_metrics": metrics,
                    "behavioral_patterns": patterns,
                }
            )

        return insights
