# backend/db/models.py
from sqlalchemy import Column, Integer, String, Float, Date
from db.database import Base

class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    date = Column(Date, index=True)
    value = Column(Float)