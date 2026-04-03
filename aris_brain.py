import requests


def ask_ai(prompt):

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=300)

        # Check if request succeeded
        if response.status_code != 200:
            return f"AI server error: {response.status_code}"

        data = response.json()

        return data.get("response", "No response from model.")

    except requests.exceptions.ConnectionError:
        return "AI connection error: Ollama server not running."

    except requests.exceptions.Timeout:
        return "AI response timeout."

    except Exception as e:
        return f"AI error: {str(e)}"