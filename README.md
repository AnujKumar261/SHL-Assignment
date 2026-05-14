📌 SHL Agent – FastAPI Backend for Skill Assessment Queries

🚀 Overview

This project is a FastAPI-based intelligent retrieval and chat system designed to answer queries related to SHL assessments and catalog data.
It uses a combination of retrieval (FAISS/vector search) and LLM-based response generation to provide accurate and contextual answers.

📂 Project Structure
SHL-Agent/
│
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── llm.py               # LLM integration logic
│   ├── retriever.py        # Vector search / FAISS retrieval
│   ├── prompts.py          # Prompt templates
│   ├── guardrails.py       # Safety & validation rules
│   ├── scraper.py          # Data scraping utilities
│   ├── catalog_loader.py   # Loads SHL dataset
│
├── data/
│   ├── shl_catalog.json
│   ├── embeddings.npy
│   ├── faiss.index
│
├── approach_document.md    # Design & methodology document
├── requirements.txt        # Python dependencies
├── render.yaml             # Deployment config (Render)
├── .gitignore              # Ignored files
⚙️ Features
🔍 Semantic search using embeddings + FAISS
🤖 LLM-powered conversational responses
🧠 Context-aware prompt engineering
🛡️ Guardrails for safe and structured outputs
⚡ FastAPI-based lightweight backend
📦 Ready for cloud deployment (Render / similar)
🔗 API Endpoints
1. Health Check
GET /health

Response:

{
  "status": "ok"
}
2. Chat Endpoint
POST /chat

Request Body:

{
  "message": "What SHL tests are available for Java developers?"
}

Response:

{
  "response": "Here are relevant SHL assessments..."
}
🧠 System Design
1. Retrieval Layer
Uses SHL catalog dataset
Converts text into embeddings
Stores vectors in FAISS index
Retrieves top-k similar matches
2. LLM Layer
Combines user query + retrieved context
Uses structured prompt templates
Generates final response via LLM
3. Guardrails
Filters irrelevant outputs
Ensures response consistency
Prevents hallucinated results
🧪 Evaluation Strategy
Manual test queries across domains
Checked relevance of retrieved results
Validated response coherence
Iteratively improved prompt design
⚠️ Known Limitations
Retrieval depends on dataset quality
Edge-case queries may return partial matches
Latency depends on embedding + LLM call time
🛠️ Tech Stack
Python 3.10+
FastAPI
FAISS (vector search)
NumPy
OpenAI / LLM API
Uvicorn
🚀 Deployment

This project is deployment-ready using Render.

Run locally:
pip install -r requirements.txt
uvicorn app.main:app --reload
🌐 Live API (after deployment)
https://your-deployed-url.onrender.com


Built as part of SHL assignment submission.

📌 Notes
.env is excluded for security
Large files like embeddings/index are stored in /data
Ensure /health and /chat are live before submission
