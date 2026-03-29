import logging
import datetime
from app.core.db import reports_collection

logger = logging.getLogger(__name__)


class ReportService:

    @staticmethod
    def save_report(crypto: str, result: dict):
        """
        Store analysis result in MongoDB
        """
        logger.info(f"[MongoDB] Saving report for {crypto}...")
        try:
            document = {
                "crypto": crypto,
                "news": result.get("news"),
                "sentiment": result.get("sentiment"),
                "price": result.get("price"),
                "risk": result.get("risk"),
                "report": result.get("report"),
                "critique": result.get("critique"),
                "created_at": datetime.datetime.utcnow()
            }
            reports_collection.insert_one(document)
            logger.info(f"[MongoDB] ✅ Report saved for {crypto}")
        except Exception as e:
            logger.error(f"[MongoDB] ❌ Failed to save report for {crypto}: {e}")
            raise


    @staticmethod
    def get_reports_by_crypto(crypto: str):
        """
        Fetch all reports for a crypto
        """

        docs = list(
            reports_collection.find(
                {"crypto": crypto}
            ).sort("created_at", -1)
        )
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs


    @staticmethod
    def get_latest_report(crypto: str):
        """
        Get latest report
        """

        doc = reports_collection.find_one(
            {"crypto": crypto},
            sort=[("created_at", -1)]
        )
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc