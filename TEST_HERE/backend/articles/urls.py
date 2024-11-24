from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 이게 뭔데.. 하
urlpatterns = [
    path('list/', views.post_list),  # /api/posts/ 경로에 연결, 게시글 조회
    path('create/', views.post_create),  # /api/posts/ 경로에 연결, 게시글 생성
]
