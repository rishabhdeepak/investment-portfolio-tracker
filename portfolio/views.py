from django.shortcuts import render

def portfolio(request):
	context = {}
	return render(request, 'portfolio/portfolio.html', context)