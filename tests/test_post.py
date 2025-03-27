"""
Test script for the POST /findFlights endpoint in the Flight Reservation Flask Application.
"""

import requests  # Ensure the `requests` library is installed

URL = (
    "http://127.0.0.1:5002/flightreservation-flask-full/findFlights"
)  # Break long line
DATA = {
    "departure": "AUS",
    "arrival": "NYC",
    "date_of_departure": "02/05/2024"
}

def test_post_find_flights():
    """
    Test the POST /findFlights endpoint with sample data.
    """
    response = requests.post(URL, data=DATA, timeout=10)  # Add timeout
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
