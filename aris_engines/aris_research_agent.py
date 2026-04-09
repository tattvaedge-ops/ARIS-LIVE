from aris_tools.google_search import google_search

def research_query(query, ask_openai):

    results = google_search(query)

    print("🌐 GOOGLE RESULTS:", results)

    if not results:
        return "⚠️ No live data found."

    # 🔥 STEP 1: STRUCTURED DATA OUTPUT (FORCED)
    structured_output = "🧠 ARIS LIVE RESEARCH REPORT\n\n"

    for i, r in enumerate(results[:5], 1):
        title = r.get("title", "No Title")
        snippet = r.get("snippet", "No Description")
        link = r.get("link", "")

        structured_output += f"{i}. {title}\n"
        structured_output += f"   📌 {snippet}\n"
        structured_output += f"   🔗 {link}\n\n"

    # 🔥 STEP 2: CONTEXT FOR INTELLIGENCE
    context = ""

    for r in results:
        context += f"""
Title: {r.get('title')}
Summary: {r.get('snippet')}
"""

    prompt = f"""
You are ARIS Research Intelligence.

Analyze the LIVE DATA below and extract REAL INSIGHTS.

LIVE DATA:
{context}

User Query:
{query}

Instructions:
- Extract key trends
- Identify companies/events
- Mention important numbers if present
- Keep it concise and sharp
- NO generic explanation
"""

    # 🔥 STEP 3: INTELLIGENCE LAYER
    try:
        ai_output = ask_openai(prompt)
        return structured_output + "\n🔍 INSIGHTS:\n" + ai_output

    except Exception as e:
        print("⚠️ OpenAI failed:", e)
        return structured_output