import logging
import time
import uuid
from dotenv import load_dotenv
import os

load_dotenv()
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Header, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import pandas as pd
import io

from agents.data_agent import DataCleaningAgent
from agents.prediction_agent import EmissionPredictionAgent
from agents.optimization_agent import OptimizationAgent
from agents.loop_agent import LoopAgent
from services.memory_service import InMemorySessionService, MemoryBank
from services.report_service import ReportService
from models.schemas import EmissionOutput, OptimizationResponse, OptimizationSuggestion

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CarbonAssistant")

app = FastAPI(title="Carbon Emission Intelligence Assistant")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services & Agents
session_service = InMemorySessionService()
memory_bank = MemoryBank()
data_agent = DataCleaningAgent()
prediction_agent = EmissionPredictionAgent()
optimization_agent = OptimizationAgent()
loop_agent = LoopAgent()
report_service = ReportService()

# Middleware for Observability
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(f"Request {request_id} started: {request.method} {request.url}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    logger.info(f"Request {request_id} completed in {process_time:.4f}s")
    return response

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), x_session_id: Optional[str] = Header(None)):
    if not x_session_id:
        x_session_id = session_service.create_session()
    
    session = session_service.get_session(x_session_id)
    if not session:
        x_session_id = session_service.create_session()
        session = session_service.get_session(x_session_id)

    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        logger.info(f"Uploaded CSV shape: {df.shape}")
        logger.info(f"Uploaded CSV columns: {df.columns.tolist()}")
        logger.info(f"First row: {df.iloc[0].to_dict()}")
        
        # Agent: Data Cleaning
        cleaned_df = data_agent.clean(df)
        logger.info(f"Cleaned data shape: {cleaned_df.shape}")
        
        # Convert to dict for storage (simplified)
        data_dict = cleaned_df.iloc[0].to_dict() # Assuming single row for this demo or we process first row
        logger.info(f"Stored data: {data_dict}")
        
        session_service.update_session(x_session_id, "data", data_dict)
        session_service.update_session(x_session_id, "data_uploaded", True)
        
        return {
            "message": "File uploaded and processed successfully", 
            "session_id": x_session_id,
            "preview": data_dict
        }
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict", response_model=EmissionOutput)
async def predict(x_session_id: str = Header(...)):
    session = session_service.get_session(x_session_id)
    if not session or not session.get("data"):
        raise HTTPException(status_code=400, detail="No data found in session")
    
    data = session["data"]
    
    # Agent: Prediction
    # We need to convert data dict back to DataFrame for the agent
    df = pd.DataFrame([data])
    
    # Ensure columns match what the model expects (basic check)
    # The model was trained on: energy_usage_kwh, fuel_consumption_liters, distance_traveled_km, waste_generated_kg, company_size
    # We assume the CSV has these.
    
    try:
        logger.info(f"Prediction data from session: {data}")
        
        # Agent: Prediction
        # We need to convert data dict back to DataFrame for the agent
        df = pd.DataFrame([data])
        logger.info(f"DataFrame for prediction:\n{df}")
        logger.info(f"DataFrame dtypes:\n{df.dtypes}")
        
        emission_value = prediction_agent.predict(df)
        logger.info(f"Predicted emission: {emission_value}")
        
        explanation = prediction_agent.explain(data, emission_value)
        
        output = EmissionOutput(emission_kg=emission_value, explanation=explanation)
        
        session_service.update_session(x_session_id, "prediction", output)
        session_service.update_session(x_session_id, "prediction_made", True)
        
        # Save to long-term memory
        memory_bank.save_emission_record({
            "session_id": x_session_id,
            "input": data,
            "emission": emission_value
        })
        
        return output
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize", response_model=OptimizationResponse)
async def optimize(background_tasks: BackgroundTasks, x_session_id: str = Header(...)):
    session = session_service.get_session(x_session_id)
    if not session or not session.get("prediction"):
        raise HTTPException(status_code=400, detail="No prediction found. Run prediction first.")
    
    data = session["data"]
    prediction = session["prediction"] # This is an EmissionOutput object or dict
    
    # If it's stored as object, pydantic might have serialized it or not. 
    # InMemorySession stores objects.
    current_emission = prediction.emission_kg
    
    # Agent: Optimization (Parallel/Background?)
    # The requirement says "Optimization Suggestion Agent (parallel) Runs in parallel with prediction".
    # But here we expose it as a separate endpoint. 
    # To demonstrate "parallel", we could trigger it in /predict and retrieve here, 
    # OR we just run it here. The user flow usually waits for prediction then asks for optimization.
    # I'll run it here synchronously for the response, but maybe log or do heavy lifting in background if it was complex.
    
    suggestions = optimization_agent.optimize(data, current_emission)
    total_savings = sum(s.potential_saving_kg for s in suggestions)
    
    response = OptimizationResponse(suggestions=suggestions, total_potential_savings=total_savings)
    
    session_service.update_session(x_session_id, "optimization", response)
    session_service.update_session(x_session_id, "optimization_done", True)
    
    return response

@app.post("/generate-report")
async def generate_report(x_session_id: str = Header(...)):
    session = session_service.get_session(x_session_id)
    
    # Loop Agent check
    status = loop_agent.check_readiness(session)
    if not status["ready"]:
        # In a real agent loop, we would ask the user. Here we return 400 with the message.
        # Or we could just proceed if we have enough data.
        # Let's enforce the check.
        if "prediction" not in session or "optimization" not in session:
             raise HTTPException(status_code=400, detail=status["message"])
    
    prediction = session["prediction"]
    optimization = session["optimization"]
    
    pdf_bytes = report_service.generate_pdf("My Company", prediction, optimization)
    
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})

@app.get("/health")
def health():
    return {"status": "ok"}
