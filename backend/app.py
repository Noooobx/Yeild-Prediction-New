from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load Model & Pipeline
MODEL_PATH = 'models/crop_yield_xgb.pkl'

if os.path.exists(MODEL_PATH):
    model_pipeline = joblib.load(MODEL_PATH)
    print(f"XGBoost Pipeline loaded successfully from {MODEL_PATH}")
else:
    model_pipeline = None
    print(f"Error: Model file not found at {MODEL_PATH}")

# Column metadata no longer needed as Pipeline handles it via ColumnTransformer


def convert_area_to_hectare(area, unit):
    unit = unit.lower()
    if unit == 'hectare':
        return area
    elif unit == 'acre':
        return area * 0.404686
    elif unit == 'sq_meter':
        return area * 0.0001
    else:
        return area  # Default or throw error

def convert_yield(yield_val, target_unit):
    # yield_val is in tons/ha
    target_unit = target_unit.lower()
    
    if target_unit == 'ton':
        return yield_val
    elif target_unit == 'kg':
        return yield_val * 1000
    elif target_unit == 'quintal':
        return yield_val * 10
    else:
        return yield_val

@app.route('/predict', methods=['POST'])
def predict():
    if not model_pipeline:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        data = request.json
        print("Received data:", data)
        
        # 1. Parse and Validate Input
        # Required fields check could be added here
        
        # 2. Prepare Input DataFrame
        input_data = {
            'Crop_Type': data.get('Crop_Type'),
            'Nitrogen': float(data.get('Nitrogen', 0)),
            'Phosphorus': float(data.get('Phosphorus', 0)),
            'Potassium': float(data.get('Potassium', 0)),
            'Soil_pH': float(data.get('Soil_pH', 6.5)),
            'Soil_Moisture': float(data.get('Soil_Moisture', 50)),
            'Soil_Type': data.get('Soil_Type'),
            'Temperature': float(data.get('Temperature', 25)),
            'Rainfall': float(data.get('Rainfall', 100)),
            'Humidity': float(data.get('Humidity', 60)),
            'Sunlight_Hours': float(data.get('Sunlight_Hours', 8)),
            'Fertilizer_Type': data.get('Fertilizer_Type', 'None'),
            'Fertilizer_Dosage': float(data.get('Fertilizer_Dosage', 0)),
            'Irrigation_Method': data.get('Irrigation_Method'),
            'Growth_Duration': float(data.get('Growth_Duration', 120)),
            'Season': data.get('Season'),
            'Area': convert_area_to_hectare(float(data.get('Area', 1)), data.get('Area_Unit', 'Hectare'))
        }
        
        # Create DataFrame
        df = pd.DataFrame([input_data])
        
        # 3. Predict Yield per Hectare
        # The pipeline handles scaling and one-hot encoding internally
        prediction_per_ha = model_pipeline.predict(df)[0]
        
        # 4. Calculate Total Yield
        area_ha = input_data['Area']
        total_yield_tons = prediction_per_ha * area_ha
        
        # 5. Unit Conversion
        yield_unit = data.get('Yield_Unit', 'Ton')
        
        final_yield_per_ha = convert_yield(prediction_per_ha, yield_unit)
        final_total_yield = convert_yield(total_yield_tons, yield_unit)
        
        response = {
            'Yield_per_Hectare': float(round(final_yield_per_ha, 3)),
            'Total_Yield': float(round(final_total_yield, 3)),
            'Yield_Unit': yield_unit,
            'Area_in_Hectares': float(round(area_ha, 3))
        }
        
        return jsonify(response)

    except Exception as e:
        print("Error during prediction:", e)
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
