from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
import os
from config.paths_config import *

app = Flask(__name__)

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the model with comprehensive error handling
try:
    model_path = os.getenv('MODEL_PATH', MODEL_SAVE_DIR)
    model = joblib.load(model_path)
    logger.info("Model loaded successfully")
    
    # Validate model with test prediction
    test_data = pd.DataFrame({
        'Class': [0],  # Business class
        'Type of Travel': [0],  # Business travel
        'Flight Distance': [1000],
        'Service_rating': [5],  # Combined service rating
        'Delay_ratio': [0]
    })
    test_pred = model.predict(test_data)
    logger.info(f"Model validation prediction: {test_pred[0]}")

except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

@app.route("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Get and validate numeric inputs
            flight_distance = max(0, float(request.form["Flight Distance"]))
            departure_delay = max(0, float(request.form["Departure Delay"]))
            arrival_delay = max(0, float(request.form["Arrival Delay"]))

            # Calculate delay ratio with safety checks
            total_delay = departure_delay + arrival_delay
            delay_ratio = 0 if flight_distance == 0 else min(1.0, total_delay / (flight_distance + 1))

            # Calculate service quality score
            service_ratings = [
                int(request.form["Online Boarding"]),
                int(request.form["Inflight wifi service"]),
                int(request.form["Inflight entertainment"]),
                int(request.form["Seat comfort"]),
                int(request.form["Leg room service"]),
                int(request.form["On-board service"]),
                int(request.form["Cleanliness"]),
                int(request.form["Ease of Online Booking"])
            ]
            avg_service_rating = sum(service_ratings) / len(service_ratings)

            # Create feature DataFrame
            features = pd.DataFrame({
                'Class': [int(request.form["Class"])],
                'Type of Travel': [int(request.form["Type of Travel"])],
                'Flight Distance': [flight_distance],
                'Service_rating': [avg_service_rating],
                'Delay_ratio': [delay_ratio]
            })

            # Log input features for debugging
            logger.info(f"Input features: {features.to_dict('records')[0]}")

            # Initialize prediction
            prediction = 0

            # Business rules for satisfaction
            is_business = int(request.form["Class"]) == 0
            is_business_travel = int(request.form["Type of Travel"]) == 0
            good_service = avg_service_rating >= 4.0
            minimal_delays = delay_ratio < 0.1
            long_flight = flight_distance >= 500

            # Apply satisfaction rules
            if (is_business and is_business_travel and good_service) or \
               (long_flight and minimal_delays and good_service):
                prediction = 1

            # Override with model prediction if available
            if model is not None:
                model_pred = model.predict(features)[0]
                if model_pred == 1 or prediction == 1:
                    prediction = 1

            logger.info(f"Final prediction: {prediction}")

            return render_template(
                "index.html",
                prediction=prediction,
                features=features.to_dict('records')[0]
            )

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    # Set debug mode based on environment
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting Flask app on port {port} with debug={debug_mode}")
    app.run(debug=debug_mode, port=port)