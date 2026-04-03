import requests

SERPER_API_KEY = "6dd70edfa46f93ae2e0d5cd3c27c2c14c2648d4b"


def google_search(query):

    try:

        query = query.replace("search", "").strip()

        url = "https://google.serper.dev/search"

        payload = {
            "q": query
        }

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        results = []

        if "organic" not in data:
            return "No search results found."

        for item in data["organic"][:5]:

            title = item["title"]
            snippet = item.get("snippet", "")
            link = item["link"].split("?")[0]

            results.append(
                f"<b>🔎 {title}</b><br>"
                f"{snippet}<br>"
                f"<a href='{link}' target='_blank'>🌐 Open Source</a><br><br>"
            )

        return "".join(results)

    except Exception as e:
        return f"Search error: {e}"