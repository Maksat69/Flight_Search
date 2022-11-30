import os

import requests

SHEETY_END_POINT = os.getenv('SHEETY_END')


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.users_data = {}

    def get_destination_data(self):
        response = requests.get(url=f"{SHEETY_END_POINT}/cheaperPrise")
        data = response.json()
        self.destination_data = data["cheaperPrise"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_param = {
                "cheaperPrise": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_END_POINT}/{city['id']}", json=new_param)

            print(response.text)

    def get_users_data(self):
        response = requests.get(url=f"{SHEETY_END_POINT}/users")
        data = response.json()
        self.users_data = data["users"]
        return self.users_data
