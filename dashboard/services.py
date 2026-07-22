from decimal import Decimal

def build_allocation(values, total_value):
	allocation = {}

	if total_value>0:
		for key, value in values.items():
			allocation[key] = {
				'value' : value,
				'allocation_percentage' : (value/total_value)*Decimal('100')
			}

	else:
		for key, value in values.items():
			allocation[key] = {
				'value' : value,
				'allocation_percentage' : Decimal('0')
			}
	allocation = dict(sorted(
		allocation.items(), key= lambda item:item[1]['value'],
		reverse=True))

	return allocation

def get_dashboard_summary(user):
	portfolios = user.portfolios.all()

	total_invested = Decimal('0')
	total_value = Decimal('0')
	total_profit_loss = Decimal('0')

	combined_stock_values = {}
	combined_sector_values = {}

	for portfolio in portfolios:
		summary = portfolio.get_portfolio_summary()
		total_invested += summary['total_invested']
		total_value += summary['total_value']
		total_profit_loss += summary['total_profit_loss']

		for holding in summary['holdings'].values():
			asset_symbol = holding['asset'].symbol
			if asset_symbol not in combined_stock_values:
				combined_stock_values[asset_symbol] = Decimal('0')
			if holding['current_value'] is not None:
				combined_stock_values[asset_symbol] += holding['current_value']
			sector = holding['asset'].sector or 'Unknown'
			if sector not in combined_sector_values:
				combined_sector_values[sector] = Decimal('0')
			if holding['current_value'] is not None:
				combined_sector_values[sector] += holding['current_value']

	combined_stock_allocation = build_allocation(combined_stock_values, 
											  total_value)
	combined_sector_allocation = build_allocation(combined_sector_values, 
												  total_value)
		
	if total_invested>0:
		total_return_percentage = (total_profit_loss/total_invested)*Decimal('100')
	else:
		total_return_percentage = Decimal('0')

	return{
		'portfolios': portfolios,
        'total_invested': total_invested,
        'total_value': total_value,
        'total_profit_loss': total_profit_loss,
        'total_return_percentage': total_return_percentage,
		'combined_stock_allocation' : combined_stock_allocation,
		'combined_sector_allocation' : combined_sector_allocation	
	}