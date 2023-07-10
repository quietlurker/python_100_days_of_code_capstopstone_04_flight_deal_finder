import os
import requests


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destinations = {}
        self.sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
        self.sheety_token = os.environ["SHEETY_TOKEN"]
        self.sheety_headers = {"Authorization": f"Bearer {self.sheety_token}"}
        self.registered_users = {}

    def get_destination_data(self):
        destination_data = requests.get(url=f"{self.sheety_endpoint}/prices", headers=self.sheety_headers)
        destination_data.raise_for_status()
        self.destinations = destination_data.json()["prices"]
        return self.destinations

    def update_iata(self, count, iata, row_id):
        code_update = {"price": {"iataCode": iata}}
        self.destinations[count]["iataCode"] = iata
        print(self.destinations)
        update_code = requests.put(url=f"{self.sheety_endpoint}/prices/{row_id}", json=code_update,
                                   headers=self.sheety_headers)
        update_code.raise_for_status()

    def get_users(self):
        user_data = requests.get(url=f"{self.sheety_endpoint}/users", headers=self.sheety_headers)
        user_data.raise_for_status()
        self.registered_users = user_data.json()["users"]
        return self.registered_users

    def update_user_list(self, name, email):
        new_user = {
            "user": {
                "name": name,
                "email": email
            }
        }
        self.registered_users = ({"name": name, "email": email})
        update_users = requests.post(url=f"{self.sheety_endpoint}/users", json=new_user, headers=self.sheety_headers)
        update_users.raise_for_status()
