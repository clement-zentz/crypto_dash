# backend/api/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from db import models
from db.database import get_db
from schemas.crypto import CryptoDashboardResponse

router = APIRouter()

@router.get("/crypto/", response_model=CryptoDashboardResponse)
def get_crypto(
    symbol: Optional[str] = None, 
    db : Session = Depends(get_db)
):
    """
    Return time-series price data for BTC and ETH (or a single symbol if provided).
    """
    query = db.query(models.CryptoPrice)
    if symbol:
        symbol = symbol.upper()
        query = query.filter(models.CryptoPrice.symbol == symbol)
    else:
        query = query.filter(models.CryptoPrice.symbol.in_(["BTC", "ETH"]))

    rows = query.all()

    bitcoin = [{"date": r.date, "value": r.value} for r in rows if r.symbol == "BTC"]
    ethereum = [{"date": r.date, "value": r.value} for r in rows if r.symbol == "ETH"]

    return {
        "bitcoin": sorted(bitcoin, key=lambda x: x["date"]),
        "ethereum": sorted(ethereum, key=lambda x: x["date"])
    }