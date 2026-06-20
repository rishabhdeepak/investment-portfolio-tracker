from django.contrib import admin
from .models import Portfolio, Asset, Transaction

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'base_currency',
        'created_at',
    )

    search_fields = (
        'name',
        'user__username',
    )

    list_filter = (
        'base_currency',
        'created_at',
    )

    ordering = (
        '-created_at',
    )
    

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'symbol',
        'name',
		'asset_type',
        'exchange',
        'sector',
    )

    search_fields = (
        'symbol',
		'name',
    )

    list_filter = (
        'asset_type',
		'exchange',
    )

    ordering = (
        'symbol',
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'portfolio',
    	'asset',
    	'transaction_type',
    	'quantity',
    	'price',
    	'transaction_date',
    )

    search_fields = (
    'asset__symbol',
    'asset__name',
    'portfolio__name',
	)

    list_filter = (
    'transaction_type',
    'transaction_date',
	)

    ordering = (
        ('-transaction_date',)
    )