from django.urls import path
from . import views

urlpatterns = [
	path('<int:portfolio_id>/', views.portfolio, name="portfolio"),
	path('create-portfolio/', views.create_portfolio, name="create_portfolio"),
	path('<int:portfolio_id>/create-transaction/', views.create_transaction, name="create_transaction"),
	path('<int:portfolio_id>/transaction/<int:transaction_id>/update/', views.update_transaction, name="update_transaction"),
	path('<int:portfolio_id>/transaction/<int:transaction_id>/delete/', views.delete_transaction, name="delete_transaction"),
	path('<int:portfolio_id>/update/', views.update_portfolio, name="update_portfolio"),
	path('<int:portfolio_id>/delete/', views.delete_portfolio, name="delete_portfolio"),
	path('search-assets/', views.search_assets_view, name='search_assets'),	
]