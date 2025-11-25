import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# 1. Generate Synthetic Data
def generate_data(n_samples=1000):
    np.random.seed(42)
    data = {
        'energy_usage_kwh': np.random.uniform(100, 5000, n_samples),
        'fuel_consumption_liters': np.random.uniform(50, 2000, n_samples),
        'distance_traveled_km': np.random.uniform(10, 1000, n_samples),
        'waste_generated_kg': np.random.uniform(10, 500, n_samples),
        'company_size': np.random.randint(1, 1000, n_samples)
    }
    df = pd.DataFrame(data)
    
    # Simplified formula for carbon emission (target)
    # Emission = Energy*0.5 + Fuel*2.3 + Distance*0.2 + Waste*0.1
    df['carbon_emission_kg'] = (
        df['energy_usage_kwh'] * 0.5 +
        df['fuel_consumption_liters'] * 2.3 +
        df['distance_traveled_km'] * 0.2 +
        df['waste_generated_kg'] * 0.1 +
        np.random.normal(0, 50, n_samples) # Add noise
    )
    return df

def train_model():
    print("Generating synthetic data...")
    df = generate_data()
    
    X = df.drop('carbon_emission_kg', axis=1)
    y = df['carbon_emission_kg']
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R2 Score: {r2:.2f}")
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/carbon_emission_model.pkl')
    print("Model saved to models/carbon_emission_model.pkl")

if __name__ == "__main__":
    train_model()
