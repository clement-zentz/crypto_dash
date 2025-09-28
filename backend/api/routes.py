# backend/api/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from db import models
from db.database import get_db
from schemas.crypto import CryptoPriceRead

router = APIRouter()

@router.get("/crypto/", response_model=List[CryptoPriceRead])
def get_crypto(
    symbol: Optional[str] = None, 
    db : Session = Depends(get_db)
):
    query = db.query(models.CryptoPrice)
    if symbol:
        query = query.filter(
            models.CryptoPrice.symbol == symbol.upper()
        )
    return query.all()