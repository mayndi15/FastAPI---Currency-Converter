from asyncio import gather
from fastapi import APIRouter, Path, Query
import converter 

router = APIRouter(prefix='/converter')

@router.get('/sync/{from_currency}')
def sync_converter(from_currency:str = Path(max_length=3, regex='^[A-Z]{3}$'), 
                   to_currencies:str = Query(max_length=50, regex='^[A-Z]{3}(,[A-Z]{3})*$'), 
                   price:float = Query(gt=0)):
    
    to_currencies = to_currencies.split(',')

    result = []

    for currency in to_currencies:
        response = converter.sync_converter(from_currency=from_currency, to_currency=currency, price=price)

        result.append(response)

    return result

@router.get('/async/{from_currency}')
async def async_converter(from_currency:str = Path(max_length=3, regex='^[A-Z]{3}$'), 
                          to_currencies:str = Query(max_length=50, regex='^[A-Z]{3}(,[A-Z]{3})*$'), 
                          price:float = Query(gt=0)):
    
    to_currencies = to_currencies.split(',')

    coroutines = []

    for currency in to_currencies:
        coro = converter.async_converter(from_currency=from_currency, to_currency=currency, price=price)

        coroutines.append(coro)
    
    result = await gather(*coroutines)

    return result