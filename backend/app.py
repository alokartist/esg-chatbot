import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.utils import get_sqlite_connection
from backend.llm import ask_llm

# Load environment variables
load_dotenv("backend/.env")

DB_PATH = os.getenv("ESG_DB_PATH")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set. Fill backend/.env")

# Initialize FastAPI app
app = FastAPI(title="ESG Data Chatbot API")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
try:
    conn = get_sqlite_connection(DB_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to connect to database: {e}")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "ESG Chatbot API is running"}


@app.post("/api/chat")
def chat(request: QuestionRequest):
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # 🔹 Pass both question & DB connection to the LLM
        answer = ask_llm(request.question)

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")
