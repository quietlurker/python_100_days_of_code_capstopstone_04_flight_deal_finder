import os
import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destinations = {}
        self.sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
        self.sheety_token = os.environ["SHEETY_TOKEN"]
        self.sheety_headers = {"Authorization": f"Bearer {self.sheety_token}"}

    def get_destination_data(self):
        destination_data = requests.get(url=self.sheety_endpoint, headers=self.sheety_headers)
        destination_data.raise_for_status()
        self.destinations = destination_data.json()["prices"]
        return self.destinations

    def update_iata(self, city, iata, row_id):
        code_update = {"price": {"iataCode": iata}}
        self.destinations[city]["iataCode"] = iata
        update_code = requests.put(url=f"{self.sheety_endpoint}/{row_id}", json=code_update,
                                   headers=self.sheety_headers)
        update_code.raise_for_status()
