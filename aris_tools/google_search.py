import requests
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def google_search(query):

    try:
        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "num": 5
        }

        response = requests.get(url, params=params)
        data = response.json()

        results = []

        if "items" in data:
            for item in data["items"]:
                results.append({
                    "title": item.get("title"),
                    "snippet": item.get("snippet"),
                    "link": item.get("link")
                })

        return results

    except Exception as e:
        print("GOOGLE SEARCH ERROR:", str(e))
        return []