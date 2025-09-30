# backend/schemas/crypto.py
from pydantic import BaseModel
from datetime import date
from typing import List

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

# New lightweight point schema for chart data
class PricePoint(BaseModel):
    date: date
    value: float

class CryptoDashboardResponse(BaseModel):
    bitcoin: List[PricePoint]
    ethereum: List[PricePoint]