from django.urls import path
from . import views

urlpatterns = [
	path('<int:portfolio_id>', views.portfolio, name="portfolio")
]