import pandas as pd
import numpy as np
import random

# Constants for data generation
NUM_ROWS = 15000

CROPS = [
    'Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Tea', 'Coffee', 'Jute', 'Potato', 'Onion'
]

# Ideal conditions for each crop (approximate averages)
# N, P, K in kg/ha
# pH: 0-14
# Temp: Celsius
# Moisture: %
CROP_PROFILE = {
    'Rice': {'N': 80, 'P': 40, 'K': 40, 'pH': 6.5, 'Moisture': 80, 'Temp': 25, 'Rainfall': 200, 'Humidity': 80},
    'Wheat': {'N': 60, 'P': 30, 'K': 30, 'pH': 6.5, 'Moisture': 50, 'Temp': 20, 'Rainfall': 100, 'Humidity': 60},
    'Maize': {'N': 100, 'P': 50, 'K': 50, 'pH': 6.5, 'Moisture': 60, 'Temp': 25, 'Rainfall': 150, 'Humidity': 65},
    'Cotton': {'N': 120, 'P': 60, 'K': 60, 'pH': 7.0, 'Moisture': 50, 'Temp': 30, 'Rainfall': 80, 'Humidity': 55},
    'Sugarcane': {'N': 150, 'P': 70, 'K': 70, 'pH': 6.5, 'Moisture': 70, 'Temp': 28, 'Rainfall': 180, 'Humidity': 70},
    'Tea': {'N': 100, 'P': 40, 'K': 40, 'pH': 5.5, 'Moisture': 75, 'Temp': 24, 'Rainfall': 250, 'Humidity': 85},
    'Coffee': {'N': 110, 'P': 50, 'K': 50, 'pH': 6.0, 'Moisture': 70, 'Temp': 23, 'Rainfall': 220, 'Humidity': 80},
    'Jute': {'N': 80, 'P': 40, 'K': 40, 'pH': 6.5, 'Moisture': 85, 'Temp': 30, 'Rainfall': 180, 'Humidity': 85},
    'Potato': {'N': 50, 'P': 30, 'K': 80, 'pH': 5.8, 'Moisture': 60, 'Temp': 18, 'Rainfall': 120, 'Humidity': 70},
    'Onion': {'N': 60, 'P': 40, 'K': 40, 'pH': 6.5, 'Moisture': 55, 'Temp': 22, 'Rainfall': 90, 'Humidity': 60}
}

SOIL_TYPES = ['Clay', 'Sandy', 'Loam', 'Silt', 'Peaty', 'Chalky']
SEASONS = ['Kharif', 'Rabi', 'Zaid', 'Whole Year']
IRRIGATION_METHODS = ['Drip', 'Sprinkler', 'Flood', 'Rainfed']
FERTILIZER_TYPES = ['Urea', 'DAP', 'MOP', 'NPK', 'Superphosphate', 'Organic', 'None']

def generate_data():
    data = []
    
    for _ in range(NUM_ROWS):
        crop = random.choice(CROPS)
        profile = CROP_PROFILE[crop]
        
        # Add random variation to ideal conditions
        n = max(0, int(np.random.normal(profile['N'], 20)))
        p = max(0, int(np.random.normal(profile['P'], 15)))
        k = max(0, int(np.random.normal(profile['K'], 15)))
        ph = max(4.0, min(10.0, np.random.normal(profile['pH'], 0.5)))
        moisture = max(20, min(100, np.random.normal(profile['Moisture'], 10)))
        temp = max(10, min(45, np.random.normal(profile['Temp'], 5)))
        rainfall = max(0, np.random.normal(profile['Rainfall'], 50))
        humidity = max(20, min(100, np.random.normal(profile['Humidity'], 10)))
        sunlight = max(2, min(14, np.random.normal(8, 2)))
        
        soil = random.choice(SOIL_TYPES)
        season = random.choice(SEASONS)
        irrigation = random.choice(IRRIGATION_METHODS)
        fertilizer = random.choice(FERTILIZER_TYPES)
        dosage = max(0, np.random.normal(100, 30)) if fertilizer != 'None' else 0
        
        area = round(random.uniform(0.5, 20.0), 2) # In Hectares internally
        growth_days = int(np.random.normal(120, 20)) # Varies by crop reality but simplifying for random gen
        
        # Calculate Base Yield (tons/ha) - Simplified agronomic logic
        base_yield = 5.0 # baseline
        
        # Nutrient Impact
        # Optimal NPK boosts yield, deficiency hurts it
        nutrient_score = 1.0
        if n < profile['N'] * 0.7: nutrient_score -= 0.1
        if p < profile['P'] * 0.7: nutrient_score -= 0.05
        if k < profile['K'] * 0.7: nutrient_score -= 0.05
        
        # Weather Impact
        weather_score = 1.0
        if abs(temp - profile['Temp']) > 5: weather_score -= 0.2
        if moisture < profile['Moisture'] * 0.6: weather_score -= 0.2
        if rainfall < profile['Rainfall'] * 0.5 and irrigation == 'Rainfed': weather_score -= 0.4
        
        # Fertilizer Impact
        fert_boost = 0
        if fertilizer != 'None':
            # Diminishing returns curve logic (simplified)
            fert_boost = min(0.3, (dosage / 200.0) * 0.3) 
            
        # Irrigation Impact
        irri_boost = 0.0
        if irrigation in ['Drip', 'Sprinkler']:
            irri_boost = 0.2
        elif irrigation == 'Flood':
            irri_boost = 0.1
            
        # Random noise
        noise = np.random.normal(0, 0.5)
        
        # Final Yield Calculation
        # Crop specific potential (arbitrary scalar for realism)
        crop_potential = {
             'Rice': 4.0, 'Wheat': 3.5, 'Maize': 5.0, 'Cotton': 2.0, 
             'Sugarcane': 80.0, 'Tea': 2.0, 'Coffee': 1.5, 
             'Jute': 2.5, 'Potato': 20.0, 'Onion': 15.0
        }
        
        yield_per_ha = crop_potential[crop] * nutrient_score * weather_score * (1 + fert_boost + irri_boost) + noise
        yield_per_ha = max(0.1, yield_per_ha) # Ensure positive
        
        data.append([
            crop, n, p, k, round(ph, 1), round(moisture, 1), soil, 
            round(temp, 1), round(rainfall, 1), round(humidity, 1), round(sunlight, 1),
            fertilizer, round(dosage, 1), irrigation, growth_days, season, area, round(yield_per_ha, 3)
        ])

    columns = [
        'Crop_Type', 'Nitrogen', 'Phosphorus', 'Potassium', 'Soil_pH', 'Soil_Moisture', 'Soil_Type', 
        'Temperature', 'Rainfall', 'Humidity', 'Sunlight_Hours', 'Fertilizer_Type', 'Fertilizer_Dosage', 
        'Irrigation_Method', 'Growth_Duration', 'Season', 'Area', 'Yield_per_Hectare'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('data/crop_yield_dataset.csv', index=False)
    print(f"Dataset generated with {NUM_ROWS} rows at data/crop_yield_dataset.csv")

if __name__ == "__main__":
    generate_data()
