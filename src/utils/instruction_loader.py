from __future__ import annotations

from pathlib import Path


def load_instruction(path: str | Path) -> str:
    """Load an instruction text file with safe defaults."""
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8").strip()
