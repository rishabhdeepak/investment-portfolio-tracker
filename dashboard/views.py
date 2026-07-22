from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import get_dashboard_summary

@login_required(login_url='login')
def dashboard(request):
    context = get_dashboard_summary(request.user)
    return render(request, 'dashboard/dashboard.html', context)