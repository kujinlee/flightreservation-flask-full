"""
Unit tests for the routes in the Flight Reservation Flask Application.
"""

def test_get_all_flights(client):
    """
    Test the GET /flights endpoint.
    """
    response = client.get("/flightreservation-flask-full/flights")
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Ensure the response is a list

def test_find_flights(client):
    """
    Test the POST /findFlights endpoint.
    """
    data = {
        "departure": "AUS",
        "arrival": "NYC",
        "date_of_departure": "2024-02-05"
    }
    response = client.post("/flightreservation-flask-full/findFlights", data=data)
    assert response.status_code == 200
    assert "flights" in response.data.decode()  # Ensure the response contains flight data

def test_reserve_flight(client):
    """
    Test the GET /reserve endpoint.
    """
    response = client.get("/flightreservation-flask-full/reserve?flight_id=1")
    assert response.status_code == 200
    assert "Reserve" in response.data.decode()  # Ensure the response contains reservation form

def test_create_reservation(client):
    """
    Test the POST /createReservation endpoint.
    """
    data = {
        "flight_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "card_number": "4111111111111111",
        "amount": 200.00
    }
    response = client.post("/flightreservation-flask-full/createReservation", data=data)
    assert response.status_code == 200
    assert "Reservation Confirmation" in response.data.decode()

def test_check_in(client):
    """
    Test the GET /checkIn endpoint.
    """
    response = client.get("/flightreservation-flask-full/checkIn?reservation_id=1")
    assert response.status_code == 200
    assert "Check-In" in response.data.decode()

def test_complete_check_in(client):
    """
    Test the POST /completeCheckIn endpoint.
    """
    data = {
        "reservation_id": 1,
        "number_of_bags": 2
    }
    response = client.post("/flightreservation-flask-full/completeCheckIn", data=data)
    assert response.status_code == 200
    assert "Final Details" in response.data.decode()
