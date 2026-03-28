from pymongo import MongoClient
from app.core.config import settings

client = MongoClient("mongodb://localhost:27017")

db = client["crypto_ai"]

reports_collection = db["reports"]