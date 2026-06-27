from django import forms
from .models import Portfolio, Transaction

class PortfolioForm(forms.ModelForm):
	class Meta:
		model = Portfolio
		fields = ['name', 'base_currency']

class TransactionForm(forms.ModelForm):
	class Meta:
		model = Transaction
		fields = ['asset', 'transaction_type', 'quantity', 'price',
			'fees','taxes', 'transaction_date', 'notes']
		widgets = {'transaction_date': forms.DateInput(attrs={'type': 'date'})}
		
		