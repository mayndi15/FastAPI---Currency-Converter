from fastapi import HTTPException
from os import getenv
import requests
import aiohttp

apikey = getenv('ALPHAVANTAGE_APIKEY')

def sync_converter(from_currency:str, to_currency:str, price:float):
    external_url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={apikey}'

    try:
        response = requests.get(url=external_url)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=ex)
    
    data = response.json()

    if("Realtime Currency Exchange Rate" not in data):  
        raise HTTPException(status_code=400, detail="Realtime Currency Exchange Rate not in response")

    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])

    return price * exchange_rate

async def async_converter(from_currency:str, to_currency:str, price:float):
    external_url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={apikey}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=external_url) as response:
                data = await response.json()
    except Exception as ex:
        raise HTTPException(status_code=400, detail=ex)
    
    if("Realtime Currency Exchange Rate" not in data):  
        raise HTTPException(status_code=400, detail="Realtime Currency Exchange Rate not in response")

    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])

    return price * exchange_rate