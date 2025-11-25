from typing import Dict, Any

class LoopAgent:
    def __init__(self):
        pass

    def check_readiness(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks if the user is ready to generate a report.
        Returns a status and a message/question.
        """
        if not session_state.get("data_uploaded"):
            return {"ready": False, "message": "Please upload your CSV data first."}
        
        if not session_state.get("prediction_made"):
            return {"ready": False, "message": "We haven't calculated your emissions yet. Shall we proceed to prediction?"}
        
        if not session_state.get("optimization_done"):
            return {"ready": False, "message": "We have optimization suggestions available. Would you like to view them before generating the report?"}
        
        if not session_state.get("user_confirmed_report"):
             return {"ready": False, "message": "Are you ready to generate the final sustainability report?"}

        return {"ready": True, "message": "Generating report..."}

    def process_user_response(self, session_state: Dict[str, Any], response: str) -> Dict[str, Any]:
        # Simple logic to handle confirmation
        if response.lower() in ["yes", "y", "confirm", "generate"]:
            session_state["user_confirmed_report"] = True
            return {"confirmed": True, "message": "Confirmed. Proceeding to report generation."}
        else:
            return {"confirmed": False, "message": "Okay, let me know when you are ready."}
