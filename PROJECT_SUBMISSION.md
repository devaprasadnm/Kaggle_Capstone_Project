# Carbon Intelligence Assistant: Project Submission

## 1. Project Overview
The **Carbon Intelligence Assistant** is an advanced, multi-agent AI system designed to help organizations measure, understand, and reduce their carbon footprint. Unlike traditional calculators that simply output a number, this system uses **Agentic AI** to act as a virtual sustainability team—analyzing data, explaining complex results in plain English, and brainstorming tailored optimization strategies.

## 2. Key Features & Agentic Concepts
This project demonstrates the application of advanced Agentic AI concepts, specifically addressing the following course requirements:

### A. Multi-Agent System
The application is built upon a sequential multi-agent architecture where specialized agents collaborate to solve the user's problem:
1.  **Data Cleaning Agent (Rule-Based)**: Acts as a Data Engineer. It ingests raw, messy CSV files, maps inconsistent column names to a standardized schema, and handles missing values.
2.  **Emission Prediction Agent (Hybrid: ML + LLM)**: Acts as a Data Scientist. It uses a Random Forest model to predict precise emission values and **Google Gemini** to analyze the input factors and explain *why* the emissions are high (e.g., "High fuel consumption in logistics").
3.  **Optimization Agent (Generative)**: Acts as a Sustainability Consultant. It uses **Google Gemini** to generate creative, context-aware reduction strategies (e.g., "Switch to EVs", "Install LED lighting") based on the specific company profile.
4.  **Loop Agent (Orchestrator)**: Acts as a Project Manager. It implements a "Human-in-the-loop" workflow, ensuring the user has completed all necessary analysis steps (Upload -> Predict -> Optimize) before allowing the final report generation.

### B. Tools & Integrations
The agents are equipped with powerful tools to extend their capabilities:
*   **Google Gemini API (LLM)**: Used by the Prediction and Optimization agents for reasoning and natural language generation.
*   **Scikit-Learn (ML)**: A custom-trained Random Forest Regressor used for numerical precision.
*   **ReportLab**: A tool used by the Report Service to compile dynamic PDF documents.
*   **Environment Management**: Uses `python-dotenv` for secure API key management.

### C. State Management & Memory
*   **Session Memory (`InMemorySessionService`)**: The system maintains a stateful conversation with the user. It remembers the uploaded data, the prediction result, and the generated suggestions across different API calls.
*   **Long-Term Memory (`MemoryBank`)**: Stores historical emission records, allowing for future trend analysis and benchmarking.

### D. Observability
*   **Logging & Tracing**: Every request is tagged with a unique `Request-ID` and logged with execution time. The system logs the input shape, agent decisions, and any errors, providing full visibility into the agent's thought process.

## 3. Technical Architecture

### Backend (FastAPI)
*   **Framework**: FastAPI for high-performance, async API endpoints.
*   **Design Pattern**: Service-Repository pattern with clear separation of concerns between Agents, Services, and Models.
*   **Deployment**: Containerized using **Docker** for easy deployment to cloud platforms.

### Frontend (React)
*   **Framework**: React with Vite for a fast, modern user experience.
*   **Styling**: Tailwind CSS for a premium, responsive design.
*   **Visualization**: Recharts for displaying emission data visually.

## 4. How to Run

### Prerequisites
*   Docker (optional) OR Python 3.9+ and Node.js 16+
*   Google API Key (for Gemini features)

### Quick Start (Local)
1.  **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    # Create .env file with GOOGLE_API_KEY=your_key
    uvicorn main:app --reload
    ```
2.  **Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## 5. Conclusion
The Carbon Intelligence Assistant moves beyond simple automation. By integrating **LLMs** for reasoning and **ML** for precision, wrapped in a **Multi-Agent** framework, it provides a truly intelligent tool that empowers users to take actionable steps towards sustainability.
