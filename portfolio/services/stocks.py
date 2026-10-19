import yfinance as yf
from django.core.cache import cache
from django.conf import settings

def get_current_price(ticker):

    cache_key = f'current_price:{ticker}'
    cached_price = cache.get(cache_key)

    if cached_price is not None:
        return cached_price

    current_price = fetch_current_price(ticker)

    cache.set(cache_key, current_price, timeout=settings.MARKET_PRICE_CACHE_TIMEOUT)

    return current_price

def fetch_current_price(ticker):
    try:
        ticker_obj = yf.Ticker(ticker)
        return ticker_obj.fast_info['lastPrice']
    except Exception as e:
        print(f"Failed to fetch {ticker}: {e}")
        return None

def search_assets(query):
    search = yf.Search(query)
    results = []
    for item in search.quotes:
        if item.get('quoteType') not in [
            'EQUITY',
            'ETF',
            'CRYPTOCURRENCY',
        ]:
            continue
        symbol = item.get('symbol')
        if not symbol:
            continue
        try:
            ticker_obj = yf.Ticker(symbol)
            currency = ticker_obj.fast_info.get('currency')
        except Exception:
            currency = None
        results.append({
            'symbol': symbol,
            'name': item.get('longname') or item.get('shortname'),
            'quote_type': item.get('quoteType'),
            'exchange': item.get('exchDisp'),
            'sector': item.get('sector'),
            'industry': item.get('industryDisp'),
            'quote_currency': currency,
        })
    return results[:10]