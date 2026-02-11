import requests


class WorldExplorerClient:
    def __init__(self):
        # Using the free REST Countries API v3.1 - no API key needed
        self.base_url = "https://restcountries.com/v3.1"

    def _get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return None
            print(f"API Request Failed: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_all_countries(self):
        return self._get("all")

    def get_country_by_name(self, name):
        return self._get(f"name/{name}")

    def get_country_by_code(self, code):
        # 2 or 3 char code
        return self._get(f"alpha/{code}")

    def get_country_by_currency(self, currency_code):
        return self._get(f"currency/{currency_code}")

    def get_country_by_language(self, language_code):
        return self._get(f"lang/{language_code}")

    def get_country_by_capital(self, capital):
        return self._get(f"capital/{capital}")

    def get_country_by_region(self, region):
        return self._get(f"region/{region}")

    def get_country_by_subregion(self, subregion):
        return self._get(f"subregion/{subregion}")

    # Note: The REST Countries API doesn't have a dedicated city endpoint.
    # For city searches, we search by capital city name since that's available.
    def get_city_by_name(self, name):
        """
        Search for a city by looking up capitals.
        Returns countries whose capital matches the search term.
        """
        result = self.get_country_by_capital(name)
        if result:
            # Transform to city-like response format
            cities = []
            for country in result:
                capital_list = country.get('capital', [])
                for capital in capital_list:
                    if name.lower() in capital.lower():
                        cities.append({
                            'name': capital,
                            'country': country.get('name', {}).get('common', ''),
                            'country_code': country.get('cca2', ''),
                            'population': country.get('population', 0),
                            'region': country.get('region', ''),
                            'flag': country.get('flags', {}).get('svg', ''),
                        })
            return cities
        return []

    def get_cities_by_country(self, country_name):
        """Get the capital city of a country."""
        result = self.get_country_by_name(country_name)
        if result and len(result) > 0:
            country = result[0]
            capitals = country.get('capital', [])
            return [{'name': cap, 'country': country_name} for cap in capitals]
        return []
