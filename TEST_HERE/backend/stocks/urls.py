from django.urls import path
from .views import stock_data

urlpatterns = [
    path('api/stocks/<str:ticker>/', stock_data, name='stock_data'),
]