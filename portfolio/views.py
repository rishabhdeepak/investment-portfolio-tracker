from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def portfolio(request, portfolio_id):
	portfolio = get_object_or_404(request.user.portfolios, id=portfolio_id)
	holdings = portfolio.get_holdings()
	context = {'portfolio': portfolio,'holdings': holdings}
	return render(request, 'portfolio/portfolio.html', context)