from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from src.utils.instruction_loader import load_instruction


class SimplifiedOfferDesignAgent:
    """Generates three offer concepts grounded in upstream insights."""

    name = "Simplified Offer Design Agent"
    description = "Synthesizes insights into 3 prioritized offer concepts."

    def __init__(self) -> None:
        instruction_path = Path(__file__).with_name("instruction.txt")
        self.instructions = load_instruction(instruction_path)

    def run(self, orchestrator_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        trend_briefs = orchestrator_payload.get("trend_briefs", [])
        customer_insights = orchestrator_payload.get("customer_insights", [])
        event_calendar = orchestrator_payload.get("event_calendar", {})

        trend_titles = [trend.get("title", "trend") for trend in trend_briefs[:3]]
        segment_ids = [segment.get("segment_id", "segment") for segment in customer_insights]
        events = event_calendar.get("high_velocity_events", [])

        event_names = [event.get("event_name", "Major Event") for event in events[:2]]

        offers = [
            {
                "priority_rank": 1,
                "title": "App-Exclusive Game Day Mega Bundle",
                "offer_summary": (
                    "A limited-time, app-exclusive bundle designed for game-day "
                    "watch parties with shareable sides and premium sandwiches."
                ),
                "success_hypothesis": (
                    "If Wendy's ties app-exclusive bundles to game-day moments, "
                    "families and groups will increase order size and repeat visits."
                ),
                "evidence_map": [
                    f"Trend: {trend_titles[0] if trend_titles else 'App-first value unlocks'}",
                    f"Event: {event_names[0] if event_names else 'Super Bowl LX'}",
                    f"Segment: {segment_ids[2] if len(segment_ids) > 2 else 'family-bundle-planner'}",
                ],
                "justification_points": [
                    "Bundles match group ordering behavior and reduce decision friction.",
                    "App exclusivity builds loyalty and improves data capture.",
                    "Game-day timing aligns with peak demand windows.",
                ],
            },
            {
                "priority_rank": 2,
                "title": "Late Night Heat Drop",
                "offer_summary": (
                    "Time-boxed late-night spicy combo with a digital reward "
                    "for repeat visits within 7 days."
                ),
                "success_hypothesis": (
                    "A craveable, spicy offer with a short redemption window will "
                    "drive frequency among late-night and Gen Z segments."
                ),
                "evidence_map": [
                    f"Trend: {trend_titles[2] if len(trend_titles) > 2 else 'Late-night craveable rewards'}",
                    f"Segment: {segment_ids[1] if len(segment_ids) > 1 else 'late-night-craver'}",
                    "Signal: Rising interest in late-night digital deals",
                ],
                "justification_points": [
                    "Time-boxed rewards motivate faster repeat visits.",
                    "Spicy variants differentiate Wendy's in a crowded market.",
                    "Late-night demand aligns with digital ordering habits.",
                ],
            },
            {
                "priority_rank": 3,
                "title": "Global Matchday Value Trio",
                "offer_summary": (
                    "Three-value meal combos inspired by global flavors, "
                    "aligned to international sports tournaments."
                ),
                "success_hypothesis": (
                    "Global flavor cues tied to major tournaments will increase "
                    "trial and social sharing while keeping value perceptions high."
                ),
                "evidence_map": [
                    f"Trend: {trend_titles[1] if len(trend_titles) > 1 else 'Family and group bundle momentum'}",
                    f"Event: {event_names[1] if len(event_names) > 1 else 'FIFA World Cup 2026'}",
                    f"Segment: {segment_ids[0] if segment_ids else 'value-driven-lunch-buyer'}",
                ],
                "justification_points": [
                    "Global events create built-in cultural moments for promotions.",
                    "Value trio format preserves affordability perception.",
                    "Flavor variety encourages social media discussion.",
                ],
            },
        ]

        return offers
