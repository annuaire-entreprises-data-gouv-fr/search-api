from datetime import datetime

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


def convert_to_year_month(date_string):
    try:
        date_object = datetime.strptime(date_string, "%m/%d/%Y")
        formatted_date = date_object.strftime("%Y-%m")
        return formatted_date
    except ValueError:
        return "Invalid date format"
