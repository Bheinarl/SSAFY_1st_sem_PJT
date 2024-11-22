# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/products/<str:category>/', views.fetch_products, name='fetch_products'),
]