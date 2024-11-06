# articles/models.py

from django.db import models
from django.contrib.auth.models import User

class LocationBasedRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    recommended_product = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.recommended_product}"
