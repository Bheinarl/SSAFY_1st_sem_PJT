from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('list/', views.post_list),  # /api/posts/ 경로에 연결, 게시글 조회
    path('create/', views.post_create),  # /api/posts/ 경로에 연결, 게시글 생성
    path('<int:post_id>/', views.post_detail, name='post_detail'),  # 상세 페이지
    path('<int:post_id>/edit/', views.post_edit, name='post_edit'),  # 상세 페이지 수정
    path('<int:post_id>/delete/', views.post_delete, name='post_delete'),  # 게시물 삭제
    path('<int:post_id>/like/', views.post_like, name='post_like'),  # 게시물 좋아요
    path('<int:post_id>/comments/', views.comment_list, name='comment-list'),  # 댓글 조회
    path('<int:post_id>/comments/create/', views.comment_create, name='comment-create'),  # 댓글 생성
]
