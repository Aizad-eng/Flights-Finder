import pandas as pd
import requests
import all_iata_codes

class FetchData:

    API_KEY = "TEQUILA API KEY"
    API_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"

    def __init__(self):
        self.city_names = []
        self.iata_codes = []
        self.iata_codes_price_dict = {}

        self.headers = {
            "apikey": FetchData.API_KEY
        }

    def fetch_city_names(self):
        self.city_names = self.df["city"].to_list()

    def get_city_from_user(self):
        city = input("Enter the name of cities you want to travel separated by commas i.e paris, tokyo: ")
        city_list = city.strip().split(",")
        for city in city_list:

            if len(city)== 0:
                pass
            else:
                self.city_names.append(city)

    def get_iata_codes(self):


        while True:

            self.get_city_from_user()
            valid_cities =[]
            for city in self.city_names:
                parameters = {
                    "term": f"{city}"
                }

                response = requests.get(url=FetchData.API_ENDPOINT, params=parameters, headers=self.headers)
                json_response = response.json()
                if len(json_response["locations"]) >= 1:
                    print("Fetching Iata Codes ...")
                    iata_code = json_response["locations"][0]["code"]
                    self.iata_codes.append(iata_code)

                    valid_cities.append(city)

            if len(valid_cities)==len(self.city_names):
                break
            else:
                invalid_cities = [city for city in self.city_names if city not in valid_cities]
                print(f"Please enter valid destination{'' if len(invalid_cities) == 1 else 's'}. {invalid_cities} {'is' if len(invalid_cities)==1 else 'are'} not recognized as valid destination{'' if len(invalid_cities) == 1 else 's'}.")


