"""
Mock server for testing the Flight Reservation Flask Application.
"""

import os
import logging
from flask import Flask, request, render_template

# Ensure the working directory is set to the project root
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Initialize the Flask app
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))  # Set the correct template folder

# Add debug logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Template folder set to: %s", app.template_folder)
logging.debug("Absolute path to template folder: %s", os.path.abspath(app.template_folder))
logging.debug("Current working directory: %s", os.getcwd())
logging.debug("Template search path: %s", app.jinja_loader.searchpath)

@app.route("/flightreservation-flask-full/findFlights", methods=["GET", "POST"])
def find_flights():
    """
    Mock endpoint for finding flights.
    """
    logging.debug("Received request for /findFlights with method: %s", request.method)
    if request.method == "GET":
        # Render the flight search form
        return render_template("findFlights.html")
    # Mock response for flight search results
    return render_template(
        "findFlightsResults.html",
        flights=[
            {
                "id": 1,
                "flight_number": "AA101",
                "operating_airlines": "American Airlines",
                "departure_city": "AUS",
                "arrival_city": "NYC",
                "date_of_departure": "2024-02-05",
                "estimated_departure_time": "10:00 AM",
                "price": 200.00,
            },
            {
                "id": 2,
                "flight_number": "UA202",
                "operating_airlines": "United Airlines",
                "departure_city": "AUS",
                "arrival_city": "NYC",
                "date_of_departure": "2024-02-05",
                "estimated_departure_time": "12:00 PM",
                "price": 250.00,
            },
        ],
    )

@app.route("/flightreservation-flask-full/reserve", methods=["GET"])
def reserve():
    """
    Mock endpoint for reserving a flight.
    """
    return render_template(
        "reserve.html",
        flight={
            "flight_number": "AA101",
            "operating_airlines": "American Airlines",
            "departure_city": "AUS",
            "arrival_city": "NYC",
            "date_of_departure": "2024-02-05",
            "price": 200.00,
        },
    )

@app.route("/flightreservation-flask-full/createReservation", methods=["POST"])
def create_reservation():
    """
    Mock endpoint for creating a reservation.
    """
    if request.method != "POST":
        return "Method Not Allowed", 405  # Return 405 for unsupported methods
    return render_template(
        "reservationConfirmation.html",
        reservation={"id": 1, "card_number": "**** **** **** 1234", "amount": 200.00},
        flight={
            "flight_number": "AA101",
            "departure_city": "AUS",
            "arrival_city": "NYC",
            "date_of_departure": "2024-02-05",
            "estimated_departure_time": "10:00 AM",
        },
        passenger={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        show_confirm_button=True,
    )

@app.route("/flightreservation-flask-full/checkIn", methods=["GET"])
def check_in():
    """
    Mock endpoint for checking in.
    """
    return render_template(
        "checkIn.html",
        reservation={
            "id": 1,
            "flight": {"flight_number": "AA101"},
            "passenger": {"first_name": "John", "last_name": "Doe"},
        },
    )

@app.route("/flightreservation-flask-full/completeCheckIn", methods=["POST"])
def complete_check_in():
    """
    Mock endpoint for completing check-in.
    """
    if request.method != "POST":
        return "Method Not Allowed", 405  # Return 405 for unsupported methods
    return render_template(
        "finalDetails.html",
        reservation={
            "id": 1,
            "number_of_bags": 2,
            "checked_in": True,
            "amount": 200.00,
            "flight": {
                "flight_number": "AA101",
                "departure_city": "AUS",
                "arrival_city": "NYC",
                "date_of_departure": "2024-02-05",
                "estimated_departure_time": "10:00 AM",
            },
            "passenger": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
            },
        },
    )

if __name__ == "__main__":
    logging.debug("Starting mock server...")
    app.run(debug=True, port=5002)