"""
Routes for handling flight-related operations in the Flight Reservation Flask Application.
"""

import logging
import random  # Import standard libraries first
from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, current_app
from sqlalchemy.exc import SQLAlchemyError  # Import third-party modules first
from database.database import get_db  # Import first-party modules
from models.models import Passenger, Reservation, Flight  # Fix import path

flight_bp = Blueprint("flights", __name__)

@flight_bp.context_processor
def inject_base_url():
    """
    Inject the BASE_URL into all templates.
    """
    return {"BASE_URL": current_app.config["BASE_URL"]}

@flight_bp.route("/flights", methods=["GET"])
def get_all_flights():
    """
    Retrieve all flights from the database.
    """
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
    """
    Retrieve a specific flight by its ID.
    """
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
    """
    Render the flight search form.
    """
    return render_template("findFlights.html")

@flight_bp.route("/findFlights", methods=["POST"])
def find_flights():
    """
    Search for flights based on user-provided criteria.
    """
    logging.info("MYLOG: Received findFlights request")
    data = request.form
    departure = data.get("departure")
    arrival = data.get("arrival")
    date_of_departure = data.get("date_of_departure")

    # Reformat date_of_departure to YYYY-MM-DD
    if date_of_departure:
        try:
            date_of_departure = datetime.strptime(
                date_of_departure, "%m/%d/%Y"
            ).strftime("%Y-%m-%d")
        except ValueError:
            try:
                date_of_departure = datetime.strptime(
                    date_of_departure, "%Y-%m-%d"
                ).strftime("%Y-%m-%d")
            except ValueError:
                logging.error("MYLOG: Invalid date format for date_of_departure")
                return jsonify(
                    {"error": "Invalid date format. Use MM/DD/YYYY or YYYY-MM-DD."}
                ), 400

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
    """
    Render the reservation page for a specific flight.
    """
    logging.info("MYLOG: Received reserve request")
    flight_id = request.args.get("flight_id")
    with next(get_db()) as db:
        flight = db.query(Flight).filter(Flight.id == flight_id).first()
        if not flight:
            return jsonify({"error": "Flight not found"}), 404
        return render_template("reserve.html", flight=flight)

@flight_bp.route("/createReservation", methods=["POST"])
def create_reservation():
    """
    Create a new reservation for a flight.
    """
    logging.info("MYLOG: Received createReservation request")
    data = request.form
    with next(get_db()) as db:
        try:
            passenger = Passenger(
                first_name=data["first_name"],
                last_name=data["last_name"],
                middle_name=data.get("middle_name"),
                email=data["email"],
                phone=data["phone"]
            )
            db.add(passenger)
            db.commit()
            db.refresh(passenger)

            reservation = Reservation(
                flight_id=data["flight_id"],
                passenger_id=passenger.id,
                card_number=data["card_number"],
                amount=data["amount"]
            )
            db.add(reservation)
            db.commit()
            db.refresh(reservation)

            return render_template(
                "reservationConfirmation.html",
                reservation=reservation,
                flight=reservation.flight,
                passenger=reservation.passenger,
                show_confirm_button=True
            )
        except SQLAlchemyError as exc:  # Catch specific SQLAlchemy exceptions
            db.rollback()
            logging.error("MYLOG: Error creating reservation: %s", exc)
            return jsonify({"error": f"Failed to create reservation: {exc}"}), 500

def process_payment(card_number, amount):
    """
    Placeholder function for external payment processing.
    Simulates a 50% chance of payment success or failure.
    """
    logging.info("MYLOG: Processing payment for card: %s, amount: %s", card_number, amount)
    payment_success = random.choice([True, False])
    logging.info("MYLOG: Payment success: %s", payment_success)
    return payment_success

@flight_bp.route("/completeReservation", methods=["POST"])
def complete_reservation():
    """
    Complete a reservation by processing payment.
    """
    data = request.form
    logging.info("MYLOG: Received completeReservation request")
    with next(get_db()) as db:
        try:
            reservation = db.query(Reservation).filter(
                Reservation.id == data["reservation_id"]
            ).first()
            if not reservation:
                logging.error("MYLOG: Reservation not found")
                return jsonify({"error": "Reservation not found"}), 404

            payment_success = process_payment(
                reservation.card_number, reservation.amount
            )
            logging.info("MYLOG: Payment success is %s", payment_success)

            flight = db.query(Flight).filter(
                Flight.id == reservation.flight_id
            ).first()
            if not flight:
                logging.error("MYLOG: Flight not found")
                return jsonify({"error": "Flight not found"}), 404

            if payment_success:
                return render_template(
                    "reservationConfirmation.html",
                    reservation=reservation,
                    flight=flight,
                    passenger=reservation.passenger,
                    success=True,
                    show_confirm_button=False,
                )
            return render_template(
                "reserve.html",
                flight=flight,
                error_message="Payment failed. Please check your information and try again.",
            )
        except SQLAlchemyError as exc:  # Replace broad exception with SQLAlchemyError
            logging.error("MYLOG: Error in complete_reservation: %s", exc)
            return jsonify({"error": f"Failed to complete reservation: {exc}"}), 500

@flight_bp.route("/checkIn", methods=["GET"])
def render_check_in_page():
    """
    Render the check-in page for a reservation.
    """
    reservation_id = request.args.get("reservation_id")
    with next(get_db()) as db:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404
        return render_template("checkIn.html", reservation=reservation)

@flight_bp.route("/completeCheckIn", methods=["POST"])
def complete_check_in():
    """
    Complete the check-in process for a reservation.
    """
    data = request.form
    with next(get_db()) as db:
        reservation = db.query(Reservation).filter(Reservation.id == data["reservation_id"]).first()
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404

        reservation.number_of_bags = data["number_of_bags"]
        reservation.checked_in = True
        db.commit()

        return render_template("finalDetails.html", reservation=reservation)
