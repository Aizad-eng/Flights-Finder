
import json

import pandas as pd
import requests
from datetime import datetime, timedelta


class FlightSearch:
    API_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
    API_KEY = "TEQUILA API KEY"

    def __init__(self, fetchdata):

        self.stop_overs = 0
        self.list_of_stopovers = []
        self.flight_data_df = pd.DataFrame()
        self.fetchdata = fetchdata

        self.headers = {
            "apikey": FlightSearch.API_KEY,
            "Content-Type": "application/json"

        }
    def search_flight(self, departure_city, from_time, to_time):
        for city in self.fetchdata.iata_codes:
            max_stopovers = 0
            print(f"Searching for direct flights from {departure_city} ---> {city}...")
            is_expensive = False
            good_flights_found = True
            while True:
                # try:
                parameters = {
                    "fly_from": departure_city,
                    "fly_to": city,
                    "date_from": from_time.strftime("%d/%m/%Y"),
                    "date_to": to_time.strftime("%d/%m/%Y"),
                    "nights_in_dst_from": 7,
                    "nights_in_dst_to": 30,
                    "flight_type": "round",
                    "max_stopovers": max_stopovers,
                    "curr": "USD"
                }

                response = requests.get(url=FlightSearch.API_ENDPOINT, params=parameters, headers=self.headers)
                data = response.json()

                city_flight_data = []
                if max_stopovers >2:
                    good_flights_found = False
                    break

                elif len(data["data"]) == 0 and max_stopovers <=2:
                    print(f"No direct flights were found. We also looked for flights with {max_stopovers} "
                          f"stopovers but found none. Now, we're searching for flights with {max_stopovers+1} stopovers.")
                    max_stopovers += 1

                else:
                    break

            with open("json_data.json", "w") as file:
                json.dump(data, file, indent=4)
            # try:

            min_price_of_flight = 100
            if good_flights_found:
                while True:
                    print(f"Searching for flights under {min_price_of_flight}")
                    for i in range(len(data["data"])):
                        flight_price = data["data"][i]["price"]
                        local_departure = data["data"][i]["local_departure"]
                        local_arrival = data["data"][i]["local_arrival"]
                        route = data["data"][i]["route"]
                        booking_link = data["data"][i]["deep_link"]

                        self.stop_overs = max_stopovers
                        self.list_of_stopovers.append(self.stop_overs)

                        if flight_price < min_price_of_flight:
                            stopover_locations = [stopover["cityTo"] for stopover in route if (
                                    (stopover["cityCodeTo"] != city) and (stopover["cityCodeTo"] != departure_city))]
                            flight_data = {
                                "from_from": departure_city,
                                "fly_to": city,
                                "local_departure": local_departure,
                                "local_arrival": local_arrival,
                                "price (USD)": flight_price,
                                "Stop_overs": len(stopover_locations),
                                "Stop_over_locations": f"{', '.join(stopover_locations) if len(stopover_locations) >= 1 else 'N/A'}",
                                "booking_link": booking_link,

                            }

                            city_flight_data.append(flight_data)

                    if len(city_flight_data) == 0:
                        print(
                            f"No flights found under {min_price_of_flight} now searching for flights under {min_price_of_flight + 50}")
                        min_price_of_flight += 50
                    else:
                        print(f"Flights found for {city} under {min_price_of_flight}$")
                        break

                if len(city_flight_data) >= 1:
                    city_df = pd.DataFrame(city_flight_data)
                    city_df['price (USD)'] = city_df['price (USD)'].astype(str)  # Convert to string


                    city_df['price (USD)'] = city_df['price (USD)'].str.strip()  # Remove leading and trailing whitespaces
                    city_df['price (USD)'] = city_df['price (USD)'].astype(int)  # Convert to float
                    city_df = city_df.sort_values(by='price (USD)', ascending=True)

                    self.flight_data_df = pd.concat([self.flight_data_df, city_df], ignore_index=True)
            else:
                print(f"No good flights found for {city}")
        if self.flights_found():
            self.flight_data_df.to_csv("Flights_data.csv", index=False)

    def flights_found(self):
        return not self.flight_data_df.empty
