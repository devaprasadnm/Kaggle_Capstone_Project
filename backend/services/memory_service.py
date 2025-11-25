from typing import Dict, Any, Optional
import uuid

class InMemorySessionService:
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "history": [],
            "data": None,
            "prediction": None,
            "optimization": None
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._sessions.get(session_id)

    def update_session(self, session_id: str, key: str, value: Any):
        if session_id in self._sessions:
            self._sessions[session_id][key] = value

class MemoryBank:
    def __init__(self):
        self._store: Dict[str, Any] = {
            "company_profiles": {},
            "past_emissions": []
        }

    def save_profile(self, company_name: str, profile: Dict):
        self._store["company_profiles"][company_name] = profile

    def save_emission_record(self, record: Dict):
        self._store["past_emissions"].append(record)
        
    def get_stats(self):
        return {
            "total_records": len(self._store["past_emissions"]),
            "companies": list(self._store["company_profiles"].keys())
        }
