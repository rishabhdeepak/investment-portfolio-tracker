from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PortfolioForm, TransactionForm

@login_required(login_url='login')
def portfolio(request, portfolio_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	holdings = portfolio.get_holdings()
	transactions = (portfolio.transactions.select_related('asset')
				 .order_by('-transaction_date', '-id'))
	context = {'portfolio': portfolio,'holdings': holdings,
			   'transactions': transactions}
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
		form.instance.portfolio = portfolio
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