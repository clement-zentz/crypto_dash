# backend/api/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.db import models
from backend.db.database import get_db
from backend.schemas.crypto import CryptoDashboardResponse
from backend.services.coingecko import fetch_multiple, upsert_prices

router = APIRouter()

@router.get("/crypto/", response_model=CryptoDashboardResponse)
async def get_crypto(
    symbol: Optional[str] = None, 
    refresh: bool = False,
    days: int = 7,
    db : Session = Depends(get_db)
):
    """
    Return time-series price data for BTC and ETH (or a single symbol if provided).
    """
    # Rafraîchir si demandé ou si base vide
    if refresh or db.query(models.CryptoPrice).count() == 0:
        pairs = []
        if symbol:
            s = symbol.upper()
            if s == "BTC":
                pairs.append(("bitcoin", "BTC"))
            elif s == "ETH":
                pairs.append(("ethereum", "ETH"))
        else:
            pairs = [("bitcoin", "BTC"), ("ethereum", "ETH")]
        data = await fetch_multiple(pairs, days=days)
        upsert_prices(db, data)

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