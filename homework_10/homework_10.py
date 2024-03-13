import time
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

ALPHAVANTAGE_API_KEY = "QO1H0O59FMXBAA24"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

cached_rate = None
last_cache_time = 0


def fetch_exchange_rate(source_currency: str, destination_currency: str):
    global cached_rate, last_cache_time

    if time.time() - last_cache_time < 10 and cached_rate:
        return cached_rate

    url = ("https://www.alphavantage.co/query?"
           f"function=CURRENCY_EXCHANGE_RATE"
           f"&from_currency={source_currency}"
           f"&to_currency={destination_currency}"
           f"&apikey={ALPHAVANTAGE_API_KEY}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        rate = response.json()["Realtime Currency Exchange Rate"][
            "5. Exchange Rate"
            ]
        cached_rate = rate
        last_cache_time = time.time()
        return rate
    except (requests.RequestException, KeyError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch exchange rate: {str(e)}"
            )


@app.post("/exchange-rate")
async def get_current_market_rate(
    source_currency: str,
    destination_currency: str
):
    rate = fetch_exchange_rate(source_currency, destination_currency)
    return {"rate": rate}
