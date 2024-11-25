# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/fetch_and_save_products/funds/', views.fetch_and_save_funds_products, name='get_fund_products'),
    path('api/fetch_and_save_products/<str:category>/', views.fetch_and_save_deposit_savings_products, name='fetch_and_save_deposit_savings_products'),
    path('api/products/funds/<str:subcategory>/', views.get_filtered_funds_products, name='get_filtered_products'),
    path('api/products/<str:category>/', views.get_filtered_deposit_savings_products, name='get_filtered_products'),
]