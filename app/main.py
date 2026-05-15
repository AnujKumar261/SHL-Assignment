from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# -----------------------------
# Request Schema
# -----------------------------
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# Health Endpoint
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Safe fallback functions
# -----------------------------
def get_latest_user_message(messages):
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return ""


def needs_clarification(user_message: str) -> bool:
    if not user_message:
        return True
    if len(user_message.split()) < 5:
        return True
    return False


def generate_clarification_question():
    return (
        "Could you share more details about the role, "
        "skills required, and seniority level?"
    )


# -----------------------------
# Chat Endpoint (SAFE VERSION)
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    try:
        messages = request.messages
        latest_user_message = get_latest_user_message(messages)

        # -----------------------------
        # Simple clarification logic
        # -----------------------------
        if needs_clarification(latest_user_message):
            return {
                "reply": generate_clarification_question(),
                "recommendations": [],
                "end_of_conversation": False
            }

        # -----------------------------
        # Lazy import (IMPORTANT FIX)
        # -----------------------------
        try:
            from app.retriever import retrieve_assessments
            from app.llm import generate_reply
            from app.guardrails import is_off_topic
        except Exception:
            return {
                "reply": "System is initializing. Please try again shortly.",
                "recommendations": [],
                "end_of_conversation": False
            }

        # -----------------------------
        # Off-topic check
        # -----------------------------
        if is_off_topic(latest_user_message):
            return {
                "reply": "I can only help with SHL assessment recommendations.",
                "recommendations": [],
                "end_of_conversation": False
            }

        # -----------------------------
        # Retrieval (safe wrapper)
        # -----------------------------
        try:
            retrieved = retrieve_assessments(latest_user_message, top_k=5)
        except Exception:
            retrieved = []

        catalog_context = "\n\n".join([
            f"Name: {r.get('name','')}\n"
            f"Description: {r.get('description','')}\n"
            f"URL: {r.get('url','')}\n"
            f"Type: {r.get('test_type','Unknown')}"
            for r in retrieved
        ])

        # -----------------------------
        # Prompt
        # -----------------------------
        prompt = f"""
You are an SHL assessment assistant.

User Query:
{latest_user_message}

Context:
{catalog_context}

Rules:
- Recommend only from provided context
- Be concise and recruiter-friendly
"""

        # -----------------------------
        # LLM call (safe wrapper)
        # -----------------------------
        try:
            reply = generate_reply(prompt)
        except Exception:
            reply = "Unable to generate response at the moment."

        # -----------------------------
        # Recommendations
        # -----------------------------
        recommendations = []
        for item in retrieved:
            recommendations.append({
                "name": item.get("name"),
                "url": item.get("url"),
                "test_type": item.get("test_type", "Unknown")
            })

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    except Exception as e:
        return {
            "reply": f"Server error: {str(e)}",
            "recommendations": [],
            "end_of_conversation": False
        }