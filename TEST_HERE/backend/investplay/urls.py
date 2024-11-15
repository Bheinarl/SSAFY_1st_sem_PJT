# from django.contrib import admin
# from django.urls import path, include
# from accounts.views import CustomRegisterView  # 커스텀 회원가입 뷰 임포트

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('accounts.urls')),
#     path('investment/', include('investment.urls')),

#     # dj-rest-auth 기본 로그인 및 인증 관련 URL
#     path('api/auth/', include('dj_rest_auth.urls')),  

#     # 커스텀 회원가입 URL (닉네임 중복 체크를 위해 필요)
#     path('api/auth/custom-registration/', CustomRegisterView.as_view(), name='custom_registration'),

#     # 기본 회원가입 URL
#     path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),  # accounts의 사용자 정보 URL 포함
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
