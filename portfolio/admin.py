from django.contrib import admin
from .models import Portfolio, Asset, Transaction

admin.site.register(Portfolio)
admin.site.register(Asset)
admin.site.register(Transaction)
