import logging
from app.core.config import settings
from strands.models.gemini import GeminiModel

logger = logging.getLogger(__name__)


def get_model():
    provider = settings.MODEL_PROVIDER
    logger.info(f"[Model] Loading model for provider: '{provider}'")

    if provider == "gemini":
        if not settings.GEMINI_API_KEY:
            logger.error("[Model] ❌ GEMINI_API_KEY is not set in .env")
            raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")
        try:
            model = GeminiModel(
                client_args={"api_key": settings.GEMINI_API_KEY},
                model_id="gemini-2.5-flash"
            )
            logger.info("[Model] ✅ Gemini model (gemini-2.5-flash) loaded successfully")
            return model
        except Exception as e:
            logger.error(f"[Model] ❌ Failed to initialize Gemini model: {type(e).__name__}: {e}")
            raise

    raise ValueError(
        f"Unsupported MODEL_PROVIDER: '{provider}'. "
        "Supported values: 'gemini'"
    )