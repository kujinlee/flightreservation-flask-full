"""
Mock server for testing the Flight Reservation Flask Application.
"""

from flask import Flask, request, render_template

app = Flask(__name__)

# Configure the template folder
app.template_folder = "templates"

@app.route("/flightreservation-flask-full/findFlights", methods=["GET", "POST"])
def find_flights():
    """
    Mock endpoint for finding flights.
    """
    if request.method == "GET":
        # Render the flight search form
        return render_template("findFlights.html")
    # Mock response for flight search results
    return render_template(
        "findFlightsResults.html",
        flights=[
            {
                "flight_number": "AA101",
                "operating_airlines": "American Airlines",
                "departure_city": "AUS",
                "arrival_city": "NYC",
                "date_of_departure": "2024-02-05",
                "estimated_departure_time": "10:00 AM",
                "price": 200.00,
            },
            {
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
    app.run(debug=True, port=5002)
