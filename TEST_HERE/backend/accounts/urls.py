from django.urls import path
from . import views

urlpatterns = [
    path('set_alert/', views.set_alert, name='set_alert'),  # 환율 알람 설정 엔드포인트
    path('check_exchange_rate/', views.check_exchange_rate, name='check_exchange_rate'),  # 환율 알람 체크 엔드포인트
    path('get_exchange_rate/', views.get_exchange_rate, name='get_exchange_rate'),  # 환율 API 엔드포인트
    path('update_max_score/', views.update_max_score, name='update_max_score'),  # 최고 점수 업데이트 엔드포인트


    path('profile/', views.profile, name='profile'),  # 프로필 엔드포인트
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'), # 기타 기존 경로들 유지
    path('update_profile/', views.update_profile, name='update_profile'),  # 프로필 수정 엔드포인트
    path('get_current_user/', views.get_current_user, name='get_current_user'),  # 현재 유저 정보 엔드포인트
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),  # 리더보드 엔드포인트
]
