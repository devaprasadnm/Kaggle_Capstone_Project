import pandas as pd
import numpy as np

class DataCleaningAgent:
    def __init__(self):
        # Define column mappings for different CSV formats
        self.column_mappings = {
            'company_id': 'company_size',
            'energy_consumption_kwh': 'energy_usage_kwh',
            'fuel_used_liters': 'fuel_consumption_liters',
            'distance_travelled_km': 'distance_traveled_km',
            'industrial_waste_kg': 'waste_generated_kg',
        }
        
        # Expected model features
        self.expected_features = [
            'energy_usage_kwh',
            'fuel_consumption_liters', 
            'distance_traveled_km',
            'waste_generated_kg',
            'company_size'
        ]
    
    def map_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map various column names to expected model features"""
        # Create a copy to avoid modifying original
        df = df.copy()
        
        # Rename columns based on mapping
        df = df.rename(columns=self.column_mappings)
        
        # Keep only expected features (drop extras like carbon_emission_tons, renewable_energy_pct)
        available_features = [col for col in self.expected_features if col in df.columns]
        
        # If some features are missing, fill with defaults
        for feature in self.expected_features:
            if feature not in df.columns:
                if feature == 'company_size':
                    df[feature] = 10  # Default company size
                else:
                    df[feature] = 0  # Default to 0 for other features
        
        # Select only the expected features in the correct order
        df = df[self.expected_features]
        
        return df
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        # First map columns to expected schema
        df = self.map_columns(df)
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        # Fill non-numeric with mode
        non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
        for col in non_numeric_cols:
            if len(df[col].mode()) > 0:
                df[col] = df[col].fillna(df[col].mode()[0])
            
        return df

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        # Simple min-max normalization for demonstration
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
        return df
