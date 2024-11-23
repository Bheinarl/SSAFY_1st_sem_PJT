from django.urls import path
from . import views

urlpatterns = [
    path('locations/', views.location_list),
]