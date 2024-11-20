from django.urls import path
from .views import fetch_news

urlpatterns = [
    path('fetch-news/', fetch_news, name='fetch_news'),
]
