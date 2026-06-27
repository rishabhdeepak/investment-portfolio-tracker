from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ValidationError

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

    def get_holdings(self, exclude_transaction_id=None):
        holdings = {}
        transactions = (self.transactions.select_related('asset').
                        order_by('transaction_date', 'id'))
        if exclude_transaction_id:
            transactions = transactions.exclude(id=exclude_transaction_id)
        for txn in transactions:
            asset_id = txn.asset_id
            if asset_id not in holdings:
                holdings[asset_id] = {
                    'asset': txn.asset,
                    'quantity': Decimal('0'),
                    'total_cost': Decimal('0'),
                }
            if txn.transaction_type in ['BUY', 'IMPORT']:
                holdings[asset_id]['quantity'] += txn.quantity
                holdings[asset_id]['total_cost'] += (txn.quantity * txn.price
                                                      + txn.fees + txn.taxes)
            elif txn.transaction_type == 'SELL':
                current_quantity = holdings[asset_id]['quantity']
                if current_quantity <= 0:
                    continue

                avg_cost = (holdings[asset_id]['total_cost']) / current_quantity
                holdings[asset_id]['quantity'] -= txn.quantity
                holdings[asset_id]['total_cost'] -= (txn.quantity * avg_cost)

        holdings = {asset_id: data for asset_id, data in holdings.items()
                    if data['quantity'] > 0}

        for data in holdings.values():
            data['avg_buy_price'] = (data['total_cost'] / data['quantity'])
        return holdings

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

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError({
                'quantity': (
                    "Quantity must be greater than zero."
                )
            })
        if self.price < 0:
            raise ValidationError({
                'price': (
                    "Price cannot be negative."
                )
            })
        if self.fees < 0:
            raise ValidationError({
                'fees': (
                    "Fees cannot be negative."
                )
            })
        if self.taxes < 0:
            raise ValidationError({
                'taxes': (
                    "Taxes cannot be negative."
                )
            })
        if self.transaction_type == 'SELL':
            holdings = self.portfolio.get_holdings(
                exclude_transaction_id= self.id if self.pk else None)
            asset_id = self.asset_id
            if asset_id not in holdings:
                raise ValidationError({
                    'asset': (
                        "Cannot sell an asset that is not held."
                    )
                })
            if self.quantity > holdings[asset_id]['quantity']:
                raise ValidationError({
                    'quantity': (
                        "Cannot sell more than the quantity held."
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    @property
    def total_value(self):
        return (self.quantity * self.price) + self.fees + self.taxes

    def __str__(self):
        return (f"{self.transaction_type} "
                f"{self.asset.symbol}")