# app.py

from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load the trained vehicle maintenance prediction model
model_path = 'vehicle_model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

# Encoding dictionaries based on your actual categories
battery_status_encoding = {
    'New': 0,
    'Good': 1,
    'Weak': 2
}

tire_condition_encoding = {
    'New': 0,
    'Good': 1,
    'Worn Out': 2
}

brake_condition_encoding = {
    'New': 0,
    'Good': 1,
    'Worn Out': 2
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract and convert form inputs
        Vehicle_Age = float(request.form['Vehicle_Age'])
        Odometer_Reading = float(request.form['Odometer_Reading'])
        Service_History = float(request.form['Service_History'])
        Reported_Issues = float(request.form['Reported_Issues'])
        Accident_History = float(request.form['Accident_History'])
        Fuel_Efficiency = float(request.form['Fuel_Efficiency'])

        # Encode categorical inputs
        Battery_Status = battery_status_encoding[request.form['Battery_Status']]
        Tire_Condition = tire_condition_encoding[request.form['Tire_Condition']]
        Brake_Condition = brake_condition_encoding[request.form['Brake_Condition']]

        # Feature array in model-trained order
        features = [
            Vehicle_Age,
            Odometer_Reading,
            Service_History,
            Reported_Issues,
            Accident_History,
            Fuel_Efficiency,
            Battery_Status,
            Brake_Condition,
            Tire_Condition
        ]

        final_features = [np.array(features)]
        prediction = model.predict(final_features)

        output = "Maintenance Needed" if prediction[0] == 1 else "No Maintenance Needed"
        return render_template('index.html', prediction_text=f'Prediction: {output}')

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)
