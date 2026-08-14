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

    combined_asset_values = {}
    combined_sector_values = {}


    # --------------------------------------------------
    # Combine data from all portfolios
    # --------------------------------------------------

    for portfolio in portfolios:

        summary = portfolio.get_portfolio_summary()

        total_invested += summary['total_invested']
        total_value += summary['total_value']
        total_profit_loss += summary['total_profit_loss']


        for holding in summary['holdings'].values():

            asset = holding['asset']
            current_value = holding['current_value']


            # Ignore holdings where current value
            # is unavailable

            if current_value is None:
                continue


            # --------------------------------------------------
            # Asset allocation
            # --------------------------------------------------

            asset_symbol = asset.symbol

            if asset_symbol not in combined_asset_values:

                combined_asset_values[asset_symbol] = Decimal('0')

            combined_asset_values[asset_symbol] += current_value


            # --------------------------------------------------
            # Sector allocation
            # --------------------------------------------------

            sector = asset.sector or 'Unknown'

            if sector not in combined_sector_values:

                combined_sector_values[sector] = Decimal('0')

            combined_sector_values[sector] += current_value


    # --------------------------------------------------
    # Build allocation data
    # --------------------------------------------------

    combined_asset_allocation = build_allocation(
        combined_asset_values,
        total_value
    )

    combined_sector_allocation = build_allocation(
        combined_sector_values,
        total_value
    )


    # --------------------------------------------------
    # Overall portfolio return
    # --------------------------------------------------

    if total_invested > 0:

        total_return_percentage = (
            total_profit_loss / total_invested
        ) * Decimal('100')

    else:

        total_return_percentage = Decimal('0')


    # --------------------------------------------------
    # Chart data
    # --------------------------------------------------

    asset_labels = list(
        combined_asset_allocation.keys()
    )

    asset_values = [
        data['allocation_percentage']
        for data in combined_asset_allocation.values()
    ]


    sector_labels = list(
        combined_sector_allocation.keys()
    )

    sector_values = [
        data['allocation_percentage']
        for data in combined_sector_allocation.values()
    ]


    # --------------------------------------------------
    # Return dashboard context
    # --------------------------------------------------

    return {

        'portfolios': portfolios,

        'total_invested': total_invested,

        'total_value': total_value,

        'total_profit_loss': total_profit_loss,

        'total_return_percentage': total_return_percentage,

        # Exact asset allocation data
        # Used by the table

        'combined_asset_allocation':
            combined_asset_allocation,

        # Exact sector allocation data
        # Used by the table

        'combined_sector_allocation':
            combined_sector_allocation,

        # Percentage data
        # Used by Chart.js

        'asset_labels':
            asset_labels,

        'asset_values':
            asset_values,

        'sector_labels':
            sector_labels,

        'sector_values':
            sector_values,
    }