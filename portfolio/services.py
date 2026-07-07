import yfinance as yf
from django.core.cache import cache

def get_current_price(ticker):

    cache_key = f'current_price:{ticker}'
    cached_price = cache.get(cache_key)

    if cached_price is not None:
        return cached_price

    ticker_obj = yf.Ticker(ticker)
    current_price = ticker_obj.fast_info['lastPrice']

    cache.set(cache_key, current_price, timeout=300)

    return current_price

def search_assets(query):
    search = yf.Search(query)
    results = []
    for item in search.quotes:
        if item.get('quoteType') not in ['EQUITY','ETF','CRYPTOCURRENCY']:
            continue
        results.append({
            'symbol': item.get('symbol'),
            'name': item.get('longname') or item.get('shortname'),
            'quote_type': item.get('quoteType'),
            'exchange': item.get('exchDisp'),
            'sector': item.get('sector'),
            'industry': item.get('industryDisp')})
    return results[:10]