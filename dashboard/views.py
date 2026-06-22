from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
	portfolios = request.user.portfolios.all()
	context = {'portfolios': portfolios}
	return render(request, 'dashboard/dashboard.html', context)