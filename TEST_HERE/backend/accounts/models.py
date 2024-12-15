from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from PIL import Image

class CurrencyAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # 유저가 삭제되면 알람도 삭제
    currency = models.CharField(max_length=10)  # 알람 원하는 통화
    target_rate = models.FloatField()  # 알람 원하는 환율 수치
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.currency} Alert"

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, blank=True, null=True)  # nickname 필드 추가
    age = models.PositiveIntegerField(null=True, blank=True)  # age 필드 추가
    my_investor_type = models.TextField(null=True, blank=True)  # my_investor_type 필드 추가
    max_score = models.IntegerField(default=0)  # max_score 필드 추가
    profile_picture = models.ImageField(
        upload_to='media/images/',
        default='static/images/default-user.png',  # 기본 이미지 설정
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.nickname if self.nickname else self.username  # nickname이 있으면 nickname을, 없으면 username을 반환
