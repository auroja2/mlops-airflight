from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from config.paths_config import *

app = Flask(__name__)

# Load the model
try:
    model = joblib.load(MODEL_SAVE_DIR)
    print("Model loaded successfully")
    
    # Test prediction with fewer, key features
    test_data = pd.DataFrame({
        'Class': [0],  # Business class
        'Type of Travel': [0],  # Business travel
        'Flight Distance': [1000],
        'Delay_ratio': [0],
        'Service_rating': [5],  # Combined service rating
    })
    test_pred = model.predict(test_data)
    print(f"Test prediction with ideal values: {test_pred[0]}")
    
except Exception as e:
    print(f"Error loading model: {str(e)}")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Get numeric inputs
            departure_delay = float(request.form["Departure Delay"])
            arrival_delay = float(request.form["Arrival Delay"])
            flight_distance = float(request.form["Flight Distance"])

            # Calculate delay ratio
            delay_ratio = (departure_delay + arrival_delay) / (flight_distance + 1)

            # Calculate average service rating
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

            # Create feature array with fewer features
            features = pd.DataFrame({
                'Class': [int(request.form["Class"])],
                'Type of Travel': [int(request.form["Type of Travel"])],
                'Flight Distance': [flight_distance],
                'Delay_ratio': [delay_ratio],
                'Service_rating': [avg_service_rating]
            })

            # Debug prints
            print("\nInput features:")
            print(features.to_dict('records')[0])
            
            # Prediction logic with business rules
            prediction = 0  # Default to not satisfied

            # Business class + Business travel + Good service = Satisfied
            if (int(request.form["Class"]) == 0 and  # Business Class
                int(request.form["Type of Travel"]) == 0 and  # Business Travel
                avg_service_rating >= 4.0):  # Good service
                prediction = 1

            # Long flight + Minimal delays + Good service = Satisfied
            if (flight_distance >= 500 and 
                delay_ratio < 0.1 and
                avg_service_rating >= 4.0):
                prediction = 1

            print(f"Final prediction: {prediction}")
            print(f"Average service rating: {avg_service_rating:.2f}")
            print(f"Delay ratio: {delay_ratio:.3f}")

            return render_template(
                "index.html", 
                prediction=int(prediction),
                features=features.to_dict('records')[0]
            )

        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
