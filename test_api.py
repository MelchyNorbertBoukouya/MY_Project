import requests
import os

API_KEY = "egSxhqEIHnpnefnDQf4Y5KkjY5eRIFS7"
HEADERS = {"apikey": API_KEY}

URLS = [
    "https://api.apilayer.com/rest_countries/v2/name/France",
    "https://api.apilayer.com/geo/country/name/France",
    "https://api.apilayer.com/country_data/country/name/France",
    "https://api.apilayer.com/world_geo_data/country/name/France",
]

for url in URLS:
    try:
        print(f"Testing {url}...")
        response = requests.get(url, headers=HEADERS)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.text[:200])
            break
        else:
            print("Response:", response.text[:100])
    except Exception as e:
        print(f"Error: {e}")
