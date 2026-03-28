from fastapi import APIRouter
from app.schemas.request import CryptoRequest
from app.agents.coordinator import run_analysis_async
from app.services.report_service import ReportService

router = APIRouter()


@router.post("/analyze")
async def analyze_crypto(request: CryptoRequest):
    return await run_analysis_async(request.crypto)

@router.get("/reports/{crypto}")
def get_reports(crypto: str):
    return ReportService.get_reports_by_crypto(crypto)

@router.get("/reports/{crypto}/latest")
def get_latest_report(crypto: str):
    return ReportService.get_latest_report(crypto)