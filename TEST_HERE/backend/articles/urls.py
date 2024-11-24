from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'', PostViewSet)  # 기본 경로 설정
# 이게 뭔데.. 하
urlpatterns = [
    path('', include(router.urls)),  # /api/posts/ 경로에 연결
]
