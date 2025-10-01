# backend/services/coingecko.py
import httpx, logging, asyncio
from datetime import datetime, timezone
from backend.db.models import CryptoPrice
from typing import List, Dict, Optional, Iterable
from sqlalchemy.orm import Session

COINGECKO_URL = "https://api.coingecko.com/api/v3"
logger = logging.getLogger(__name__)

async def fetch_crypto_data(coin_id: str, days: int = 7, vs_currency: str = "usd", 
symbol: Optional[str] = None, client: Optional[httpx.AsyncClient] = None) -> List[Dict]:
    """Get price data (market_chart) from CoinGecko 
    and send a normalize list: [{symbol, data, value, ...}].

    Args:
        coin_id (str): _description_
        days (int, optional): _description_. Defaults to 7.
        vs_currency (str, optional): _description_. Defaults to "usd".
        symbol (Optional[str], optional): _description_. Defaults to None.
        client (Optional[httpx.AsyncClient], optional): _description_. Defaults to None.

    Returns:
        List[Dict]: _description_
    """
    symbol = symbol or coin_id.upper()
    url = f"{COINGECKO_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}

    own_client = client is None
    if own_client:
        client = httpx.AsyncClient(timeout=10)

    try:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()
    except httpx.HTTPError as e:
        logger.error("Error CoinGecko (%s): %s", coin_id, e)
        return []
    finally:
        if own_client and client:
            await client.aclose()

    prices_raw = payload.get("prices", [])
    results: List[Dict] = []
    seen_dates = set()

    for ts_ms, price in prices_raw:
        dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).date()
        if dt in seen_dates:
            continue
        seen_dates.add(dt)
        results.append({
            "symbol": symbol,
            "date": dt,
            "value": float(price)
        })

    results.sort(key=lambda x: x["date"])
    return results

async def fetch_multiple(pairs: Iterable[tuple[str, str]], days: int = 7) -> List[Dict]:
    """pairs = [(coin_id, symbol)]"""
    out: List[Dict] = []
    async with httpx.AsyncClient(timeout=10) as client:
        coros = [fetch_crypto_data(c, days=days, symbol=s, client=client) for c, s in pairs]
        results = await asyncio.gather(*coros, return_exceptions=False)
    for chunk in results:
        out.extend(chunk)
    return out

def upsert_prices(db: Session, data: List[Dict]) -> None:
    """Remplace (symbol,date) existants puis insère."""
    if not data:
        return
    # Regrouper par symbol/date
    for row in data:
        db.query(CryptoPrice).filter(
            CryptoPrice.symbol == row["symbol"],
            CryptoPrice.date == row["date"]
        ).delete()
        db.add(CryptoPrice(symbol=row["symbol"], date=row["date"], value=row["value"]))
    db.commit()