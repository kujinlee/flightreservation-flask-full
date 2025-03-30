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

def test_find_flights(client, mocker):
    # Mock the database query
    mock_flights = [
        {"id": 1, "flight_number": "AA101", "departure_city": "AUS", "arrival_city": "NYC"},
        {"id": 2, "flight_number": "UA202", "departure_city": "AUS", "arrival_city": "NYC"},
    ]
    mocker.patch('app.models.Flight.query.all', return_value=mock_flights)

    # Test the /findFlights route
    response = client.get('/findFlights')
    assert response.status_code == 200
    assert "AA101" in response.data.decode()

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
