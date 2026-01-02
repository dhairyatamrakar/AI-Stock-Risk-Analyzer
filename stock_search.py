import requests

def search_stocks(query):
    if not query or len(query) < 2:
        return []

    url = "https://query1.finance.yahoo.com/v1/finance/search"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    params = {
        "q": query,
        "quotesCount": 8,
        "newsCount": 0
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)

        # If Yahoo blocks or returns empty response
        if response.status_code != 200 or not response.text:
            return []

        data = response.json()

        results = []
        for item in data.get("quotes", []):
            symbol = item.get("symbol")
            name = item.get("shortname") or item.get("longname")
            if symbol and name:
                results.append(f"{symbol} — {name}")

        return results

    except (requests.exceptions.RequestException, ValueError):
        # Network error or JSON decode error
        return []
