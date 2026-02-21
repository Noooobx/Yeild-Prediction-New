import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load Data
print("Loading dataset...")
df = pd.read_csv('data/merged_agricultural_data.csv')

# 2. EDA & Cleaning (Simplified for script)
# Remove realistic outliers (e.g. negative yields or impossible pH) -> Generator handles most, but good practice
df = df[df['Yield_per_Hectare'] > 0]
df = df[(df['Soil_pH'] > 0) & (df['Soil_pH'] < 14)]

# Save basic correlation plot for user
plt.figure(figsize=(10, 8))
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm')
plt.title("Feature Correlation Matrix")
plt.savefig("data/correlation_matrix.png")
print("Saved correlation matrix to data/correlation_matrix.png")

# 3. Prepare Pipeline
X = df.drop(columns=['Yield_per_Hectare', 'Cluster_Label', 'Area']) # Area is linear scaling, not yield driver per se
y = df['Yield_per_Hectare']

categorical_features = ['Crop_Type', 'Soil_Type', 'Fertilizer_Type', 'Irrigation_Method', 'Season']
numerical_features = [
    'Nitrogen', 'Phosphorus', 'Potassium', 'Soil_pH', 'Soil_Moisture', 
    'Temperature', 'Rainfall', 'Humidity', 'Sunlight_Hours', 'Fertilizer_Dosage', 
    'Growth_Duration'
]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# 4. XGBoost Model with optimization
xgb = XGBRegressor(objective='reg:squarederror', n_jobs=-1, random_state=42)

pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', xgb)])

# Grid Search for Tuning (Simplified)
param_grid = {
    'model__n_estimators': [100, 200],
    'model__learning_rate': [0.05, 0.1],
    'model__max_depth': [5, 7]
}

print("Starting Grid Search for Hyperparameter Tuning...")
search = GridSearchCV(pipeline, param_grid, cv=3, scoring='r2', verbose=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

search.fit(X_train, y_train)
best_model = search.best_estimator_

# 5. Evaluation
y_pred = best_model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\nTraining Complete.")
print(f"Best Params: {search.best_params_}")
print(f"R2 Score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

# 6. Save Artifacts
joblib.dump(best_model, 'models/crop_yield_xgb.pkl')
print("Saved model to models/crop_yield_xgb.pkl")

# Save feature importance plot (Tricky with Pipeline, skipping complex extraction for now)
