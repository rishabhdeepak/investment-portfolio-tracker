from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm, TransactionForm
from .services.stocks import search_assets
from .services.mutual_funds import search_mutual_funds
from django.http import JsonResponse
from .models import Asset
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from django.conf import settings
import json

@login_required(login_url='login')
def portfolio(request, portfolio_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)

	summary = portfolio.get_portfolio_summary()

	transactions = (portfolio.transactions.select_related('asset')
				 .order_by('-transaction_date', '-id'))

	sector_labels = list(summary['sector_allocation'].keys())
	sector_values = [
        float(value)
        for value in summary['sector_allocation'].values()
    ]
	asset_labels = [
        holding['asset'].symbol
        for holding in summary['top_holdings']
    ]
	asset_values = [
        float(holding['allocation_percentage'])
        for holding in summary['top_holdings']
    ]
	
	context = {'portfolio': portfolio,
			   'holdings': summary['holdings'],
			   'transactions': transactions,
			   'total_invested': summary['total_invested'],
			   'total_value': summary['total_value'],
			   'total_profit_loss': summary['total_profit_loss'],
			   'portfolio_return_percentage': summary['portfolio_return_percentage'],
			   'sector_allocation' : summary['sector_allocation'],
			   'top_holdings' : summary['top_holdings'],
			   'best_performer' : summary['best_performer'],
			   'worst_performer' : summary['worst_performer'],
			   'sector_labels': sector_labels,
			   'sector_values': sector_values,
			   'asset_labels': asset_labels,
			   'asset_values': asset_values,
			   }
	return render(request, 'portfolio/portfolio.html', context)

@login_required(login_url='login')
def create_portfolio(request):
	if request.method == 'POST':
		form = PortfolioForm(request.POST)
		if form.is_valid():
			portfolio = form.save(commit=False)
			portfolio.user = request.user
			portfolio.save()
			return redirect('portfolio', portfolio_id=portfolio.id)
	else:
		form = PortfolioForm()
	context = {'form': form}
	return render(request, 'portfolio/create_portfolio.html', context)

@login_required(login_url='login')
def create_transaction(request, portfolio_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)

	if request.method == 'POST':
		form = TransactionForm(request.POST)

		symbol = request.POST.get('symbol')
		asset_name = request.POST.get('asset_name')
		quote_type = request.POST.get('quote_type')
		exchange = request.POST.get('exchange')
		sector = request.POST.get('sector')
		industry = request.POST.get('industry')

		asset_type_map = {
			"EQUITY": "STOCK",
			"ETF": "ETF",
			"CRYPTOCURRENCY": "CRYPTO",
			"MUTUAL_FUND": "MUTUAL_FUND",
			}
		
		asset, created = Asset.objects.get_or_create(
			symbol=symbol,
			defaults= {'name': asset_name,
			'asset_type': asset_type_map.get(quote_type, 'STOCK'),
			'exchange' : exchange or '',
			'sector' : sector or '',
			'industry': industry or ''
					 })

		form.instance.portfolio = portfolio
		form.instance.asset = asset

		if form.is_valid():
			transaction = form.save(commit=False)
			transaction.portfolio = portfolio
			transaction.save()
			return redirect('portfolio', portfolio_id=portfolio.id)
		
	else:
		form = TransactionForm()

	context = {'form': form, 'portfolio': portfolio}
	return render(request, 'portfolio/create_transaction.html', context)

@login_required(login_url='login')
def update_transaction(request, portfolio_id, transaction_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	transaction = get_object_or_404(portfolio.transactions, id=transaction_id)
	if request.method == 'POST':
		form = TransactionForm(request.POST, instance=transaction)
		if form.is_valid():
			form.save()
			return redirect('portfolio', portfolio_id=portfolio.id)
	else:
		form = TransactionForm(instance=transaction)
	context = {'form': form, 'portfolio': portfolio, 'transaction': transaction}
	return render(request, 'portfolio/update_transaction.html', context)

@login_required(login_url='login')
def delete_transaction(request, portfolio_id, transaction_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	transaction = get_object_or_404(portfolio.transactions, id=transaction_id)
	if request.method == 'POST':
		transaction.delete()
		return redirect('portfolio', portfolio_id=portfolio.id)
	context = {'portfolio': portfolio, 'obj': transaction}
	return render(request, 'portfolio/delete.html', context)

@login_required(login_url='login')
def update_portfolio(request, portfolio_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	if request.method == 'POST':
		form = PortfolioForm(request.POST, instance=portfolio)
		if form.is_valid():
			form.save()
			return redirect('portfolio', portfolio_id=portfolio.id)
	else:
		form = PortfolioForm(instance=portfolio)
	context = {'form': form, 'portfolio': portfolio}
	return render(request, 'portfolio/update_portfolio.html', context)

@login_required(login_url='login')
def delete_portfolio(request, portfolio_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	if request.method == 'POST':
		portfolio.delete()
		return redirect('home')
	context = {'obj': portfolio}
	return render(request, 'portfolio/delete.html', context)

@login_required(login_url='login')
def search_assets_view(request):
	query = request.GET.get('q', '').strip().lower()
	if not query:
		return JsonResponse([], safe=False)

	cache_key = f"search:{query}"
	cached_results = cache.get(cache_key)

	if cached_results is not None:
		return JsonResponse(cached_results, safe=False)
	
	with ThreadPoolExecutor(max_workers=2) as executor:
		stock_future = executor.submit(search_assets, query)
		mutual_fund_future = executor.submit(search_mutual_funds, query)

		try:
			stock_results = stock_future.result()
		except Exception:
			stock_results = []

		try:
			mutual_fund_results = mutual_fund_future.result()
		except Exception:
			mutual_fund_results = []

	results = stock_results+mutual_fund_results

	results.sort(
    key=lambda asset: (
        not asset["name"].lower().startswith(query),
        not asset["symbol"].lower().startswith(query),
        asset["name"].lower()))

	cache.set(cache_key, results, timeout=settings.SEARCH_CACHE_TIMEOUT,)

	return JsonResponse(results, safe=False)

@login_required(login_url='login')
def asset_detail(request, portfolio_id, asset_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	summary = portfolio.get_portfolio_summary()
	holdings = summary['holdings']
	asset = get_object_or_404(Asset.objects.filter(
		transactions__portfolio=portfolio).distinct(), id=asset_id)
	holding = holdings.get(asset.id)
	transactions = (portfolio.transactions.filter(asset=asset)
				 .order_by('-transaction_date', '-id'))

	context = {
		'portfolio': portfolio,
		'asset': asset,
		'transactions': transactions,
		'holding': holding
	}
	return render(request, 'portfolio/asset_details.html', context)
