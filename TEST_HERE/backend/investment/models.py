from django.db import models
from accounts.models import CustomUser

class Investment(models.Model):
    ASSET_TYPES = [('stock', 'Stock'), ('bond', 'Bond'), ('etf', 'ETF')]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class InvestmentAnalysis(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    conservative_ratio = models.FloatField()
    aggressive_ratio = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
