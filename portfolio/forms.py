from django import forms
from .models import Portfolio, Transaction


# --------------------------------------------------
# Shared form styling
# --------------------------------------------------

INPUT_CLASS = (
    "w-full px-4 py-3 rounded-xl "
    "bg-slate-900 border border-slate-700 "
    "text-slate-100 placeholder-slate-500 "
    "outline-none transition "
    "focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-500/20"
)


SELECT_CLASS = (
    "w-full px-4 py-3 rounded-xl "
    "bg-slate-900 border border-slate-700 "
    "text-slate-100 "
    "outline-none transition "
    "focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-500/20 "
    "cursor-pointer"
)


TEXTAREA_CLASS = (
    "w-full px-4 py-3 rounded-xl "
    "bg-slate-900 border border-slate-700 "
    "text-slate-100 placeholder-slate-500 "
    "outline-none transition "
    "focus:border-blue-500 "
    "focus:ring-2 focus:ring-blue-500/20 "
    "resize-y"
)


# --------------------------------------------------
# Portfolio Form
# --------------------------------------------------

class PortfolioForm(forms.ModelForm):

    class Meta:

        model = Portfolio

        fields = [
            'name',
            'base_currency'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': INPUT_CLASS,
                    'placeholder': 'Enter portfolio name',
                }
            ),

            'base_currency': forms.Select(
                attrs={
                    'class': SELECT_CLASS,
                }
            ),

        }


# --------------------------------------------------
# Transaction Form
# --------------------------------------------------

class TransactionForm(forms.ModelForm):

    class Meta:

        model = Transaction

        fields = [
            'transaction_type',
            'quantity',
            'price',
            'fees',
            'taxes',
            'transaction_date',
            'notes',
        ]

        widgets = {

            'transaction_type': forms.Select(
                attrs={
                    'class': SELECT_CLASS,
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASS,
                    'placeholder': 'Enter quantity',
                    'step': 'any',
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASS,
                    'placeholder': 'Enter price',
                    'step': 'any',
                }
            ),

            'fees': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASS,
                    'placeholder': '0.00',
                    'step': 'any',
                }
            ),

            'taxes': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASS,
                    'placeholder': '0.00',
                    'step': 'any',
                }
            ),

            'transaction_date': forms.DateInput(
                attrs={
                    'class': INPUT_CLASS,
                    'type': 'date',
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': TEXTAREA_CLASS,
                    'placeholder': 'Add any notes about this transaction...',
                    'rows': 4,
                }
            ),

        }