# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5001

# Set environment variables
ENV FLASK_RUN_PORT=5001
ENV BASE_URL=/flightreservation-flask-full

# Run the application
CMD ["python", "app.py"]
