import pandas as pd
import joblib
import os
import sys

# Add backend to path to import agent if needed, but let's test raw model first
sys.path.append(os.path.join(os.getcwd(), 'backend'))

def test_model():
    model_path = "ml/models/carbon_emission_model.pkl"
    print(f"Testing model at: {model_path}")
    
    if not os.path.exists(model_path):
        print("Model file does not exist!")
        return

    try:
        model = joblib.load(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Create sample data matching the training schema
    data = {
        'energy_usage_kwh': [1200],
        'fuel_consumption_liters': [600],
        'distance_traveled_km': [800],
        'waste_generated_kg': [50],
        'company_size': [50]
    }
    df = pd.DataFrame(data)
    print("Input Data:")
    print(df)

    try:
        prediction = model.predict(df)
        print(f"Prediction: {prediction[0]}")
    except Exception as e:
        print(f"Prediction failed: {e}")
        if hasattr(model, "feature_names_in_"):
            print(f"Model expects features: {model.feature_names_in_}")

if __name__ == "__main__":
    test_model()
