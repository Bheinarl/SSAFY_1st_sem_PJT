from django.urls import path
from . import views

urlpatterns = [
    path('api/stocks/list/', views.stock_list, name='stock_list'),
    path('api/stocks/<str:ticker>/', views.stock_data, name='stock_data'),
]