# Medical Equipment Failure Prototype

This is a full-stack prototype (Flask + SQLite + ML) trained on the provided dataset.

## Quick summary of training
- Dataset used: Medical_Device_Failure_dataset.csv
- Rows: 4149, Columns: 14
- Target created: `failure` = 1 if `Failure_Event_Count` > 0 else 0
- Model: RandomForestClassifier in a sklearn Pipeline (with preprocessing)
- Test accuracy: 0.8566

## Run locally
1. (Optional) create virtualenv and install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize DB:
   ```bash
   python database/init_db.py
   ```
3. Copy trained model into model/ (already included)
4. Run app:
   ```bash
   python app.py
   ```
5. Open http://127.0.0.1:5000/

## Files included
- model/equipment_model.pkl (trained model pipeline)
- app.py (Flask app)
- database/init_db.py
- templates/, static/ (frontend)
- requirements.txt