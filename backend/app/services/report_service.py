from app.core.db import reports_collection
import datetime


class ReportService:

    @staticmethod
    def save_report(crypto: str, result: dict):
        """
        Store analysis result in MongoDB
        """

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


    @staticmethod
    def get_reports_by_crypto(crypto: str):
        """
        Fetch all reports for a crypto
        """

        return list(
            reports_collection.find(
                {"crypto": crypto}
            ).sort("created_at", -1)
        )


    @staticmethod
    def get_latest_report(crypto: str):
        """
        Get latest report
        """

        return reports_collection.find_one(
            {"crypto": crypto},
            sort=[("created_at", -1)]
        )