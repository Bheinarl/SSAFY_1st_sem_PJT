from django.urls import path
from .views import stock_data

urlpatterns = [
    path('get_stock_data/', views.get_stock_data, name='get_stock_data'),
    path('api/stock-data/', views.get_stock_data, name='get_stock_data'),
    path('api/stocks/<str:ticker>/', stock_data),  # /api/stocks/<티커>/ 경로로 API 요청
]