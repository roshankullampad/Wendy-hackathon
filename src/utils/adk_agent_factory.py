from __future__ import annotations

from pathlib import Path
import secrets
from typing import Sequence

from google.adk.agents.llm_agent import LlmAgent
from google.genai import types

from src.utils.instruction_loader import load_instruction

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_TOP_K = 40


def build_llm_agent(
    *,
    name: str,
    description: str,
    instruction_path: Path,
    tools: Sequence[object] | None = None,
    model: str = DEFAULT_MODEL,
    response_mime_type: str | None = "application/json",
    temperature: float = DEFAULT_TEMPERATURE,
    top_p: float = DEFAULT_TOP_P,
    top_k: int = DEFAULT_TOP_K,
) -> LlmAgent:
    instruction = load_instruction(instruction_path)
    config_kwargs = {
        "temperature": temperature,
        "topP": top_p,
        "topK": top_k,
        "seed": secrets.randbelow(2**31),
    }
    if response_mime_type:
        config_kwargs["responseMimeType"] = response_mime_type
    generate_content_config = types.GenerateContentConfig(**config_kwargs)
    return LlmAgent(
        name=name,
        description=description,
        model=model,
        instruction=instruction,
        tools=list(tools) if tools else [],
        generate_content_config=generate_content_config,
    )
