# accounts/urls.py

from django.urls import path
from . import views
from .views import CustomRegisterView
from .views import CustomUserDetailsView

urlpatterns = [
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),  # 환율 API 엔드포인트
    path('set_alert/', views.set_alert, name='set_alert'),
    path('check_exchange_rate/', views.check_exchange_rate, name='check_exchange_rate'),
    path('custom-registration/', CustomRegisterView.as_view(), name='custom_registration'),
    path('user/', CustomUserDetailsView.as_view(), name='user-details'),  # 사용자 정보 URL 오버라이드
    path('update_max_score/', views.update_max_score, name='update_max_score'),
]
