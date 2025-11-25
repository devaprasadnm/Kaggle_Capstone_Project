# Carbon Intelligence Assistant: Agentic Architecture

This document explains the "Agentic AI" components working behind the scenes of the Carbon Intelligence Assistant.

## 1. Multi-Agent System Architecture
The system is composed of specialized agents, each with a distinct role. They work together in a **Sequential Workflow** orchestrated by the FastAPI backend (`main.py`).

### 🤖 The Agents

#### A. Data Cleaning Agent (`agents/data_agent.py`)
*   **Role**: The "Data Engineer".
*   **Task**: Takes raw, messy CSV uploads and transforms them into a structured format that the other agents can understand.
*   **Logic**: Uses `pandas` to map column names (e.g., mapping "fuel_used" to "fuel_consumption_liters") and handle missing values.
*   **Type**: Rule-based Agent.

#### B. Emission Prediction Agent (`agents/prediction_agent.py`)
*   **Role**: The "Data Scientist" & "Analyst".
*   **Task**: 
    1.  Predicts the carbon emission value using a Machine Learning model (`random_forest`).
    2.  Explains *why* the emission is high or low.
*   **Agentic Feature**: **LLM-Powered Reasoning**.
    *   It uses **Google Gemini** to analyze the input data and the prediction result.
    *   It generates a natural language explanation (e.g., "High emissions are driven by excessive fuel consumption in your logistics fleet").

#### C. Optimization Agent (`agents/optimization_agent.py`)
*   **Role**: The "Sustainability Consultant".
*   **Task**: Suggests actionable strategies to reduce emissions.
*   **Agentic Feature**: **Generative Planning**.
    *   It uses **Google Gemini** to act as a consultant.
    *   It receives the company's specific data profile and generates tailored advice (e.g., "Switch to EVs", "Install Solar Panels").
    *   It outputs structured JSON data that the frontend can render as cards.

#### D. Loop Agent (`agents/loop_agent.py`)
*   **Role**: The "Project Manager".
*   **Task**: Monitors the state of the user's session.
*   **Logic**: Checks if the user has completed necessary steps (Upload -> Predict -> Optimize) before allowing them to generate the final report. This implements a **Human-in-the-loop** pattern.

## 2. Tools & Capabilities
The agents are equipped with specific tools to perform their tasks:
*   **Machine Learning Model**: A pre-trained `scikit-learn` model for numerical prediction.
*   **LLM (Google Gemini)**: Used for reasoning, explanation, and idea generation.
*   **Memory**:
    *   **Short-term Memory (Session)**: Stores the current file, prediction, and suggestions in RAM (`InMemorySessionService`).
    *   **Long-term Memory (Memory Bank)**: Saves historical records of emissions for future analysis.

## 3. The Workflow (Behind the Scenes)

1.  **User Uploads File** -> `DataCleaningAgent` standardizes it. -> **Memory** stores the clean data.
2.  **User Clicks "Predict"** -> `PredictionAgent` runs the ML model AND calls Gemini to explain the result. -> **Memory** stores the result.
3.  **User Clicks "Optimize"** -> `OptimizationAgent` sends data to Gemini to brainstorm solutions. -> **Memory** stores suggestions.
4.  **User Clicks "Report"** -> `LoopAgent` verifies everything is ready. -> `ReportService` compiles a PDF.

## 4. Why is this "Agentic"?
Unlike a standard script that just runs A -> B -> C, these agents:
*   **Perceive**: They look at the data (Context).
*   **Decide**: The Loop Agent decides if the process can proceed.
*   **Act**: They generate new content (Explanations, Suggestions) dynamically using an LLM, rather than just pulling from a static database.
