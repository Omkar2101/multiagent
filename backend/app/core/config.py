import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST")
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")

settings = Settings()