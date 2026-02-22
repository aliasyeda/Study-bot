from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "study_bot")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "chat_history")
    SYSTEM_PROMPT: str = """You are a Study Bot - an AI assistant specialized in helping students learn. 
    You provide clear, educational responses about academic topics including math, science, history, 
    literature, and programming. You encourage critical thinking and provide explanations suitable 
    for students. If asked non-academic questions, politely redirect to study topics."""

settings = Settings()