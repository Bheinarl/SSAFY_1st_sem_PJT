from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/stocks/', include('stocks.urls')), # 이거 순서 조심해야 함
    path('accounts/', include('accounts.urls')),
    path('api/auth/', include('accounts.urls')),  # accounts의 사용자 정보 URL 포함
    path('', include('stocks.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('stocks/', include('stocks.urls')), # stocks 앱의 URL 포함
    path('api/', include('maps.urls')), # maps 앱 관련 url ----- 여기 url들 너무 복잡해요 이거 맞나용
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
