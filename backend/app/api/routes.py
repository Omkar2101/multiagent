from fastapi import APIRouter
from app.schemas.request import CryptoRequest
from app.agents.coordinator import run_analysis

router = APIRouter()


@router.post("/analyze")
def analyze_crypto(request: CryptoRequest):
    result = run_analysis(request.crypto)
    return result