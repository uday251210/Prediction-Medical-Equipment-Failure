from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"   # Required for session handling

# -------------------------
# Load the trained model
# -------------------------
MODEL_PATH = os.path.join("outputs", "models", "equipment_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
    TRAINING_COLUMNS = model.feature_names_in_
    print(f"✅ Model trained on {len(TRAINING_COLUMNS)} features.")
except FileNotFoundError:
    print(f"❌ FATAL ERROR: Trained model not found at '{MODEL_PATH}'")
    exit()


# -------------------------
# Login route
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        # Accept both admin/admin and admin/kvgn
        if username == "admin" and password in ["admin", "kvgn"]:
            session['user'] = username
            return redirect(url_for('home'))  # Redirect to home.html after login
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")


# -------------------------
# Home route
# -------------------------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


# -------------------------
# Index route (Prediction page)
# -------------------------
@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


# -------------------------
# Predict route
# -------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = {
            'Age': [float(request.form.get('Age', 0))],
            'Maintenance_Cost': [float(request.form.get('Maintenance_Cost', 0))],
            'Downtime': [float(request.form.get('Downtime', 0))],
            'Maintenance_Frequency': [float(request.form.get('Maintenance_Frequency', 0))],
            'Maintenance_Class': [int(request.form.get('Maintenance_Class', 1))],
            'Device_Type': [request.form.get('Device_Type', 'Unknown')],
            'Manufacturer': [request.form.get('Manufacturer', 'Unknown')],
            'Country': [request.form.get('Country', 'Unknown')],
            'Model': [request.form.get('Model', 'Unknown')]
        }

        input_df = pd.DataFrame(form_data)
        processed_df = pd.get_dummies(input_df)
        aligned_df = processed_df.reindex(columns=TRAINING_COLUMNS, fill_value=0)

        pred = model.predict(aligned_df)[0]
        result = "No Failure Expected" if pred == 1 else "Machine Failure Likely"

        history_csv = os.path.join("data", "predictions.csv")
        row = input_df.copy()
        row['Prediction'] = result
        if os.path.exists(history_csv):
            row.to_csv(history_csv, mode='a', header=False, index=False)
        else:
            row.to_csv(history_csv, index=False)

        return redirect(url_for('result', prediction=result))

    except Exception as e:
        return render_template('error.html', error_message=str(e))


# -------------------------
# Result route
# -------------------------
@app.route('/result/<prediction>')
def result(prediction):
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('result.html', prediction_text=prediction)


# -------------------------
# Download history CSV
# -------------------------
@app.route('/download_history')
def download_history():
    if 'user' not in session:
        return redirect(url_for('login'))

    history_csv = os.path.join("data", "predictions.csv")
    if os.path.exists(history_csv):
        return send_file(history_csv, as_attachment=True)
    else:
        return "No history file found."


# -------------------------
# Logout route
# -------------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# -------------------------
# Run the Flask app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
