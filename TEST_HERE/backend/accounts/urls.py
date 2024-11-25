from django.urls import path
from . import views

urlpatterns = [
    path('set_alert/', views.set_alert, name='set_alert'),
    path('check_exchange_rate/', views.check_exchange_rate, name='check_exchange_rate'),
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),  # 환율 API 엔드포인트
    path('update_max_score/', views.update_max_score, name='update_max_score'),


    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('get_current_user/', views.get_current_user, name='get_current_user'),
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
]
