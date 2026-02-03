from __future__ import annotations

from typing import Any, Dict, List, Tuple

from src.customer_insights.agent import CustomerInsightsManagerAgent
from src.event_planner.agent import EventManager
from src.market_trends_analyst.agent import MarketTrendsAnalystRoot
from src.offer_design.agent import OfferDesignRootAgent
from src.orchestrator.agent import OfferOrchestratorAgent


class MarketingOrchestrator:
    """Root agent that runs the full workflow in sequence."""

    name = "Marketing Orchestrator"
    description = (
        "Coordinates the market trends, customer insights, event planning, "
        "and offer design agents in sequence."
    )

    def __init__(self) -> None:
        self.market_trends = MarketTrendsAnalystRoot()
        self.customer_insights = CustomerInsightsManagerAgent()
        self.event_manager = EventManager()
        self.offer_orchestrator = OfferOrchestratorAgent()
        self.offer_design = OfferDesignRootAgent()

    def run(self, query: str) -> Tuple[Dict[str, Any], List[str]]:
        logs: List[str] = []

        logs.append("Step 1: Market Trends Analyst started.")
        trend_briefs = self.market_trends.run(query, logs=logs)
        logs.append("Step 1: Market Trends Analyst completed.")

        logs.append("Step 2: Customer Insights started.")
        customer_insights = self.customer_insights.run(query, logs=logs)
        logs.append("Step 2: Customer Insights completed.")

        logs.append("Step 3: Event Planner started.")
        event_calendar = self.event_manager.run(query, logs=logs)
        logs.append("Step 3: Event Planner completed.")

        logs.append("Step 4: Offer Orchestrator started.")
        orchestrator_payload = self.offer_orchestrator.run(
            query=query,
            trend_briefs=trend_briefs,
            customer_insights=customer_insights,
            event_calendar=event_calendar,
        )
        logs.append("Step 4: Offer Orchestrator completed.")

        logs.append("Step 5: Offer Design started.")
        offer_concepts = self.offer_design.run(orchestrator_payload, logs=logs)
        logs.append("Step 5: Offer Design completed.")

        output = {
            "trend_briefs": trend_briefs,
            "customer_insights": customer_insights,
            "event_calendar": event_calendar,
            "offer_concepts": offer_concepts,
        }
        return output, logs


def run_workflow(query: str) -> Tuple[Dict[str, Any], List[str]]:
    """Convenience function for the UI."""
    orchestrator = MarketingOrchestrator()
    return orchestrator.run(query)
