from celery import shared_task
from django.core.cache import cache
from django.conf import settings
import yfinance as yf
from .models import Asset
from .services import fetch_current_price

@shared_task
def refresh_market_prices():
	assets = Asset.objects.filter(transactions__isnull= False).distinct()
	for asset in assets:
		try:
			current_price = fetch_current_price(asset.symbol)

			cache_key = f'current_price:{asset.symbol}'
			cache.set(cache_key, current_price, timeout=settings.MARKET_PRICE_CACHE_TIMEOUT)
		except Exception as e:
			print(
				f'FAILED  TO REFRESH {asset.symbol}: '
				f'{type(e).__name__}: {e}'
			)