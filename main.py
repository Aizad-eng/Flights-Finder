import smtplib

from email_sender import SendEmail
from fetch_data import FetchData
from flight_search import FlightSearch
from all_iata_codes import all_iata_codes
from  datetime import datetime, timedelta

is_email_valid = True

email_sender = SendEmail()
while True:
    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


    if not is_email_valid:
        email_sender = SendEmail()
    fetchdata = FetchData()
    fetchdata.get_iata_codes()
    flight_search = FlightSearch(fetchdata)

    while True:
        departure_city = input("Enter IATA CODE of the departure city: ").upper()
        if len(departure_city) == 3 and departure_city in all_iata_codes:
            break
        else:
            print(f"{departure_city} is not a valid Iata Code. Please enter valid Iata CODE. Find correct Iata code here: "
                  f"https://www.iata.org/en/publications/directories/code-search/?airport.search=")
    flight_search.search_flight(departure_city, tomorrow, six_month_from_today)
    try:
        if flight_search.flights_found():
            email_sender.send_email(email_sender.new_email)
            print("Please check your email for the flights data")

    except smtplib.SMTPRecipientsRefused:
        print(f"Your email doesnt look correct. Are you sure {email_sender.new_email} is a valid email? ")
        is_email_valid = False

    user_choice = input("Do you want to try another search (Y/N): ").upper()
    if user_choice in ("Y", "YES"):
        continue
    else:
        print("Bye, see you around. Thank you for using our service")
        break


