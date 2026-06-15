from django.shortcuts import render
from django.http import HttpResponse

def portfolio(request):
	return HttpResponse("Portfolio")