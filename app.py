from flask import Flask, jsonify, render_template  # Import render_template
from flask_cors import CORS  # Import CORS
from routes.flight_routes import flight_bp
from database import init_db
import logging
import os

# Initialize the Flask app
app = Flask(__name__)

# Set BASE_URL globally
app.config["BASE_URL"] = os.getenv("BASE_URL", "/flightreservation-flask-full")

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",  # Add timestamps and log levels
)

# Example log to verify logging is working
logging.info("Flask application is starting...")

# Enable CORS for the app
CORS(app)

# Register blueprints with BASE_URL
app.register_blueprint(flight_bp, url_prefix=app.config["BASE_URL"])

# Inject BASE_URL into all templates
@app.context_processor
def inject_base_url():
    return {"BASE_URL": app.config["BASE_URL"]}

@app.route("/")
def read_root():
    return render_template("index.html")  # No need to pass base_url explicitly

if __name__ == "__main__":
    init_db()  # Initialize the database
    port = int(os.getenv("FLASK_RUN_PORT", 5000))  # Use PORT from .env or default to 5000
    app.run(debug=True, host="0.0.0.0", port=port)  # Dynamically set the port
