"""
Utility module for generating Swagger JSON specifications for the Flight Reservation Flask Application.
"""

from flask import jsonify

def get_swagger_json(request, base_url):
    """
    Generate and return the Swagger JSON specification.
    """
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "Flight Reservation API",
            "description": "API documentation for the Flight Reservation system",
            "version": "1.0.0"
        },
        "host": request.host,  # Dynamically set the host
        "basePath": base_url,  # Use the provided base URL
        "schemes": ["http"],
        "paths": {
            "/findFlights": {
                "get": {
                    "summary": "Render the flight search form",
                    "produces": ["text/html"],  # Specify the response content type
                    "description": (
                        "Opens the flight search form. "
                        f"[Click here to open]({request.host_url.strip('/')}"
                        f"{base_url}/findFlights)"
                    ),
                    "responses": {
                        "200": {
                            "description": "Flight search form rendered successfully"
                        }
                    }
                },
                "post": {
                    "summary": "Search for flights",
                    "parameters": [
                        {
                            "name": "departure",
                            "in": "formData",
                            "required": True,
                            "type": "string",
                            "description": "Departure city"
                        },
                        {
                            "name": "arrival",
                            "in": "formData",
                            "required": True,
                            "type": "string",
                            "description": "Arrival city"
                        },
                        {
                            "name": "date_of_departure",
                            "in": "formData",
                            "required": True,
                            "type": "string",
                            "format": "date",
                            "description": "Date of departure"
                        }
                    ],
                    "produces": ["text/html"],  # Specify the response content type
                    "description": (
                        "Submits a search for flights based on the provided criteria. "
                        "The response is an HTML page displaying the search results."
                    ),
                    "responses": {
                        "200": {
                            "description": "A list of flights matching the search criteria is displayed."
                        },
                        "400": {
                            "description": "Invalid input data."
                        }
                    }
                }
            },
            "/reserve": {
                "get": {
                    "summary": "Render the reservation page",
                    "produces": ["text/html"],  # Specify the response content type
                    "description": (
                        f"Opens the reservation page. "
                        f"[Click here to open]({request.host_url.strip('/')}"
                        f"{base_url}/reserve?flight_id=<flight_id>)"
                    ),
                    "parameters": [
                        {
                            "name": "flight_id",
                            "in": "query",
                            "required": True,
                            "type": "integer",
                            "description": "The ID of the flight to reserve"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Reservation page rendered successfully"
                        },
                        "404": {
                            "description": "Flight not found"
                        }
                    }
                }
            },
            "/createReservation": {
                "post": {
                    "summary": "Create a new reservation",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "flight_id": {"type": "integer"},
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "phone": {"type": "string"},
                                    "card_number": {"type": "string"},
                                    "amount": {"type": "number"}
                                },
                                "required": [
                                    "flight_id", "first_name", "last_name", "email",
                                    "phone", "card_number", "amount"
                                ]
                            },
                            "description": "The reservation details to be created."
                        }
                    ],
                    "produces": ["text/html"],  # Specify the response content type
                    "description": (
                        "Creates a new reservation and returns an HTML page with the "
                        "reservation confirmation."
                    ),
                    "responses": {
                        "201": {
                            "description": "Reservation created successfully. The confirmation page is displayed."
                        },
                        "400": {
                            "description": "Invalid input data."
                        },
                        "500": {
                            "description": "Failed to create reservation."
                        }
                    }
                }
            },
            "/checkIn": {
                "get": {
                    "summary": "Render the check-in page",
                    "produces": ["text/html"],  # Specify the response content type
                    "description": (
                        f"Opens the check-in page. "
                        f"[Click here to open]({request.host_url.strip('/')}"
                        f"{base_url}/checkIn?reservation_id=<reservation_id>)"
                    ),
                    "parameters": [
                        {
                            "name": "reservation_id",
                            "in": "query",
                            "required": True,
                            "type": "integer",
                            "description": "The ID of the reservation to check in"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Check-in page rendered successfully"
                        },
                        "404": {
                            "description": "Reservation not found"
                        }
                    }
                }
            },
            "/completeCheckIn": {
                "post": {
                    "summary": "Complete the check-in process",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "reservation_id": {"type": "integer"},
                                    "number_of_bags": {"type": "integer"}
                                },
                                "required": ["reservation_id", "number_of_bags"]
                            },
                            "description": (
                                "The check-in details to be completed."
                            )
                        }
                    ],
                    "produces": ["text/html"],  # Specify the response content type
                    "description": (
                        "Completes the check-in process and returns an HTML page with "
                        "the final reservation details."
                    ),
                    "responses": {
                        "200": {
                            "description": (
                                "Check-in completed successfully. The final reservation "
                                "details are displayed."
                            )
                        },
                        "404": {
                            "description": "Reservation not found."
                        }
                    }
                }
            }
        }
    })
