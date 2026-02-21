import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df = pd.read_csv('data/crop_yield_dataset.csv')

# Features and Target
X = df.drop(columns=['Yield_per_Hectare'])
y = df['Yield_per_Hectare']

# Define categorical and numerical features
categorical_features = ['Crop_Type', 'Soil_Type', 'Fertilizer_Type', 'Irrigation_Method', 'Season']
numerical_features = [
    'Nitrogen', 'Phosphorus', 'Potassium', 'Soil_pH', 'Soil_Moisture', 
    'Temperature', 'Rainfall', 'Humidity', 'Sunlight_Hours', 'Fertilizer_Dosage', 
    'Growth_Duration', 'Area'
]

# Create preprocessing pipeline
# Handle unknown categories in future data by ignoring them or handling gracefully
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models to try
models = {
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

best_model = None
best_score = -np.inf
best_name = ""

results = {}

print("Training models...")

for name, model in models.items():
    # Create full pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('model', model)])
    
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    results[name] = {'R2': r2, 'RMSE': rmse}
    print(f"{name} - R2: {r2:.4f}, RMSE: {rmse:.4f}")
    
    if r2 > best_score:
        best_score = r2
        best_model = clf
        best_name = name

print(f"\nBest Model: {best_name} with R2: {best_score:.4f}")

# Save the best model
# The pipeline includes the preprocessor, so we just save the one object
joblib.dump(best_model, 'models/crop_yield_model.pkl')
print("Model saved to models/crop_yield_model.pkl")

# Save a separate preprocessor if needed, but Pipeline handles it. 
# We might want to save column names for the API to know expected inputs
input_columns = {
    'categorical': categorical_features,
    'numerical': numerical_features
}
joblib.dump(input_columns, 'models/model_columns.pkl')
print("Model columns metadata saved to models/model_columns.pkl")
