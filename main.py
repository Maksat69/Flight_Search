import datetime as dt
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

today = dt.datetime.now() + dt.timedelta(days=1)
six_month_from_today = dt.datetime.now() + dt.timedelta(days=(6 * 30))
ORIGIN_CITY_CODE = "LON"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])

    data_manager.get_destination_data = sheet_data
    data_manager.update_destination_codes()

for destination in sheet_data:
    a = flight_search.check_flights(
        ORIGIN_CITY_CODE,
        destination["iataCode"],
        today,
        six_month_from_today
    )
    if a is None:
        continue
    if destination["lowestPrice"] > a.price:
        prices = f"Low price alert! Only {a.price} pounds"
        data_all = f"in {a.out_date} to {a.return_date}\n from {a.origin_city} in {a.origin_airport} airport \n" \
                   f"to {a.destination_city} in {a.destination_airport} airport "

        if a.stop_over > 0:
            data_all += f"\nFlight has {a.stop_over} stop over, via {a.via_city}."

        link = f"https://www.google.co.uk/flights?hl=en#flt={a.origin_airport}.{a.destination_airport}." \
               f"{a.out_date}*{a.destination_airport}.{a.origin_airport}.{a.return_date}"
        notification_manager.send_email(prices, data_all, link)
    else:
        print("NONE")





