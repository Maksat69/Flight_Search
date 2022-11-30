import os

import requests
from flight_data import FlightData

URL_END_POINT = "https://tequila-api.kiwi.com"
API_KEY = os.getenv('YOUR_API')


class FlightSearch:

    def get_destination_code(self, city_name):
        location_end_point = f"{URL_END_POINT}/locations/query"
        header = {"apikey": API_KEY}
        body_param = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_end_point, headers=header, params=body_param)
        data = response.json()["locations"]
        code = data[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        search_end_point = f"{URL_END_POINT}/v2/search"
        header = {"apikey": API_KEY}
        body_param = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(url=search_end_point, headers=header, params=body_param)

        try:
            data = response.json()["data"][0]
        except IndexError:
            body_param["max_stopovers"] = 1
            response = requests.get(url=search_end_point, headers=header, params=body_param)
            try:
                data = response.json()["data"][0]
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][0]["cityTo"],
                    destination_airport=data["route"][0]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0],
                    stop_over=1,
                    via_city=data["route"][0]["cityTo"]
                )

                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )

            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
