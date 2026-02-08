from __future__ import annotations

import json
import re
import uuid
from typing import Any, Dict, Iterable

from google.adk.agents.base_agent import BaseAgent
from google.adk.events import Event
from google.adk.runners import InMemoryRunner
from google.genai import types

USER_ID = "local-user"

_JSON_BLOCK_RE = re.compile(r"(\{.*\}|\[.*\])", re.DOTALL)


def build_user_content(message: str) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=message)])


def run_agent(agent: BaseAgent, query: str) -> list[Event]:
    runner = InMemoryRunner(agent=agent)
    session_id = str(uuid.uuid4())
    return list(
        runner.run(
            user_id=USER_ID,
            session_id=session_id,
            new_message=build_user_content(query),
        )
    )


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
