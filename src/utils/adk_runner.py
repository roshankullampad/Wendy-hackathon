from __future__ import annotations

import asyncio
import json
from pathlib import Path
import re
import threading
import uuid
from typing import Any, Dict, Iterable

from dotenv import load_dotenv
from google.adk.agents.base_agent import BaseAgent
from google.adk.events import Event
from google.adk.runners import InMemoryRunner
from google.genai import types

USER_ID = "local-user"

_JSON_BLOCK_RE = re.compile(r"(\{.*\}|\[.*\])", re.DOTALL)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Ensure local `.env` settings are available for direct Python/Streamlit runs.
load_dotenv(PROJECT_ROOT / ".env", override=False)


def build_user_content(message: str) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=message)])


def run_agent(agent: BaseAgent, query: str) -> list[Event]:
    try:
        return _run_agent_in_thread(agent, query)
    except Exception as error:
        raise _normalize_runner_error(error) from error


async def _run_agent_async(agent: BaseAgent, query: str) -> list[Event]:
    runner = InMemoryRunner(agent=agent)
    session_id = str(uuid.uuid4())
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=USER_ID,
        session_id=session_id,
        state={},
    )

    events: list[Event] = []
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=build_user_content(query),
    ):
        events.append(event)

    if not events:
        raise RuntimeError(
            "Agent execution produced no events. Verify LLM credentials/configuration."
        )
    return events


def _run_agent_in_thread(agent: BaseAgent, query: str) -> list[Event]:
    events: list[Event] = []
    run_error: Exception | None = None

    def _target() -> None:
        nonlocal events, run_error
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            events = loop.run_until_complete(_run_agent_async(agent, query))
        except Exception as error:
            run_error = error
        finally:
            pending_tasks = [task for task in asyncio.all_tasks(loop) if not task.done()]
            if pending_tasks:
                loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
            asyncio.set_event_loop(None)
            loop.close()

    thread = threading.Thread(target=_target, daemon=True)
    thread.start()
    thread.join()

    if run_error is not None:
        raise run_error
    return events


def _normalize_runner_error(error: Exception) -> RuntimeError:
    if isinstance(error, RuntimeError) and str(error).startswith("Agent execution produced no events"):
        return error

    message = str(error)
    if "Missing key inputs argument" in message:
        return RuntimeError(
            "LLM credentials are missing. Set GOOGLE_API_KEY or configure Vertex AI "
            "(GOOGLE_GENAI_USE_VERTEXAI=true, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION)."
        )
    if "API key not valid" in message or "PERMISSION_DENIED" in message:
        return RuntimeError(
            "LLM request was rejected. Verify GOOGLE_API_KEY/Vertex credentials and model access."
        )
    return RuntimeError(f"Agent execution failed: {message}")


def extract_final_responses(events: Iterable[Event]) -> Dict[str, str]:
    outputs: Dict[str, str] = {}
    for event in events:
        if event.author == "user":
            continue
        if not event.is_final_response():
            continue
        text = _event_text(event)
        if text:
            outputs[event.author] = text
    return outputs


def parse_json_payload(text: str) -> Any:
    if not text:
        return None
    cleaned = _strip_code_fences(text).strip()
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = _JSON_BLOCK_RE.search(cleaned)
        if match:
            snippet = match.group(0)
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                return None
    return None


def coerce_list(payload: Any, key: str | None = None) -> list:
    if isinstance(payload, dict) and key:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    if isinstance(payload, list):
        return payload
    return []


def coerce_dict(payload: Any) -> dict:
    if isinstance(payload, dict):
        return payload
    return {}


def _event_text(event: Event) -> str:
    if not event.content or not event.content.parts:
        return ""
    text_parts = [
        part.text for part in event.content.parts if part.text and not part.thought
    ]
    return "\n".join(text_parts).strip()


def _strip_code_fences(text: str) -> str:
    if "```" not in text:
        return text
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)
