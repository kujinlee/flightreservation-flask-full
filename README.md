# Flight Reservation Flask Application

This is a Flask implementation of the Flight Reservation System. It allows users to search for flights, complete reservations, and check-in for flights.

---

## Prerequisites

- [Python](https://www.python.org/) (v3.8 or higher recommended)
- [MySQL](https://www.mysql.com/) (for database setup)
- [OpenSSL](https://www.openssl.org/) (for generating SSL/TLS certificates)
- [pip](https://pip.pypa.io/en/stable/) (Python package manager)

---

## Setup

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/kujinlee/flightreservation-flask-full.git
    cd flightreservation-flask-full
    ```

2. **Create a Virtual Environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and configure the following variables:
    ```plaintext
    BASE_URL=/flightreservation-flask-full
    DATABASE_URL=mysql+pymysql://<your user name>:<your password>@localhost:3306/<your database name>
    FLASK_RUN_PORT=5001
    ```

    Replace `<your user name>`, `<your password>`, and `<your database name>` with your MySQL credentials and database name.

    - **BASE_URL**: The base URL path for the application (e.g., `/flightreservation-flask-full`). Ensure this matches the prefix used in your routes and templates.

5. **Set Up the Database**:
    - Create a MySQL database with the name specified in the `DATABASE_URL`.
    - Execute the SQL scripts to set up the schema and seed data:
      ```sh
      mysql -u <your user name> -p<your password> <your database name> < sql-scripts/1-schema.sql
      mysql -u <your user name> -p<your password> <your database name> < sql-scripts/2-seed.sql
      ```

6. **Generate SSL/TLS Certificates for Development**:
    If `USE_HTTPS=true` is set in the `.env` file, you need to generate self-signed SSL/TLS certificates for development:

    ```sh
    mkdir certs
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout certs/key.pem \
        -out certs/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
    ```

    - This will create two files in the `certs/` directory:
        - `key.pem`: The private key.
        - `cert.pem`: The self-signed certificate.
    - Ensure the `certs/` directory is excluded from the repository (already handled in `.gitignore`).

7. **Start the Application**:
    Activate the virtual environment and run the Flask application:
    ```sh
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    flask run
    ```

8. **Access the Application**:
    Open your browser and navigate to:
    [http://localhost:5001/flightreservation-flask-full/findFlights](http://localhost:5001/flightreservation-flask-full/findFlights)

    - This will take you to the first page of the application.
    - Ensure that the `BASE_URL` in your `.env` file is set to `/flightreservation-flask-full` for the application to work correctly.

---

## Directory Descriptions

### **`certs/`**
- This directory is used to store SSL/TLS certificates for enabling HTTPS.
- **Important**: Certificates should not be pushed to the repository. They are excluded by the `.gitignore` file.
- If HTTPS is enabled (`USE_HTTPS=true` in `.env`), ensure that valid certificates (`cert.pem` and `key.pem`) are placed in this directory.

---

## Notes

- Ensure that the `.env` file is **not pushed to the repository**. It is already excluded by the `.gitignore` file.
- Use a secure password for your database and avoid hardcoding it in the codebase.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## User Interaction Flow

1. **Search for Flights**:
   - **Route**: `GET {BASE_URL}/findFlights`
   - **Description**: Renders the `findFlights` view (flight search form).
   - **Next Step**: User submits the form to search for flights.

2. **View Flight Search Results**:
   - **Route**: `POST {BASE_URL}/findFlights`
   - **Description**: Executes the `findFlights` function to query the database for flights matching the search criteria. Renders the `findFlightsResults` view with the search results.
   - **Next Step**: User selects a flight and clicks the "Reserve" button.

3. **Reserve a Flight**:
   - **Route**: `GET {BASE_URL}/reserve`
   - **Description**: Executes the `renderReservationPage` function to render the `reserve` view with the selected flight details. The view contains a form to collect passenger data.
   - **Next Step**: User submits the form to reserve the flight.

4. **Create a Reservation**:
   - **Route**: `POST {BASE_URL}/createReservation`
   - **Description**: Executes the `createReservation` function to:
     - Create a passenger object and save it in the database.
     - Create a reservation object with the passenger ID and save it in the database.
     - Render the `reservationConfirmation` view with reservation, flight, and passenger details.
   - **Next Step**: User can either:
     - Click the "Continue to Check-In" link to proceed to check-in.
     - Click the "Confirm Reservation" button to complete the reservation.

5. **Complete Reservation**:
   - **Route**: `POST {BASE_URL}/completeReservation`
   - **Description**: Executes the `completeReservation` function to:
     - Process payment for the ticket using a mock payment function.
     - Render the `reservationConfirmation` view with a success or failure message and a "Check-In" link.
   - **Next Step**: User clicks the "Check-In" link to proceed to check-in.

6. **Check-In**:
   - **Route**: `GET {BASE_URL}/checkIn`
   - **Description**: Executes the `renderCheckInPage` function to render the `checkIn` view. The view displays reservation details and contains a form to enter the "Number of Bags."
   - **Next Step**: User submits the form to complete check-in.

7. **Complete Check-In**:
   - **Route**: `POST {BASE_URL}/completeCheckIn`
   - **Description**: Executes the `completeCheckIn` function to:
     - Update the reservation with the number of bags and mark it as checked in.
     - Render the final reservation details.

---

## API Documentation with Swagger

This project uses **Swagger** (OpenAPI) to document and test the API endpoints.

### Setting Up Swagger

1. **Install Swagger Dependencies**:
    Install the required packages for Swagger:
    ```bash
    pip install flask-swagger-ui
    ```

2. **Access the Swagger UI**:
    Once the application is running, open your browser and navigate to:
    [http://127.0.0.1:5001/flightreservation-flask-full/api-docs](http://127.0.0.1:5001/flightreservation-flask-full/api-docs)

3. **Swagger JSON**:
    The Swagger JSON specification is available at:
    [http://127.0.0.1:5001/flightreservation-flask-full/swagger.json](http://127.0.0.1:5001/flightreservation-flask-full/swagger.json)

---

## Mock Server vs Swagger

The Flight Reservation Flask Application provides two tools for testing and development: `mock_server.py` and `swagger`. Below is a comparison of their use cases:

| **Scenario**                              | **Use `mock_server.py`** | **Use `swagger`** |
|-------------------------------------------|--------------------------|-------------------|
| Frontend development without a backend    | ✅                       | ❌                |
| Testing real backend endpoints            | ❌                       | ✅                |
| API documentation                         | ❌                       | ✅                |
| Simulating backend behavior for prototyping | ✅                       | ❌                |

### Description

1. **`mock_server.py`**:
   - A standalone mock server that simulates the backend behavior with hardcoded responses.
   - Useful for frontend developers or prototyping when the real backend is unavailable.
   - Does not require a database or the actual Flask application to be running.

2. **`swagger`**:
   - Provides API documentation and a testing interface for the real backend endpoints.
   - Dynamically generates an OpenAPI (Swagger) specification for the Flask application.
   - Useful for documenting and testing the actual API endpoints.

---

## Using the Mock Server

The `mock_server.py` is a standalone mock server that simulates the backend behavior with hardcoded responses. It is useful for frontend development or prototyping when the real backend is unavailable.

### Steps to Use the Mock Server

1. **Start the Mock Server**:
   - Run the `mock_server.py` script:
     ```bash
     python /Users/kujinlee/code/copilotforjava/flightreservation-flask-full/tests/mock_server.py
     ```
   - By default, the mock server runs on port `5002`.

2. **Access the Mock Endpoints**:
   - Open your browser or use tools like Postman or cURL to test the mock endpoints. For example:
     - **Search for Flights**:
       ```
       http://127.0.0.1:5002/flightreservation-flask-full/findFlights
       ```
     - **Reserve a Flight**:
       ```
       http://127.0.0.1:5002/flightreservation-flask-full/reserve
       ```
     - **Create a Reservation** (POST method, cannot be tested in a browser):
       ```
       http://127.0.0.1:5002/flightreservation-flask-full/createReservation
       ```
     - **Check-In**:
       ```
       http://127.0.0.1:5002/flightreservation-flask-full/checkIn
       ```
     - **Complete Check-In** (POST method, cannot be tested in a browser):
       ```
       http://127.0.0.1:5002/flightreservation-flask-full/completeCheckIn
       ```

3. **Testing POST Endpoints**:
   Since `POST` methods cannot be tested directly in a browser, use one of the following tools:

   - **Using Postman**:
     1. Open Postman and create a new request.
     2. Set the method to `POST` and enter the endpoint URL. For example:
        ```
        http://127.0.0.1:5002/flightreservation-flask-full/createReservation
        ```
     3. Go to the **Body** tab and select **form-data** or **x-www-form-urlencoded**.
     4. Add the required fields. For example:
        ```
        flight_id: 1
        first_name: John
        last_name: Doe
        email: john.doe@example.com
        phone: 1234567890
        card_number: 4111111111111111
        amount: 200.00
        ```
     5. Click **Send** to submit the request and view the response.

   - **Using cURL**:
     1. Open a terminal.
     2. Use the following command to test a `POST` endpoint:
        ```bash
        curl -X POST http://127.0.0.1:5002/flightreservation-flask-full/createReservation \
        -d "flight_id=1" \
        -d "first_name=John" \
        -d "last_name=Doe" \
        -d "email=john.doe@example.com" \
        -d "phone=1234567890" \
        -d "card_number=4111111111111111" \
        -d "amount=200.00"
        ```
     3. View the response in the terminal.

   - **Using Python**:
     1. Use the provided `test_post.py` script to test the `POST` endpoints.
     2. Example script:
        ```python
        import requests

        url = "http://127.0.0.1:5002/flightreservation-flask-full/createReservation"
        data = {
            "flight_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "card_number": "4111111111111111",
            "amount": 200.00
        }

        response = requests.post(url, data=data)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        ```
     3. Save the script and run it:
        ```bash
        python test_post.py
        ```

---

## Running the Application

### Prerequisites
- Python 3.x installed
- Flask and required dependencies installed (`pip install -r requirements.txt`)

### Steps to Run
1. **Set the Environment Variables**:
   - Ensure the `BASE_URL` environment variable is set if needed. The default is `/flightreservation-flask-full`.

2. **Run the Application**:
   - The application is configured to run on port `5001`. To start the application, use:
     ```bash
     python app.py
     ```

3. **Using `flask run`**:
   - If you prefer to use `flask run`, ensure the port is set to `5001`:
     ```bash
     export FLASK_RUN_PORT=5001
     flask run
     ```

4. **Access the Application**:
   - Open your browser and navigate to `http://127.0.0.1:5001`.

### Notes
- The application uses `BASE_URL` to prefix routes. Ensure your templates and links use the correct `BASE_URL` dynamically. For example:
  ```html
  <p><a href="{{ BASE_URL }}/findFlights">Search for Flights</a></p>
  ```
- For production, ensure the `BASE_URL` is correctly set in the `.env` file to match the deployment path.

---

## Testing POST Endpoints

You can test the `POST` endpoints using the following methods:

### 1. **Using Postman**
1. Open Postman and create a new request.
2. Set the method to `POST` and enter the endpoint URL. For example:
   ```
   http://127.0.0.1:5002/flightreservation-flask-full/findFlights
   ```
3. Go to the **Body** tab and select **form-data** or **x-www-form-urlencoded**.
4. Add the required fields. For example:
   ```
   departure: AUS
   arrival: NYC
   date_of_departure: 02/05/2024
   ```
5. Click **Send** to submit the request and view the response.

---

### 2. **Using cURL**
1. Open a terminal.
2. Use the following command to test a `POST` endpoint:
   ```bash
   curl -X POST http://127.0.0.1:5002/flightreservation-flask-full/findFlights \
   -d "departure=AUS" \
   -d "arrival=NYC" \
   -d "date_of_departure=02/05/2024"
   ```
3. View the response in the terminal.

---

### 3. **Using Python**
1. Use the provided `test_post.py` script to test the `POST` endpoints.
2. Example script:
   ```python
   import requests

   url = "http://127.0.0.1:5002/flightreservation-flask-full/findFlights"
   data = {
       "departure": "AUS",
       "arrival": "NYC",
       "date_of_departure": "02/05/2024"
   }

   response = requests.post(url, data=data)
   print("Status Code:", response.status_code)
   print("Response Body:", response.text)
   ```
3. Save the script and run it:
   ```bash
   python test_post.py
   ```

---

### Available POST Endpoints
- `POST /flightreservation-flask-full/findFlights`: Search for flights.
- `POST /flightreservation-flask-full/createReservation`: Create a new reservation.
- `POST /flightreservation-flask-full/completeCheckIn`: Complete the check-in process.

Refer to the Swagger documentation for detailed information about the required parameters for each endpoint.

---

## Running Tests

The `tests` directory contains unit tests and integration tests for the application. These tests ensure the functionality of the application and its endpoints.

### Prerequisites
1. Ensure you have installed all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

### Running Tests with `pytest`
1. Navigate to the project root directory:
   ```bash
   cd /Users/kujinlee/code/copilotforjava/flightreservation-flask-full
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. Run a specific test file:
   ```bash
   pytest tests/test_routes.py
   ```

4. Run a specific test function:
   ```bash
   pytest tests/test_routes.py::test_find_flights
   ```

5. Generate a coverage report:
   ```bash
   pytest --cov=.
   ```

### Available Test Files
- **`tests/test_routes.py`**: Contains unit tests for the application's routes.
- **`tests/test_post.py`**: Contains a script to test the `POST` endpoints using the `requests` library.
- **`tests/conftest.py`**: Provides shared fixtures for the tests, such as the Flask app instance and database session.

### Notes
- Ensure the mock server (`mock_server.py`) is running if you are testing endpoints that rely on it.
- Use the `--disable-warnings` flag with `pytest` to suppress warnings:
  ```bash
  pytest --disable-warnings
  ```
