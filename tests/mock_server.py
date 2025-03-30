"""
Mock server for testing the Flight Reservation Flask Application.
"""

import os
import logging
from flask import Flask, request, render_template, jsonify

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

@app.route("/findFlights", methods=["GET"])
def find_flights():
    return jsonify([
        {"id": 1, "flight_number": "AA101", "departure_city": "AUS", "arrival_city": "NYC"},
        {"id": 2, "flight_number": "UA202", "departure_city": "AUS", "arrival_city": "NYC"},
    ])

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

@app.route('/api/payment', methods=['POST'])
def mock_payment():
    """
    Mock endpoint for simulating payment processing.
    """
    data = request.json
    if data.get('cardNumber') == '4111111111111111':
        return jsonify({"status": "success", "transactionId": "12345"}), 200
    else:
        return jsonify({"status": "failure", "error": "Invalid card number"}), 400

if __name__ == "__main__":
    logging.debug("Starting mock server...")
    app.run(debug=True, port=5002)