from django.shortcuts import render, redirect
from .forms import RegisterUserForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('dashboard')
	else:
		form = AuthenticationForm()
	context = {'form':form}
	return render(request, 'accounts/login.html', context)

def register_view(request):
	if request.method == 'POST':
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.save()
			login(request, user)
			return redirect('dashboard')
	else:
		form = RegisterUserForm()
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('login')