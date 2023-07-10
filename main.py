from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

# INIT
START_FROM = "WAW"
today = datetime.now()
tomorrow = today + timedelta(days=1)
in_six_months = today + timedelta(days=30 * 6)
flight_search = FlightSearch()
data_manager = DataManager()

# get list of destinations and lowest prices from google sheet
destination_list = data_manager.get_destination_data()

# update iata codes
for count, entry in enumerate(destination_list, start=0):
    if entry["iataCode"] == "":
        iata_code = flight_search.get_iata_code(entry["city"])
        data_manager.update_iata(count, iata_code, entry["id"])

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

# get the list of signed-up users from google sheets
registered_users = data_manager.get_users()

# ask for user input data
user_name = input("State your name: ")

user_email = ""
user_email2 = "empty"
while user_email != user_email2:
    user_email = input("What is your email address: ")
    user_email2 = input("Repeat email address: ")

# check if user is in the user_list
user_exist = False
for email in registered_users:
    if email["email"] == user_email:
        user_exist = True

# if user is not in user list - add it
if not user_exist:
    data_manager.update_user_list(user_name, user_email)

# search for flight for all cities in destination_list
for city in destination_list:

    # get return flights from start city to destination from google sheet list
    search_data = flight_search.search_for_flight(city["iataCode"], today.strftime("%d/%m/%Y"),
                                                  in_six_months.strftime("%d/%m/%Y"), START_FROM)
    # print results if flight were found nad price is cheaper than in google sheet
    if search_data["_results"] != 0 and search_data["data"][0]["price"] <= city["lowestPrice"]:
        print(
            f"Cheap flight from {search_data['data'][0]['route'][0]['cityFrom']} "
            f"to {search_data['data'][0]['route'][0]['cityTo']} found.\nSending emails...")

        notifications = NotificationManager()
        # do this for all users in user list
        for user in registered_users:
            notifications.send_email(search_data, user["email"])
    else:
        print(f"No cheap flights found from {START_FROM} to {city['city']} ")
