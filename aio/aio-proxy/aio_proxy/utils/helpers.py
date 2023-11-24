import requests


def fetch_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_content = response.json()
        return json_content
    except requests.RequestException as e:
        # Handle exceptions (e.g., network issues, invalid JSON, etc.)
        raise RuntimeError(f"Error fetching JSON from {url}: {str(e)}")
