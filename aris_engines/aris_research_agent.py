from aris_tools.google_search import google_search

def research_query(query, ask_openai):

    results = google_search(query)

    print("🌐 GOOGLE RESULTS:", results)

    if not results:
        return "⚠️ No live data found."

    context = ""

    for r in results:
        context += f"""
Title: {r['title']}
Summary: {r['snippet']}
Source: {r['link']}
"""

    prompt = f"""
You are ARIS Research Intelligence.

Use the LIVE INTERNET DATA below to answer the query.

LIVE DATA:
{context}

User Query:
{query}

Instructions:
- Give CURRENT real-world updates (2026)
- Extract key developments, not general theory
- Be specific (companies, events, numbers if possible)
- Structure answer cleanly
"""

    return ask_openai(prompt)