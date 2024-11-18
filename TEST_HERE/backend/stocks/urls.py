from django.urls import path
from . import views

urlpatterns = [
    path('get_stock_data/', views.get_stock_data, name='get_stock_data'),
    path('api/stock-data/', views.get_stock_data, name='get_stock_data'),
]