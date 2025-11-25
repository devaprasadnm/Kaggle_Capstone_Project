import joblib
import pandas as pd
import os
import numpy as np

class EmissionPredictionAgent:
    def __init__(self, model_path: str = None):
        if model_path is None:
            # Construct absolute path relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.model_path = os.path.join(base_dir, "ml", "models", "carbon_emission_model.pkl")
        else:
            self.model_path = model_path
            
        self.model = None
        self._load_model()
        self._setup_llm()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print(f"Model loaded successfully from {self.model_path}")
            except Exception as e:
                print(f"Failed to load model: {e}")
        else:
            print(f"Warning: Model not found at {self.model_path}")

    def predict(self, data: pd.DataFrame) -> float:
        if self.model is None:
            print("Model is None, returning 0.0")
            return 0.0
        
        try:
            # Ensure columns are in the correct order if possible, or just pass data
            # The model expects specific features.
            # Let's try to predict.
            prediction = self.model.predict(data)
            return float(prediction[0])
        except Exception as e:
            print(f"Prediction error: {e}")
            # Check for feature mismatch
            if hasattr(self.model, "feature_names_in_"):
                print(f"Model expects: {self.model.feature_names_in_}")
                print(f"Data has: {data.columns}")
            return 0.0

    def _setup_llm(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.llm_model = genai.GenerativeModel('gemini-2.5-flash')
                print("LLM initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize LLM: {e}")
                self.llm_model = None
        else:
            self.llm_model = None
            print("Warning: GOOGLE_API_KEY not found. LLM features will be disabled.")

    def explain(self, input_data: dict, prediction: float) -> str:
        if self.llm_model:
            try:
                prompt = f"""
                Act as a Carbon Emission Expert.
                Analyze the following operational data and the predicted carbon emission value.
                
                Data: {input_data}
                Predicted Emission: {prediction:.2f} kg CO2e
                
                Provide a concise, professional explanation (max 2-3 sentences) of the primary factors contributing to this emission level. 
                Focus on the most significant contributors based on the data provided.
                """
                response = self.llm_model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"LLM generation failed: {e}")
                # Fallback to simulation if LLM fails
        
        # Simulate LLM explanation (Fallback)
        reasons = []
        if input_data.get('energy_usage_kwh', 0) > 1000:
            reasons.append("high energy usage")
        if input_data.get('fuel_consumption_liters', 0) > 500:
            reasons.append("significant fuel consumption")
        
        reason_str = " and ".join(reasons) if reasons else "balanced factors"
        return f"The predicted carbon emission is {prediction:.2f} kg CO2e. This is primarily driven by {reason_str}."
