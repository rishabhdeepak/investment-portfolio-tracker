import yfinance as yf

def get_current_price(ticker):
    ticker_obj = yf.Ticker(ticker)
    return ticker_obj.fast_info['lastPrice']

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
            'exchange': item.get('exchDisp'),})
    return results[:10]