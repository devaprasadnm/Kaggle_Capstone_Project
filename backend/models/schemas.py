from pydantic import BaseModel
from typing import List, Optional

class EmissionInput(BaseModel):
    energy_usage_kwh: float
    fuel_consumption_liters: float
    distance_traveled_km: float
    waste_generated_kg: float
    company_size: int = 10

class EmissionOutput(BaseModel):
    emission_kg: float
    explanation: str
    
class OptimizationSuggestion(BaseModel):
    category: str
    suggestion: str
    potential_saving_kg: float

class OptimizationResponse(BaseModel):
    suggestions: List[OptimizationSuggestion]
    total_potential_savings: float

class ReportRequest(BaseModel):
    prediction: EmissionOutput
    optimization: OptimizationResponse
    company_name: str = "My Company"
