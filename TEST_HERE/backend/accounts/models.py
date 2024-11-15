from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, blank=True, null=True)  # nickname 필드 추가
    age = models.PositiveIntegerField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
