import requests
from .config import API_BASE_URL

def fetch_api_data(endpoint: str, timeout: int = 10):
    """Fetch JSON data from API endpoint with error handling."""
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()
