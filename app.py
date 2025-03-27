"""
Main application entry point for the Flight Reservation Flask Application.
"""

import os
import logging
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from utils.swagger import get_swagger_json  # Update the import path for swagger
from routes.flight_routes import flight_bp
from database import init_db

# Load environment variables from .env and force overwrite
load_dotenv(override=True)

# Debugging: Print the value of FLASK_RUN_PORT
print("FLASK_RUN_PORT:", os.getenv("FLASK_RUN_PORT"))

# Initialize the Flask app
app = Flask(__name__)

# Set BASE_URL globally
app.config["BASE_URL"] = os.getenv("BASE_URL", "/flightreservation-flask-full")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger().setLevel(logging.INFO)

logging.info("Flask application is starting...")

# Enable CORS for the app
CORS(app)

# Register blueprints with BASE_URL
app.register_blueprint(flight_bp, url_prefix=app.config["BASE_URL"])

# Swagger configuration
SWAGGER_URL = f"{app.config['BASE_URL']}/api-docs"
API_URL = f"{app.config['BASE_URL']}/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.context_processor
def inject_base_url():
    """
    Inject the BASE_URL into all templates.
    """
    return {"BASE_URL": app.config["BASE_URL"]}

@app.route(f"{app.config['BASE_URL']}/swagger.json")
def swagger_json():
    """
    Serve the Swagger JSON specification.
    """
    return get_swagger_json(request, app.config["BASE_URL"])

@app.route("/")
def read_root():
    """
    Render the index page.
    """
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    logging.info("MYLOG: FLASK_RUN_PORT=%s", os.getenv("FLASK_RUN_PORT", "5000"))
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))  # Use PORT from .env or default to 5000

    # Enable HTTPS with SSL/TLS certificates
    cert_path = os.path.join(os.getcwd(), "certs", "cert.pem")
    key_path = os.path.join(os.getcwd(), "certs", "key.pem")
    app.run(debug=True, host="0.0.0.0", port=port, ssl_context=(cert_path, key_path))
