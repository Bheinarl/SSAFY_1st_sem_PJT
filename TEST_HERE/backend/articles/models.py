from django.conf import settings
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 유저 모델을 참조
        on_delete=models.CASCADE,
        related_name='posts',  # 사용자가 작성한 게시글에 접근 가능
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
