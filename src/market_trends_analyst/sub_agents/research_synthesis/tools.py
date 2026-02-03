from __future__ import annotations

from typing import Dict

try:
    from google.adk.tools import web_scraper_tool as adk_web_scraper_tool
except Exception:  # pragma: no cover - optional dependency
    adk_web_scraper_tool = None


def web_scraper_tool(url: str) -> Dict[str, str]:
    """Fetch web content for a URL.

    Falls back to a lightweight placeholder payload for demos.
    """
    if adk_web_scraper_tool is not None:
        try:
            return adk_web_scraper_tool(url)
        except Exception:
            pass
    return {
        "url": url,
        "content": (
            "Sample content placeholder for trend analysis. "
            "Focuses on value offers, bundles, and app-exclusive deals."
        ),
    }
