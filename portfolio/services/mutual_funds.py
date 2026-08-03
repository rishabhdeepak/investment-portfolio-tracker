import requests
from decimal import Decimal
from django.core.cache import cache
from django.conf import settings

BASE_URL = "https://api.mfapi.in"

def search_mutual_funds(query):
	response = requests.get(f"{BASE_URL}/mf/search",
						 params={"q":query}, timeout=10)
	
	results = []

	for item in response.json():
		results.append({
			"symbol" : str(item["schemeCode"]),
			"name": item["schemeName"],
			"quote_type": "MUTUAL_FUND",
			"exchange": "",
    		"sector": "",
    		"industry": "",
		})

	return results[:10]

def fetch_current_nav(scheme_code):
	response = requests.get(f"{BASE_URL}/mf/{scheme_code}/latest", timeout=10)
	response.raise_for_status()
	data = response.json()
	return Decimal(data["data"][0]["nav"])

def get_current_nav(scheme_code):
	cache_key = f"current_price:{scheme_code}"
	cached_nav = cache.get(cache_key)

	if cached_nav is not None:
		return cached_nav

	current_nav = fetch_current_nav(scheme_code)

	cache.set(cache_key, current_nav, settings.MUTUAL_FUND_NAV_CACHE_TIMEOUT)

	return current_nav
	