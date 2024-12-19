from django.conf import settings
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.IntegerField(default=0)  # 좋아요 수
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 유저 모델을 참조
        on_delete=models.CASCADE,  # 사용자가 삭제되면 게시글도 삭제
        related_name='posts',  # 사용자가 작성한 게시글에 접근 가능
    )
    liked_users = models.ManyToManyField(  # 좋아요를 누른 사용자 목록
        settings.AUTH_USER_MODEL,  # 커스텀 유저 모델을 참조
        related_name='liked_posts',  # 사용자가 좋아요를 누른 게시글에 접근 가능
        blank=True,  # 좋아요를 누르지 않은 사용자는 빈 목록
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # 댓글이 속한 게시물
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"