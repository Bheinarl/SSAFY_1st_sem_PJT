# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    investment_tendency = models.CharField(max_length=20, choices=[
        ('stable', '안정형'),
        ('aggressive', '공격형'),
        ('balanced', '균형형')
    ], null=True, blank=True)

    def __str__(self):
        return self.user.username

class CurrencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10)
    target_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.currency} Alert"
