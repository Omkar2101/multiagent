from pymongo import MongoClient

# Create connection
client = MongoClient("mongodb://localhost:27017")

# Database
db = client["crypto_ai"]

# Collections
reports_collection = db["reports"]