from app.core.config import settings
from strands.models.gemini import GeminiModel
from strands.models.ollama import OllamaModel


def get_model():
    if settings.MODEL_PROVIDER == "gemini":
        return GeminiModel(
            client_args={"api_key": settings.GEMINI_API_KEY},
            model_id="gemini-2.5-flash"
        )

    return OllamaModel(
        host=settings.OLLAMA_HOST,
        model_id="ministral-3:3b"
    )