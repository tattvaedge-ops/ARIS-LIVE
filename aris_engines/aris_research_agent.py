from aris_tools.google_search import google_search

def research_query(query, ask_openai):

    results = google_search(query)

    if not results:
        return "⚠️ Unable to fetch live data."

    context = ""

    for r in results:
        context += f"""
Title: {r['title']}
Summary: {r['snippet']}
Source: {r['link']}

"""

    prompt = f"""
You are ARIS Research Intelligence.

Use the LIVE DATA below to answer.

LIVE DATA:
{context}

User Query:
{query}

Instructions:
- Give updated (2026) insights
- Do NOT mention sources explicitly
- Structure answer clearly
"""

    return ask_openai(prompt)