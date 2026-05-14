from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

from app.retriever import retrieve_assessments
from app.llm import generate_reply
from app.prompts import SYSTEM_PROMPT
from app.guardrails import is_off_topic

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
# Helper Functions
# -----------------------------
def get_latest_user_message(messages):
    for message in reversed(messages):
        if message.role == "user":
            return message.content
    return ""


def build_conversation(messages):
    return "\n".join(
        [f"{m.role}: {m.content}" for m in messages]
    )


def needs_clarification(user_message):
    vague_keywords = [
        "assessment",
        "test",
        "hiring",
        "developer",
        "engineer",
        "role"
    ]

    if len(user_message.split()) < 5:
        return True

    if any(word in user_message.lower() for word in vague_keywords):
        if len(user_message.split()) < 10:
            return True

    return False


def generate_clarification_question():
    return (
        "Could you share more details about the role, "
        "seniority level, required technical skills, "
        "and whether you also want personality or "
        "behavioral assessments?"
    )


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages

    latest_user_message = get_latest_user_message(messages)

    # -----------------------------
    # Off-topic Protection
    # -----------------------------
    if is_off_topic(latest_user_message):
        return {
            "reply": (
                "I can only help with SHL assessment "
                "recommendations and comparisons."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Clarification Logic
    # -----------------------------
    if needs_clarification(latest_user_message):
        return {
            "reply": generate_clarification_question(),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Retrieval
    # -----------------------------
    retrieved = retrieve_assessments(
        latest_user_message,
        top_k=5
    )

    # -----------------------------
    # Catalog Context
    # -----------------------------
    catalog_context = "\n\n".join([
        f"""
        Name: {r['name']}
        Description: {r['description']}
        URL: {r['url']}
        Type: {r.get('test_type', 'Unknown')}
        """
        for r in retrieved
    ])

    # -----------------------------
    # Conversation History
    # -----------------------------
    conversation = build_conversation(messages)

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
    {SYSTEM_PROMPT}

    Conversation History:
    {conversation}

    SHL Catalog Context:
    {catalog_context}

    Instructions:
    - Recommend ONLY assessments from catalog
    - Never hallucinate assessments
    - Be concise and recruiter-friendly
    - Explain recommendations briefly
    - If comparing assessments, use catalog context only
    """

    # -----------------------------
    # LLM Generation
    # -----------------------------
    reply = generate_reply(prompt)

    # -----------------------------
    # Structured Recommendations
    # -----------------------------
    recommendations = []

    for item in retrieved:
        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item.get(
                "test_type",
                "Unknown"
            )
        })

    # -----------------------------
    # Final Response
    # -----------------------------
    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": True
    }