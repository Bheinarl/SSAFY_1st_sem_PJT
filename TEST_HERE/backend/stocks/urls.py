from django.urls import path
from .views import stock_data

urlpatterns = [
    path('api/stocks/<str:ticker>/', stock_data),  # /api/stocks/<티커>/ 경로로 API 요청
]
