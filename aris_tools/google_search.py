import requests
import os
from dotenv import load_dotenv

load_dotenv()   # 🔥 THIS LINE IS MISSING

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

print("DEBUG API KEY:", GOOGLE_API_KEY)
print("DEBUG CX:", GOOGLE_CX)

def google_search(query):

    try:
        print("🔍 QUERY:", query)

        # ✅ Check env variables
        if not GOOGLE_API_KEY or not GOOGLE_CX:
            print("❌ MISSING API KEY OR CX")
            return []

        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "q": query
        }

        response = requests.get(url, params=params)

        print("📡 STATUS:", response.status_code)

        # ✅ Handle bad responses
        if response.status_code != 200:
            print("❌ API ERROR:", response.text)
            return []

        data = response.json()

        results = []

        # ✅ Extract results safely
        items = data.get("items", [])

        for item in items:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", "")
            })

        print("🌐 RESULTS COUNT:", len(results))

        return results

    except Exception as e:
        print("🔥 GOOGLE SEARCH ERROR:", str(e))
        return []