from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CurrencyAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # null=True, blank=True 추가
    currency = models.CharField(max_length=10)
    target_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.currency} Alert"

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, blank=True, null=True)  # nickname 필드 추가
    age = models.PositiveIntegerField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    max_score = models.IntegerField(default=0)  # max_score 필드 추가

    def __str__(self):
        return self.nickname if self.nickname else self.username