# Wendy's AI Agents Hackathon

Multi-agent AI system prototype for generating data-driven promotional offers at Wendy's.
This repo includes a Google ADK-inspired agent mesh and a Streamlit UI to run and review
offer concepts.

## Getting Started

### Prerequisites
- Python 3.10+
- Google Cloud SDK (`gcloud`) installed and authenticated
- Git

### Install
```
pip install -r requirements.txt
```

### Run the UI
```
streamlit run ui/hackathon_agents_ui.py
```

## Project Structure

```
src/
  marketing_orchestrator/
  market_trends_analyst/
  customer_insights/
  event_planner/
  orchestrator/
  offer_design/
  utils/
docs/
ui/
```

## Notes
- This prototype includes safe fallback logic for running locally without external
  APIs. When Google ADK tools are available, the agents can call those tools
  directly.
- Outputs are structured for easy inspection in the UI.
