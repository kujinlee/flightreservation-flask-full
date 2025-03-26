from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base

class Flight(Base):
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, nullable=False)
    # Removed the departure_time field
    operating_airlines = Column(String(20), nullable=False)
    departure_city = Column(String(20), nullable=False)
    arrival_city = Column(String(20), nullable=False)
    date_of_departure = Column(Date, nullable=False)
    estimated_departure_time = Column(DateTime, nullable=False)
    price = Column(Float(10, 2), nullable=False, default=0.0)

class Passenger(Base):
    __tablename__ = "passenger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    middle_name = Column(String(256), nullable=True)
    email = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=True)

class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    checked_in = Column(Boolean, nullable=False, default=False)
    number_of_bags = Column(Integer, nullable=True)
    passenger_id = Column(Integer, ForeignKey("passenger.id", ondelete="CASCADE"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flight.id"), nullable=False)
    created = Column(DateTime, nullable=False)
    card_number = Column(String(20), nullable=True)
    amount = Column(Float(10, 2), nullable=False, default=0.0)
    passenger = relationship("Passenger")
    flight = relationship("Flight")
