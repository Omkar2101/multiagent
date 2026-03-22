from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Crypto Multi-Agent System")

app.include_router(router)