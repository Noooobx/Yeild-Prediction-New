import numpy as np
import pandas as pd
import random

# Configuration
NUM_SAMPLES = 20000
CROPS = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Tea', 'Coffee', 'Jute', 'Potato', 'Onion']
SEASONS = ['Kharif', 'Rabi', 'Zaid', 'Whole Year']

# Define Clusters representing different Farming Systems
# N, P, K, pH, Moisture, Temp, Rain, Yield_Factor (Multiplies base yield)
CLUSTERS = {
    'Commercial_High_Input': {
        'N': (120, 20), 'P': (60, 15), 'K': (60, 15), 
        'Fertilizer_Dosage': (150, 30), 'Yield_Factor': (1.2, 0.1),
        'Irrigation_Prob': {'Drip': 0.4, 'Sprinkler': 0.3, 'Flood': 0.3, 'Rainfed': 0.0}
    },
    'Subsistence_Low_Input': {
        'N': (60, 15), 'P': (30, 10), 'K': (30, 10), 
        'Fertilizer_Dosage': (50, 20), 'Yield_Factor': (0.7, 0.15),
        'Irrigation_Prob': {'Drip': 0.0, 'Sprinkler': 0.1, 'Flood': 0.3, 'Rainfed': 0.6}
    },
    'Optimized_Eco_Farming': {
        'N': (90, 10), 'P': (45, 10), 'K': (45, 10), 
        'Fertilizer_Dosage': (100, 15), 'Yield_Factor': (1.1, 0.05),
        'Irrigation_Prob': {'Drip': 0.6, 'Sprinkler': 0.2, 'Flood': 0.2, 'Rainfed': 0.0}
    },
    'Stress_Drought': {
        'N': (70, 20), 'P': (35, 15), 'K': (35, 15), 
        'Fertilizer_Dosage': (60, 30), 'Yield_Factor': (0.4, 0.2), # Severe yield penalty
        'Irrigation_Prob': {'Drip': 0.1, 'Sprinkler': 0.1, 'Flood': 0.1, 'Rainfed': 0.7}
    }
}

CROP_BASE_YIELD = {
    'Rice': (4.0, 0.5), 'Wheat': (3.5, 0.4), 'Maize': (5.0, 0.6), 'Cotton': (2.0, 0.3),
    'Sugarcane': (80.0, 10.0), 'Tea': (2.0, 0.2), 'Coffee': (1.5, 0.2), 
    'Jute': (2.5, 0.3), 'Potato': (20.0, 3.0), 'Onion': (15.0, 2.0)
}

def generate_dataset():
    data = []
    
    for _ in range(NUM_SAMPLES):
        # 1. Select a Crop
        crop = random.choice(CROPS)
        base_yield_mean, base_yield_std = CROP_BASE_YIELD[crop]
        
        # 2. Select a Farming Cluster (Scenario)
        cluster_name = random.choices(list(CLUSTERS.keys()), weights=[0.4, 0.3, 0.2, 0.1])[0]
        cluster = CLUSTERS[cluster_name]
        
        # 3. Sample independant variables from Cluster distributions
        n = max(0, np.random.normal(cluster['N'][0], cluster['N'][1]))
        p = max(0, np.random.normal(cluster['P'][0], cluster['P'][1]))
        k = max(0, np.random.normal(cluster['K'][0], cluster['K'][1]))
        fert_dosage = max(0, np.random.normal(cluster['Fertilizer_Dosage'][0], cluster['Fertilizer_Dosage'][1]))
        
        # 4. Sample Weather (Correlated with Cluster somewhat - e.g. Drought has high temp)
        if cluster_name == 'Stress_Drought':
            temp = np.random.normal(35, 5) # Hot
            rain = max(0, np.random.normal(50, 30)) # Dry
            moisture = np.random.normal(30, 10) # Dry soil
        else:
            temp = np.random.normal(25, 5)
            rain = max(0, np.random.normal(150, 50))
            moisture = np.random.normal(60, 15)
            
        ph = np.random.normal(6.5, 0.5)
        humidity = np.random.normal(70, 10)
        sunlight = np.random.normal(8, 2)
        
        # 5. Categorical
        irrigation = random.choices(list(cluster['Irrigation_Prob'].keys()), 
                                    weights=list(cluster['Irrigation_Prob'].values()))[0]
        season = random.choice(SEASONS)
        soil_type = random.choice(['Clay', 'Sandy', 'Loam', 'Silt'])
        
        # 6. Determine Yield (Using Cluster Factor + Noise - NO FORMULA)
        # We use the cluster's "Yield Factor" distribution to determine outcome
        # This simulates that "Commercial" farms yield high, "Drought" yields low
        # The ML model will have to LEARN that High N + Temp + Rain = High Yield
        # Without us writing `Yield = N * 0.5 + P * 0.2`
        
        yield_factor = max(0.1, np.random.normal(cluster['Yield_Factor'][0], cluster['Yield_Factor'][1]))
        final_yield = max(0, np.random.normal(base_yield_mean, base_yield_std) * yield_factor)
        
        area = round(random.uniform(0.5, 10.0), 2)
        
        data.append({
            'Crop_Type': crop,
            'Nitrogen': round(n, 1), 'Phosphorus': round(p, 1), 'Potassium': round(k, 1),
            'Soil_pH': round(ph, 1), 'Soil_Moisture': round(moisture, 1), 'Soil_Type': soil_type,
            'Temperature': round(temp, 1), 'Rainfall': round(rain, 1), 'Humidity': round(humidity, 1),
            'Sunlight_Hours': round(sunlight, 1),
            'Fertilizer_Type': 'Complex', # Simplified
            'Fertilizer_Dosage': round(fert_dosage, 1),
            'Irrigation_Method': irrigation,
            'Growth_Duration': int(np.random.normal(120, 15)),
            'Season': season,
            'Area': area,
            'Yield_per_Hectare': round(final_yield, 3),
            'Cluster_Label': cluster_name # For debugging/EDA, not training
        })
        
    df = pd.DataFrame(data)
    df.to_csv('data/merged_agricultural_data.csv', index=False)
    print(f"Generated {NUM_SAMPLES} samples in data/merged_agricultural_data.csv")

if __name__ == "__main__":
    generate_dataset()
