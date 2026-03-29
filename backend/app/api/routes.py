import logging
from fastapi import APIRouter, HTTPException
from app.schemas.request import CryptoRequest
from app.agents.coordinator import run_analysis_async
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze")
async def analyze_crypto(request: CryptoRequest):
    logger.info(f"[Routes] POST /analyze — crypto={request.crypto}")
    try:
        result = await run_analysis_async(request.crypto)
        logger.info(f"[Routes] ✅ Analysis complete for {request.crypto}")
        return result
    except RuntimeError as e:
        logger.error(f"[Routes] ❌ Analysis failed for {request.crypto}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"[Routes] ❌ Unexpected error for {request.crypto}: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@router.get("/reports/{crypto}")
def get_reports(crypto: str):
    logger.info(f"[Routes] GET /reports/{crypto}")
    try:
        reports = ReportService.get_reports_by_crypto(crypto)
        logger.info(f"[Routes] ✅ Returning {len(reports)} reports for {crypto}")
        return reports
    except Exception as e:
        logger.error(f"[Routes] ❌ Failed to fetch reports for {crypto}: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {e}")


@router.get("/reports/{crypto}/latest")
def get_latest_report(crypto: str):
    logger.info(f"[Routes] GET /reports/{crypto}/latest")
    try:
        report = ReportService.get_latest_report(crypto)
        if report is None:
            logger.warning(f"[Routes] No report found for {crypto}")
            raise HTTPException(status_code=404, detail=f"No report found for '{crypto}'")
        logger.info(f"[Routes] ✅ Returning latest report for {crypto}")
        return report
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Routes] ❌ Failed to fetch latest report for {crypto}: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch latest report: {e}")