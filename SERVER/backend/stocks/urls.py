from django.urls import path
from . import views
from .views import fetch_news

urlpatterns = [
    path('api/stocks/list/', views.stock_list, name='stock_list'),
    path('api/stocks/generate_random_date/', views.generate_random_date, name='generate_random_date'),
    path('api/stocks/fetch_news/', fetch_news, name='fetch_news'),
    path('api/stocks/find_stock_data/<str:ticker>/', views.stock_data, name='stock_data'),
]