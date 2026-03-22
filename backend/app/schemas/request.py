from pydantic import BaseModel

class CryptoRequest(BaseModel):
    crypto: str