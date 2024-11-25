from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # accounts 앱의 URL 포함
    path('', include('stocks.urls')),
    path('stocks/', include('stocks.urls')), # stocks 앱의 URL 포함
    path('finances/', include('finances.urls')), # finances 앱의 URL 포함
    path('api/auth/', include('accounts.urls')),  # accounts의 사용자 정보 URL 포함
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/', include('maps.urls')), # maps 앱 관련 url
    path('api/articles/', include('articles.urls')),  # articles 앱 URL
    path('api/posts/', include('articles.urls')),  # articles 앱의 URL 포함

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
