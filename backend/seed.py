# backend/seed.py
from db.database import SessionLocal
from db.models import CryptoPrice
from datetime import date, timedelta
import random

db = SessionLocal()

db.query(CryptoPrice).delete()

symbols = ["BTC", "ETH"]
for symbol in symbols:
    for i in range(7):
        db.add(CryptoPrice(
            symbol=symbol,
            date=date.today() - timedelta(days=i),
            value=round(random.uniform(20000, 30000), 2) if symbol == "BTC"
            else round(random.uniform(1500, 2500), 2)
        ))

db.commit()
db.close()

print("✅ Insert test data")