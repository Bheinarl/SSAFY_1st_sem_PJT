# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/fetch_and_save_products/<str:category>/', views.fetch_and_save_products, name='fetch_and_save_products'),
    path('api/products/<str:category>/', views.get_filtered_products, name='get_filtered_products'),
    
]