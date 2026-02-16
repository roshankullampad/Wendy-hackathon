from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Dict, List, Tuple

from google.adk.agents import SequentialAgent

# ADK loads apps with /workspace/src on sys.path; add project root so src.* imports resolve.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.customer_insights.agent import CustomerInsightsManagerAgent, build_agent as build_customer_insights_agent
from src.customer_insights.sub_agents.profile_synthesizer.agent import (
    NAME as PROFILE_SYNTHESIZER_NAME,
)
from src.event_planner.agent import (
    AGENT_NAME as EVENT_PLANNER_AGENT_NAME,
    EventManager,
    build_agent as build_event_planner_agent,
)
from src.market_trends_analyst.agent import (
    MarketTrendsAnalystRoot,
    build_agent as build_market_trends_agent,
)
from src.market_trends_analyst.sub_agents.research_synthesis.agent import (
    NAME as RESEARCH_SYNTHESIS_NAME,
)
from src.offer_design.agent import build_agent as build_offer_design_agent
from src.offer_design.sub_agents.simplified_offer_design.agent import (
    NAME as SIMPLIFIED_OFFER_DESIGN_NAME,
)
from src.orchestrator.agent import build_agent as build_offer_orchestrator_agent
from src.utils.adk_runner import (
    coerce_dict,
    coerce_list,
    extract_final_responses,
    parse_json_payload,
    run_agent,
)

ADK_ROOT_NAME = "marketing_orchestrator"


def build_agent() -> SequentialAgent:
    return SequentialAgent(
        name=ADK_ROOT_NAME,
        description=MarketingOrchestrator.description,
        sub_agents=[
            build_market_trends_agent(),
            build_customer_insights_agent(),
            build_event_planner_agent(),
            build_offer_orchestrator_agent(),
            build_offer_design_agent(),
        ],
    )


class MarketingOrchestrator:
    """Root agent that runs the full workflow in sequence."""

    name = "Marketing Orchestrator"
    description = (
        "Coordinates the market trends, customer insights, event planning, "
        "and offer design agents in sequence."
    )

    def run(self, query: str) -> Tuple[Dict[str, Any], List[str]]:
        logs: List[str] = []

        logs.append("Step 1: Market Trends Analyst started.")
        logs.append("Step 2: Customer Insights started.")
        logs.append("Step 3: Event Planner started.")
        logs.append("Step 4: Offer Orchestrator started.")
        logs.append("Step 5: Offer Design started.")

        events = run_agent(build_agent(), query)
        outputs = extract_final_responses(events)

        logs.append("Step 1: Market Trends Analyst completed.")
        logs.append("Step 2: Customer Insights completed.")
        logs.append("Step 3: Event Planner completed.")
        logs.append("Step 4: Offer Orchestrator completed.")
        logs.append("Step 5: Offer Design completed.")

        trend_payload = parse_json_payload(outputs.get(RESEARCH_SYNTHESIS_NAME, ""))
        customer_payload = parse_json_payload(outputs.get(PROFILE_SYNTHESIZER_NAME, ""))
        event_payload = parse_json_payload(outputs.get(EVENT_PLANNER_AGENT_NAME, ""))
        offer_payload = parse_json_payload(outputs.get(SIMPLIFIED_OFFER_DESIGN_NAME, ""))

        trend_briefs = coerce_list(trend_payload, key="trend_briefs")
        customer_insights = coerce_list(customer_payload, key="customer_insights")
        event_calendar = coerce_dict(event_payload)
        offer_concepts = coerce_list(offer_payload, key="offer_concepts")

        output = {
            "trend_briefs": trend_briefs,
            "customer_insights": customer_insights,
            "event_calendar": event_calendar,
            "offer_concepts": offer_concepts,
        }
        return output, logs


OFFER_DESIGN_LABEL = "Offer Design"


def _run_offer_design_workflow(query: str, logs: List[str]) -> Dict[str, Any]:
    logs.append("Offer Design requires upstream insights; running dependencies.")
    output, orchestrator_logs = MarketingOrchestrator().run(query)
    logs.extend(orchestrator_logs)
    return {"offer_concepts": output.get("offer_concepts", [])}


def run_workflow(query: str, agent_name: str | None = None) -> Tuple[Dict[str, Any], List[str]]:
    """Convenience function for the UI."""
    if not agent_name or agent_name == MarketingOrchestrator.name:
        orchestrator = MarketingOrchestrator()
        output, logs = orchestrator.run(query)
        logs.insert(0, f"Selected agent: {MarketingOrchestrator.name}.")
        return output, logs

    logs: List[str] = [f"Selected agent: {agent_name}."]
    if agent_name == MarketTrendsAnalystRoot.name:
        logs.append("Market Trends Analyst started.")
        trend_briefs = MarketTrendsAnalystRoot().run(query, logs=logs)
        logs.append("Market Trends Analyst completed.")
        return {"trend_briefs": trend_briefs}, logs
    if agent_name == CustomerInsightsManagerAgent.name:
        logs.append("Customer Insights Manager started.")
        customer_insights = CustomerInsightsManagerAgent().run(query, logs=logs)
        logs.append("Customer Insights Manager completed.")
        return {"customer_insights": customer_insights}, logs
    if agent_name == EventManager.name:
        logs.append("Event Planner started.")
        event_calendar = EventManager().run(query, logs=logs)
        logs.append("Event Planner completed.")
        return {"event_calendar": event_calendar}, logs
    if agent_name == OFFER_DESIGN_LABEL:
        logs.append("Offer Design started.")
        results = _run_offer_design_workflow(query, logs)
        logs.append("Offer Design completed.")
        return results, logs

    logs.append(f"Unknown agent '{agent_name}'. Falling back to Marketing Orchestrator.")
    output, orchestrator_logs = MarketingOrchestrator().run(query)
    logs.extend(orchestrator_logs)
    return output, logs


root_agent = build_agent()
