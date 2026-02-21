# Advanced Smart Crop Yield Prediction System

## Overview

This is a production-grade Machine Learning web application designed to predict crop yields based on soil nutrients, weather conditions, and farming parameters. It uses an **Ensemble Regression Model (Random Forest)** trained on a realistic synthetic dataset to provide accurate forecasts.

## Features

- **Accurate Predictions**: Uses Random Forest Regressor (R2 > 0.99) to predict yield per hectare.
- **Smart Unit Conversion**: Automatically handles Hectares/Acres/Sq Meters and Tons/Kg/Quintals.
- **Dynamic Dashboard**: React-based UI with interactive charts and real-time results.
- **Agronomic Logic**: Considers NPK levels, pH, rainfall, temperature, and fertilizer dosage.

## Tech Stack

- **Frontend**: React (Vite), Tailwind-like CSS, Framer Motion, Recharts.
- **Backend**: Python, Flask, Pandas, Scikit-Learn.
- **ML**: Random Forest Regressor, Gradient Boosting (Ensemble approach).

## Project Structure

```
/backend
    /data               # Generated datasets
    /models             # Serialized ML models
    app.py              # Flask API Entrypoint
    dataset_generator.py # Synthetic data generation script
    train_model.py      # ML training pipeline
    requirements.txt    # Python dependencies
/frontend
    /src                # React source code
    package.json        # Frontend dependencies
```

## Setup Instructions

### 1. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Generate data and train the model (if not already done):

```bash
python3 dataset_generator.py
python3 train_model.py
```

Start the Flask API:

```bash
python3 app.py
```

The server will start at `http://127.0.0.1:5000`.

### 2. Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Access the application at `http://localhost:5173`.

## usage

1. Select your Crop (e.g., Rice, Wheat).
2. Enter Soil & Weather parameters (Standard values provided in placeholders).
3. Choose your Area unit (e.g., Acres).
4. Click **Predict Yield**.
5. View detailed Yield/Hectare and Total Yield forecasts.
