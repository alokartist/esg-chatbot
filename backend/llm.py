# backend/llm.py

import os
from dotenv import load_dotenv
from groq import Groq

# Load .env from the backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set. Please add it to backend/.env")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def ask_llm(question: str) -> str:
    """
    Ask Groq Cloud LLM a question and return the response.
    """
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  # You can switch to "mixtral-8x7b" etc.
            messages=[
                {"role": "system", "content": "You are an ESG chatbot that answers clearly and concisely."},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM error: {str(e)}"
