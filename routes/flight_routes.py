from flask import Blueprint, jsonify, request, render_template, current_app
from sqlalchemy.orm import Session
from database import get_db
from models import Passenger, Reservation, Flight  # Correct table name is already applied in models.py
import logging
import random  # Import random module

flight_bp = Blueprint("flights", __name__)

@flight_bp.context_processor
def inject_base_url():
    return {"BASE_URL": current_app.config["BASE_URL"]}

@flight_bp.route("/flights", methods=["GET"])
def get_all_flights():
    with next(get_db()) as db:
        flights = db.query(Flight).all()
        return jsonify([{
            "id": f.id,
            "flight_number": f.flight_number,
            "operating_airlines": f.operating_airlines,
            "departure_city": f.departure_city,
            "arrival_city": f.arrival_city,
            "date_of_departure": f.date_of_departure,
            "estimated_departure_time": f.estimated_departure_time,
            "price": f.price
        } for f in flights])

@flight_bp.route("/flights/<int:flight_id>", methods=["GET"])
def get_flight_by_id(flight_id):
    with next(get_db()) as db:
        flight = db.query(Flight).filter(Flight.id == flight_id).first()
        if not flight:
            return jsonify({"error": "Flight not found"}), 404
        return jsonify({
            "id": flight.id,
            "flight_number": flight.flight_number,
            "operating_airlines": flight.operating_airlines,
            "departure_city": flight.departure_city,
            "arrival_city": flight.arrival_city,
            "date_of_departure": flight.date_of_departure,
            "estimated_departure_time": flight.estimated_departure_time,
            "price": flight.price
        })

@flight_bp.route("/findFlights", methods=["GET"])
def render_find_flights_page():
    return render_template("findFlights.html")

@flight_bp.route("/findFlights", methods=["POST"])
def find_flights():
    logging.info("MYLOG: Received findFlights request")  # Debug print to verify the function is called
    data = request.form
    departure = data.get("departure")
    arrival = data.get("arrival")
    date_of_departure = data.get("date_of_departure")
    with next(get_db()) as db:
        query = db.query(Flight)
        if departure:
            query = query.filter(Flight.departure_city.ilike(f"%{departure}%"))
        if arrival:
            query = query.filter(Flight.arrival_city.ilike(f"%{arrival}%"))
        if date_of_departure:
            query = query.filter(Flight.date_of_departure == date_of_departure)
        flights = query.all()
        return render_template("findFlightsResults.html", flights=flights)

@flight_bp.route("/reserve", methods=["GET"])
def render_reservation_page():
    logging.info("MYLOG: Received reserve request")  # Debug print to verify the function is called
    flight_id = request.args.get("flight_id")
    with next(get_db()) as db:
        flight = db.query(Flight).filter(Flight.id == flight_id).first()
        if not flight:
            return jsonify({"error": "Flight not found"}), 404
        return render_template("reserve.html", flight=flight)

@flight_bp.route("/createReservation", methods=["POST"])
def create_reservation():
    logging.info("MYLOG: Received createReservation request")  # Debug print to verify the function is called
    data = request.form
    with next(get_db()) as db:
        try:
            # Create a new passenger
            passenger = Passenger(
                first_name=data["first_name"],
                last_name=data["last_name"],
                middle_name=data.get("middle_name"),  # Optional field
                email=data["email"],
                phone=data["phone"]
            )
            db.add(passenger)
            db.commit()
            db.refresh(passenger)

            # Create a new reservation
            reservation = Reservation(
                flight_id=data["flight_id"],
                passenger_id=passenger.id,
                card_number=data["card_number"],
                amount=data["amount"]
            )
            db.add(reservation)
            db.commit()
            db.refresh(reservation)

            # Render confirmation page with "Confirm Reservation" button
            return render_template(
                "reservationConfirmation.html",
                reservation=reservation,
                flight=reservation.flight,
                passenger=reservation.passenger,
                show_confirm_button=True  # Enable the "Confirm Reservation" button
            )
        except Exception as e:
            db.rollback()  # Rollback in case of an error
            return jsonify({"error": f"Failed to create reservation: {e}"}), 500

def process_payment(card_number, amount):
    """
    Placeholder function for external payment processing.
    Simulates a 50% chance of payment success or failure.
    """
    log_message = f"MYLOG: Processing payment for card: {card_number}, amount: {amount}"
    logging.info(log_message)  # Log the message

    # Simulate payment success or failure with 50% chance
    payment_success = random.choice([True, False])
    logging.info(f"MYLOG: Payment success: {payment_success}")  # Log the result

    return payment_success, log_message  # Return the log message for debugging

@flight_bp.route("/completeReservation", methods=["POST"])
def complete_reservation():
    data = request.form
    logging.info("MYLOG: Received completeReservation request")  # Log the start of the function
    with next(get_db()) as db:
        try:
            # Fetch the reservation
            reservation = db.query(Reservation).filter(Reservation.id == data["reservation_id"]).first()
            if not reservation:
                logging.error("MYLOG: Reservation not found")  # Log error if reservation is not found
                return jsonify({"error": "Reservation not found"}), 404

            # Process payment
            payment_success, log_message = process_payment(reservation.card_number, reservation.amount)
            logging.info(f"MYLOG: Payment success is {payment_success}")  # Log payment success

            # Fetch flight details
            flight = db.query(Flight).filter(Flight.id == reservation.flight_id).first()
            if not flight:
                logging.error("MYLOG: Flight not found")  # Log error if flight is not found
                return jsonify({"error": "Flight not found"}), 404

            if payment_success:
                # Render the confirmation page with success message
                return render_template(
                    "reservationConfirmation.html",
                    reservation=reservation,
                    flight=flight,
                    passenger=reservation.passenger,
                    success=True,
                    log_message=log_message,
                    show_confirm_button=False  # Disable the "Confirm Reservation" button
                )
            else:
                # Redirect back to the reserve page with an error message
                return render_template(
                    "reserve.html",
                    flight=flight,
                    error_message="Payment failed. Please check your information and try again."
                )
        except Exception as e:
            logging.error(f"MYLOG: Error in complete_reservation: {e}")  # Log the exception
            return jsonify({"error": f"Failed to complete reservation: {e}"}), 500

@flight_bp.route("/checkIn", methods=["GET"])
def render_check_in_page():
    reservation_id = request.args.get("reservation_id")
    with next(get_db()) as db:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404
        return render_template("checkIn.html", reservation=reservation)

@flight_bp.route("/completeCheckIn", methods=["POST"])
def complete_check_in():
    data = request.form
    with next(get_db()) as db:
        reservation = db.query(Reservation).filter(Reservation.id == data["reservation_id"]).first()
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        reservation.number_of_bags = data["number_of_bags"]
        reservation.checked_in = True
        db.commit()

        return render_template("finalDetails.html", reservation=reservation)