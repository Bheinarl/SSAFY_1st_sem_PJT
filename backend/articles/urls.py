# articles/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('location_recommendation/', views.location_recommendation, name='location_recommendation'),
]
