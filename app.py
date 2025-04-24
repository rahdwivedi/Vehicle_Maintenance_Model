from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set your secret key for session handling

# Load the trained model
model_path = 'vehicle_model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Encoding dictionaries
battery_status_encoding = {'New': 0, 'Good': 1, 'Weak': 2}
tire_condition_encoding = {'New': 0, 'Good': 1, 'Worn Out': 2}
brake_condition_encoding = {'New': 0, 'Good': 1, 'Worn Out': 2}

# Dummy user credentials
users = {
    'admin': 'admin@123'
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        Vehicle_Age = float(request.form['Vehicle_Age'])
        Odometer_Reading = float(request.form['Odometer_Reading'])
        Service_History = float(request.form['Service_History'])
        Reported_Issues = float(request.form['Reported_Issues'])
        Accident_History = float(request.form['Accident_History'])
        Fuel_Efficiency = float(request.form['Fuel_Efficiency'])
        Battery_Status = battery_status_encoding[request.form['Battery_Status']]
        Tire_Condition = tire_condition_encoding[request.form['Tire_Condition']]
        Brake_Condition = brake_condition_encoding[request.form['Brake_Condition']]

        features = [Vehicle_Age, Odometer_Reading, Service_History, Reported_Issues,
                    Accident_History, Fuel_Efficiency, Battery_Status, Brake_Condition, Tire_Condition]
        final_features = [np.array(features)]
        prediction = model.predict(final_features)

        output = "Maintenance Needed" if prediction[0] == 1 else "No Maintenance Needed"
        return render_template('index.html', prediction_text=f'Prediction: {output}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)





