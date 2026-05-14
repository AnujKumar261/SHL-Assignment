# 🚀 SHL Agent – FastAPI Backend

SHL Agent is a FastAPI-based backend system designed to intelligently answer queries related to SHL assessments. It uses a combination of semantic search (FAISS-based vector retrieval) and large language models to generate accurate, context-aware responses.

The system first processes user queries by converting them into embeddings and retrieving the most relevant information from a pre-built SHL catalog dataset. This retrieved context is then passed to an LLM, which generates a final response in a structured and meaningful way.

The project also includes guardrails to ensure response quality and consistency, along with a lightweight and scalable FastAPI architecture that makes it easy to deploy on cloud platforms like Render.

## Features
- Semantic search using FAISS vector database  
- LLM-powered response generation  
- Context-aware retrieval system (RAG approach)  
- FastAPI backend for high performance  
- Deployment-ready architecture  

## API Endpoints
- `/health` → Returns API status  
- `/chat` → Accepts user query and returns intelligent response  

## Tech Stack
Python, FastAPI, FAISS, NumPy, LLM API, Uvicorn

## Deployment
The project is ready for deployment using Render or any cloud platform that supports Python FastAPI applications.

## Status
Backend is fully functional with retrieval and LLM integration completed and ready for submission.
