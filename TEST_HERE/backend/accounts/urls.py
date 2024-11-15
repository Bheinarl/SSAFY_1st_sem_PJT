from django.urls import path
from .views import CustomRegisterView

urlpatterns = [
    path('custom-registration/', CustomRegisterView.as_view(), name='custom_registration'),
]

from django.urls import path
from .views import CustomUserDetailsView

urlpatterns += [
    path('user/', CustomUserDetailsView.as_view(), name='user-details'),  # 사용자 정보 URL 오버라이드
]
