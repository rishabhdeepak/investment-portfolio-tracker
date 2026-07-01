from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm, TransactionForm
from .services import search_assets
from django.http import JsonResponse
from .models import Asset
from decimal import Decimal

@login_required(login_url='login')
def portfolio(request, portfolio_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	holdings = portfolio.get_holdings()
	transactions = (portfolio.transactions.select_related('asset')
				 .order_by('-transaction_date', '-id'))
	
	total_invested = Decimal('0')
	total_value = Decimal('0')
	total_profit_loss = Decimal('0')
	for data in holdings.values():
		total_invested += data['total_cost']
		if data['current_value'] is not None:
			total_value += data['current_value']
		if data['profit_loss'] is not None:
			total_profit_loss += data['profit_loss']

	context = {'portfolio': portfolio,'holdings': holdings,
			   'transactions': transactions,'total_invested': total_invested,
			   'total_value': total_value,'total_profit_loss': total_profit_loss}
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
	query = request.GET.get('q', '')
	if not query:
		return JsonResponse([], safe=False)
	results = search_assets(query)
	return JsonResponse(results, safe=False)

@login_required(login_url='login')
def asset_detail(request, portfolio_id, asset_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	holdings = portfolio.get_holdings()
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
