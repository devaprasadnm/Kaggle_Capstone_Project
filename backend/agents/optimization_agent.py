from typing import List, Dict
from models.schemas import OptimizationSuggestion

import os
import json
import google.generativeai as genai

class OptimizationAgent:
    def __init__(self):
        self._setup_llm()

    def _setup_llm(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.llm_model = genai.GenerativeModel('gemini-2.5-flash')
                print("Optimization Agent LLM initialized.")
            except Exception as e:
                print(f"Failed to initialize Optimization LLM: {e}")
                self.llm_model = None
        else:
            self.llm_model = None

    def optimize(self, data: Dict[str, float], current_emission: float) -> List[OptimizationSuggestion]:
        suggestions = []
        
        if self.llm_model:
            try:
                prompt = f"""
                Act as a Sustainability Consultant.
                Based on the following data and total emission, suggest 3 specific optimization strategies to reduce carbon footprint.
                
                Data: {data}
                Total Emission: {current_emission} kg CO2e
                
                Return the response strictly as a JSON list of objects. Each object must have:
                - "category": string (e.g., Energy, Logistics, Fuel)
                - "suggestion": string (actionable advice)
                - "potential_saving_kg": float (estimated saving)
                
                Do not include markdown formatting like ```json ... ```. Just the raw JSON array.
                """
                response = self.llm_model.generate_content(prompt)
                text = response.text.strip()
                
                # Clean up markdown if present
                if text.startswith("```json"):
                    text = text[7:]
                elif text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                
                data_json = json.loads(text.strip())
                for item in data_json:
                    suggestions.append(OptimizationSuggestion(**item))
                
                if suggestions:
                    return suggestions
            except Exception as e:
                print(f"LLM optimization failed: {e}")
                # Fallback to heuristics if LLM fails
        
        # Heuristic Fallback
        energy = data.get('energy_usage_kwh', 0)
        fuel = data.get('fuel_consumption_liters', 0)
        distance = data.get('distance_traveled_km', 0)
        
        # Simple heuristic for savings
        if energy > 1000:
            saving = current_emission * 0.10 # 10%
            suggestions.append(OptimizationSuggestion(
                category="Energy",
                suggestion="Switch to LED lighting and optimize HVAC schedules.",
                potential_saving_kg=saving
            ))
            
        if fuel > 500:
            saving = current_emission * 0.15 # 15%
            suggestions.append(OptimizationSuggestion(
                category="Fuel",
                suggestion="Upgrade fleet to electric vehicles or hybrid models.",
                potential_saving_kg=saving
            ))
            
        if distance > 500:
            saving = current_emission * 0.05 # 5%
            suggestions.append(OptimizationSuggestion(
                category="Logistics",
                suggestion="Optimize delivery routes using route planning software.",
                potential_saving_kg=saving
            ))
            
        if not suggestions:
            saving = current_emission * 0.02
            suggestions.append(OptimizationSuggestion(
                category="General",
                suggestion="Conduct a detailed energy audit.",
                potential_saving_kg=saving
            ))
            
        return suggestions
