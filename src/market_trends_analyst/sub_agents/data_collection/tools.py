from __future__ import annotations

import random
from typing import Dict, List

try:
    from google.adk.tools import google_search as adk_google_search
except Exception:  # pragma: no cover - optional dependency
    adk_google_search = None


SAMPLE_SOURCES = [
    {"url": "https://www.qsrmagazine.com/menu/", "source_type": "news"},
    {"url": "https://www.restaurantbusinessonline.com/marketing", "source_type": "news"},
    {"url": "https://www.nrn.com/quick-service", "source_type": "news"},
    {"url": "https://www.prnewswire.com/news-releases/", "source_type": "news"},
    {"url": "https://www.fastcompany.com/food", "source_type": "blog"},
    {"url": "https://www.qsrmagazine.com/news/", "source_type": "blog"},
    {"url": "https://www.reddit.com/r/fastfood/", "source_type": "social_media"},
    {"url": "https://www.reddit.com/r/fastfooddeals/", "source_type": "social_media"},
    {"url": "https://www.reddit.com/r/frugal/", "source_type": "forum"},
    {"url": "https://www.reddit.com/r/food/", "source_type": "social_media"},
    {"url": "https://www.webretail.com/", "source_type": "blog"},
    {"url": "https://www.qsrmagazine.com/consumer-trends/", "source_type": "news"},
    {"url": "https://www.reddit.com/r/marketing/", "source_type": "forum"},
    {"url": "https://www.restaurantbusinessonline.com/consumer-trends", "source_type": "news"},
    {"url": "https://www.qsrweb.com/blogs/", "source_type": "blog"},
]


def _fallback_results(query: str, limit: int) -> List[Dict[str, str]]:
    if not SAMPLE_SOURCES:
        return []
    sources = list(SAMPLE_SOURCES)
    random.shuffle(sources)
    return sources[:limit]


def google_search(query: str, limit: int = 12) -> List[Dict[str, str]]:
    """Return a list of URLs and source types.

    If Google ADK tools are available, attempt to use them. Otherwise, fall back
    to a curated sample list for demo purposes.
    """
    if adk_google_search is not None:
        try:
            results = adk_google_search(query)
            normalized: List[Dict[str, str]] = []
            for item in results or []:
                url = item.get("url") or item.get("link")
                if not url:
                    continue
                normalized.append({"url": url, "source_type": item.get("source_type", "news")})
            if normalized:
                return normalized[:limit]
        except Exception:
            pass
    return _fallback_results(query, limit)
