import requests
from typing import Optional

API_URL = "https://api.energidataservice.dk/dataset/Elspotprices"

def fetch_energy_prices(area="DK1", start: Optional[str] = None, end: Optional[str] = None):
    """Hent rådata fra API. start/end er 'YYYY-MM-DD' strings."""
    params = {
        "limit": 5000,
        "sort": "HourUTC asc",
        "filter": f'{{"PriceArea":["{area}"]}}'
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end

    resp = requests.get(API_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("records", [])
