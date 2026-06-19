from django.db import models
from django.conf import settings

class Portfolio(models.Model):

	CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
						     related_name='portfolios')
	
	name = models.CharField(max_length=100)

	base_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
								     default='INR')
	
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
	

class Asset(models.Model):
	ASSET_TYPE_CHOICES = [
		('STOCK', 'Stock'),
		('ETF', 'ETF'),
		('BOND', 'Bond'),
		('MUTUAL_FUND', 'Mutual Fund'),
		('CRYPTO', 'Crypto'),
	]

	symbol = models.CharField(max_length=20, unique=True)

	name = models.CharField(max_length=200)

	asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES,
								  default='STOCK')	
	
	exchange = models.CharField(max_length=50, blank=True)

	sector = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return f"{self.symbol} - {self.name}"


class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('IMPORT', 'Imported Holding'),
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,
        						  related_name='transactions')

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT,
        					  related_name='transactions')

    transaction_type = models.CharField(max_length=10, 
										choices=TRANSACTION_TYPE_CHOICES)

    quantity = models.DecimalField(max_digits=15, decimal_places=4)

    price = models.DecimalField(max_digits=15, decimal_places=4)

    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    transaction_date = models.DateField()

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.transaction_type} "
            	f"{self.asset.symbol}")