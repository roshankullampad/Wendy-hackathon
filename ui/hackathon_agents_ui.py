from __future__ import annotations

import os
import sys
import time
from typing import Any, Dict, List

import streamlit as st


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.marketing_orchestrator.agent import run_workflow  # noqa: E402


AGENT_DESCRIPTIONS = {
    "Marketing Orchestrator": (
        "Coordinates the market trends, customer insights, event planner, "
        "and offer design agents in sequence."
    ),
    "Market Trends Analyst": (
        "Collects sources and synthesizes fast-food promotional trend briefs."
    ),
    "Customer Insights Manager": (
        "Generates synthetic customer behavioral segments and profiles."
    ),
    "Event Planner": "Builds the 2026 event calendar with viewership signals.",
    "Offer Design": "Turns insights into 3 prioritized offer concepts.",
}


def render_offer_card(offer: Dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 18px; font-weight: 700; margin-bottom: 8px;">
                {offer.get("priority_rank", "")}. {offer.get("title", "Offer Concept")}
            </div>
            <div style="margin-bottom: 10px;">
                <strong>Summary:</strong> {offer.get("offer_summary", "")}
            </div>
            <div style="margin-bottom: 10px;">
                <strong>Success Hypothesis:</strong> {offer.get("success_hypothesis", "")}
            </div>
            <div style="margin-bottom: 10px;">
                <strong>Evidence Map:</strong>
                <ul>
                    {''.join([f"<li>{item}</li>" for item in offer.get("evidence_map", [])])}
                </ul>
            </div>
            <div style="margin-bottom: 0;">
                <strong>Key Reasons:</strong>
                <ul>
                    {''.join([f"<li>{item}</li>" for item in offer.get("justification_points", [])])}
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="Wendy's AI Agents", layout="wide")
    st.title("Wendy's AI Agents Hackathon")

    with st.sidebar:
        st.header("Agent Selector")
        selected_agent = st.selectbox("Select an agent", list(AGENT_DESCRIPTIONS.keys()))
        st.markdown(AGENT_DESCRIPTIONS[selected_agent])
        st.divider()
        st.caption(
            "Workflow: Market Trends Analyst -> Customer Insights -> Event Planner -> Offer Design"
        )

    query_tab, results_tab = st.tabs(["Query", "Results"])

    with query_tab:
        st.subheader("Research Query")
        query = st.text_input(
            "Enter a research topic",
            value=st.session_state.get("last_query", "Gen Z late night craving trends"),
        )
        run_button = st.button("Run Workflow", type="primary")

        log_placeholder = st.empty()

        if run_button:
            if not query.strip():
                st.warning("Please enter a research topic before running.")
            else:
                st.session_state["last_query"] = query
                with st.spinner("Processing..."):
                    results, logs = run_workflow(query, selected_agent)
                    time.sleep(0.4)
                st.session_state["analysis_complete"] = True
                st.session_state["results"] = results
                st.session_state["logs"] = logs
                st.session_state["last_agent"] = selected_agent
                st.success("Execution complete. Open the Results tab to view outputs.")

        logs: List[str] = st.session_state.get("logs", [])
        if logs:
            log_placeholder.subheader("Execution Log")
            for entry in logs:
                log_placeholder.write(f"- {entry}")

    with results_tab:
        st.subheader("Results")
        if not st.session_state.get("analysis_complete"):
            st.info("Run a query in the Query tab to view results here.")
        else:
            last_agent = st.session_state.get("last_agent")
            results = st.session_state.get("results", {})
            if not last_agent:
                st.info("Run a query in the Query tab to view results here.")
            else:
                st.caption(f"Showing output for: {last_agent}")
                if last_agent in ("Marketing Orchestrator", "Offer Design"):
                    offers = results.get("offer_concepts", [])
                    if not offers:
                        st.warning("No offers generated. Run the workflow again.")
                    else:
                        for offer in offers:
                            render_offer_card(offer)
                elif last_agent == "Market Trends Analyst":
                    trend_briefs = results.get("trend_briefs", [])
                    if not trend_briefs:
                        st.warning("No trend briefs generated. Run the workflow again.")
                    else:
                        st.json(trend_briefs)
                elif last_agent == "Customer Insights Manager":
                    customer_insights = results.get("customer_insights", [])
                    if not customer_insights:
                        st.warning("No customer insights generated. Run the workflow again.")
                    else:
                        st.json(customer_insights)
                elif last_agent == "Event Planner":
                    event_calendar = results.get("event_calendar", {})
                    if not event_calendar:
                        st.warning("No event calendar generated. Run the workflow again.")
                    else:
                        st.json(event_calendar)
                else:
                    st.json(results)


if __name__ == "__main__":
    main()
