from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

START_FROM = "WAW"

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes
# to achieve the program requirements.

# Use the Flight Search and Sheety API to populate your own copy of the Google Sheet
# with International Air Transport Association (IATA) codes for each city.
# Most of the cities in the sheet include multiple airports, you want the city code (not the airport code see here).
flight_search = FlightSearch()

destination_data = DataManager()

destination_list = destination_data.get_destination_data()

# update iata codes
for entry in range(len(destination_list)):
    if destination_list[entry]["iataCode"] == "":
        iata_code = flight_search.get_iata_code(destination_list[entry]["city"])
        destination_data.update_iata(entry, iata_code, destination_list[entry]["id"])

# print(destination_list)
# this is to stop sheety searches as we have limited requests per month and I already used 79
# destination_list = [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 270, 'id': 2},
#                     {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 210, 'id': 3},
#                     {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 2400, 'id': 4},
#                     {'city': 'Sydney', 'iataCode': 'SYD', 'lowestPrice': 2700, 'id': 5},
#                     {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 475, 'id': 6},
#                     {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 2070, 'id': 7},
#                     {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 1200, 'id': 8},
#                     {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 1300, 'id': 9},
#                     {'city': 'Cape Town', 'iataCode': 'CPT', 'lowestPrice': 1900, 'id': 10},
#                     {'city': 'London', 'iataCode': 'LON', 'lowestPrice': 50, 'id': 11},
#                     {'city': 'Kopenhagen', 'iataCode': 'CPH', 'lowestPrice': 50, 'id': 12},
#                     {'city': 'Singapore', 'iataCode': 'SIN', 'lowestPrice': 100, 'id': 13}]

today = datetime.now()
tomorrow = today + timedelta(days=1)
in_six_months = today + timedelta(days=30 * 6)

# search for flight for all cities in destination_list
for city in destination_list:

    # get return flights from start city to destination from google sheet list
    search_data = flight_search.search_for_flight(city["iataCode"], today.strftime("%d/%m/%Y"),
                                                  in_six_months.strftime("%d/%m/%Y"), START_FROM)

    # print results if flight were found nad price is cheaper than in google sheet
    if search_data["_results"] != 0 and search_data["data"][0]["price"] <= city["lowestPrice"]:
        print(
            f"Cheap flight from {search_data['data'][0]['route'][0]['cityFrom']} "
            f"to {search_data['data'][0]['route'][0]['cityTo']} found.\nSending email...")

        notifications = NotificationManager()
        notifications.send_email(search_data)
    else:
        print(f"No cheap flights found from {START_FROM} to {city['city']} ")
