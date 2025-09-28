# backend/schemas/crypto.py
from pydantic import BaseModel
from datetime import date

class CryptoPriceBase(BaseModel):
    symbol : str
    date : date
    value : float

class CryptoPriceCreate(CryptoPriceBase):
    pass

class CryptoPriceRead(CryptoPriceBase):
    id : int

    class Config:
        from_attributes = True