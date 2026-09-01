"""
tools/web.py — Web search for Friday
Uses DuckDuckGo Instant Answer API (free, no API key required).
Falls back to listing related topics if no direct answer found.
"""

import requests

DDG_URL = "https://api.duckduckgo.com/"


def search_web(query: str) -> str:
    """Search the web using DuckDuckGo and return a concise answer."""
    try:
        params = {
            "q":              query,
            "format":         "json",
            "no_html":        1,
            "skip_disambig":  1,
        }
        r = requests.get(DDG_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        # 1. Try direct abstract (best answer)
        abstract = data.get("AbstractText", "").strip()
        if abstract:
            source = data.get("AbstractURL", "")
            return f"🔍 {abstract}\n🔗 {source}"

        # 2. Try answer (e.g. "what is 2+2")
        answer = data.get("Answer", "").strip()
        if answer:
            return f"🔍 {answer}"

        # 3. Try definition
        definition = data.get("Definition", "").strip()
        if definition:
            return f"📖 {definition}\n🔗 {data.get('DefinitionURL', '')}"

        # 4. Try related topics
        topics  = data.get("RelatedTopics", [])
        results = []
        for t in topics[:4]:
            if isinstance(t, dict) and "Text" in t:
                results.append(f"  • {t['Text']}")

        if results:
            return f"🔍 Results for '{query}':\n" + "\n".join(results)

        return f"🔍 No quick answer found for '{query}'. Try being more specific."

    except requests.exceptions.ConnectionError:
        return "❌ No internet connection for web search."
    except Exception as e:
        return f"❌ Web search failed: {e}"
