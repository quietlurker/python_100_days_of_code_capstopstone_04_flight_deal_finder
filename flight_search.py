import requests
import os


class FlightSearch:
    def __init__(self):
        self.tequila_endpoint = "https://api.tequila.kiwi.com"
        self.tequila_key = os.environ["TEQUILA_KEY"]
        self.tequila_header = {"apikey": self.tequila_key}
        self.tequila_city_search = {
            "term": "",
        }

    def get_iata_code(self, city_name):
        self.tequila_city_search = {
            "term": city_name,
        }

        city_iata_code = requests.get(url=f"{self.tequila_endpoint}/locations/query", params=self.tequila_city_search,
                                      headers=self.tequila_header)
        city_iata_code.raise_for_status()
        return city_iata_code.json()["locations"][0]["code"]

    def search_for_flight(self, dest, search_date_from, search_date_to, start_point):
        search_data = {
            "fly_from": start_point,
            "fly_to": dest,
            "one_for_city": 1,
            "date_from": search_date_from,
            "date_to ": search_date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "max_stopovers": 0,
            "flight_type": "round",
            "curr": "PLN",
        }
        response = requests.get(url=f"{self.tequila_endpoint}/search", params=search_data, headers=self.tequila_header)
        response.raise_for_status()
        return response.json()
